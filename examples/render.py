"""Regenerate the README example figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import paperstyle as ps
from matplotlib.ticker import PercentFormatter

OUT = Path(__file__).parents[1] / "docs"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(12)


def save(fig, name):
    ps.savefig(fig, OUT / name, formats=("pdf", "png", "svg"), dpi=300)
    plt.close(fig)


def lines():
    ps.use(tex=False)
    x = np.linspace(0, 10, 180)
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.32))
    for i, phase in enumerate(np.linspace(0, 3.5, 6)):
        y = np.exp(-0.12 * x) * (0.63 + 0.16 * np.sin(x + phase)) + 0.022 * phase
        ax.plot(x, y, label=f"Model {i + 1}")
    ax.set(
        xlabel=r"Training step ($\times 10^3$)", ylabel="Validation error", xlim=(0, 10)
    )
    ax.legend(ncols=6)
    save(fig, "lines")


def bars():
    ps.use(tex=False, palette="gradient")
    names = ["MACE", "ORB", "eqV2", "SevenNet", "GRACE", "MatterSim"]
    values = [0.82, 0.76, 0.88, 0.71, 0.79, 0.84]
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.27))
    ax.bar(names, values, width=0.66, color=ps.colors.GRADIENT[: len(names)])
    ax.grid(axis="y")
    ax.set(ylabel="Success rate", ylim=(0.6, 0.92))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    save(fig, "bars")


def scatter():
    ps.use(tex=False)
    target = rng.uniform(0, 1, 220)
    pred = target + rng.normal(0, 0.07, len(target))
    fig, ax = plt.subplots(figsize=ps.size("default", ratio=0.78))
    ax.scatter(
        target, pred, s=12, alpha=0.58, color=ps.colors.CONTRAST[2], rasterized=True
    )
    ax.plot([0, 1], [0, 1], color=ps.colors.GREY_DARK, zorder=-10)
    ax.set(xlabel="Reference", ylabel="Prediction", xlim=(0, 1), ylim=(0, 1))
    save(fig, "scatter")


def variants():
    ps.use(tex=False)
    x = np.linspace(0, 10, 180)
    colors = ps.shades(ps.colors.GRADIENT[3], 4)
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.31))
    for i, color in enumerate(colors):
        y = 0.19 + 0.085 * np.exp(-0.28 * x) + 0.012 * i + 0.008 * np.sin(1.4 * x + i)
        ax.plot(x, y, color=color, label=f"Variant {i + 1}")
    ax.set(xlabel=r"Training step ($\times 10^3$)", ylabel="Error", xlim=(0, 10))
    ax.legend(ncols=4)
    save(fig, "variants")


def distributions():
    ps.use(tex=False)
    groups = [
        rng.normal(0.73, 0.09, 70),
        rng.normal(0.61, 0.08, 70),
        rng.normal(0.68, 0.11, 70),
        rng.normal(0.54, 0.07, 70),
        rng.normal(0.64, 0.09, 70),
    ]
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.30))
    positions = np.arange(len(groups))
    violins = ax.violinplot(
        groups,
        positions=positions,
        widths=0.65,
        showmeans=False,
        showmedians=False,
        showextrema=False,
    )
    for body in violins["bodies"]:
        body.set_facecolor("none")
        body.set_edgecolor(ps.colors.BLACK)
        body.set_linewidth(0.7)
        body.set_alpha(1)
    for i, values in enumerate(groups):
        jitter = rng.normal(0, 0.045, len(values))
        ax.scatter(
            positions[i] + jitter,
            values,
            s=12,
            alpha=0.5,
            color=ps.colors.GRADIENT[i],
            rasterized=True,
        )
    ax.grid(axis="y")
    ax.set_xticks(positions, ["MACE", "ORB", "eqV2", "SevenNet", "GRACE"])
    ax.set_ylabel("Relative error")
    save(fig, "distributions")


def iclr_panels():
    ps.use("iclr", height=2.53, tex=False)
    fig = plt.figure()
    fig.set_layout_engine("none")
    outer = fig.add_gridspec(
        1,
        2,
        width_ratios=(1.0, 1.6),
        left=0.11,
        right=0.98,
        top=0.82,
        bottom=0.29,
        wspace=0.32,
    )

    validity = fig.add_subplot(outer[0, 0])
    sizes = np.arange(4)
    rates = (
        (0.985, 0.974, 0.956, 0.941),
        (0.979, 0.958, 0.929, 0.901),
        (0.971, 0.943, 0.912, 0.884),
    )
    names = ("Method A (ours)", "Method B", "Method C")
    for name, values in zip(names, rates, strict=True):
        validity.plot(sizes, values, marker="o", label=name)
    validity.set_title("Validity")
    validity.set_xlabel("System size")
    validity.set_ylabel("Valid structures")
    validity.set_xticks(sizes, ("Small", "Medium", "Large", "XL"))
    validity.set_ylim(0.86, 1.0)
    validity.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    validity.grid(axis="y")

    distribution_grid = outer[0, 1].subgridspec(2, 2, hspace=0.58, wspace=0.32)
    distribution_axes = []
    x = np.linspace(0, 4, 120)
    for index in range(4):
        ax = fig.add_subplot(distribution_grid[index // 2, index % 2])
        distribution_axes.append(ax)
        center = 1.35 + 0.28 * index
        for method in range(3):
            curve = np.exp(-0.5 * ((x - center - 0.10 * method) / 0.42) ** 2)
            ax.plot(x, curve, color=ps.colors.CONTRAST[method])
        if index < 2:
            ax.set_title(("Small", "Large")[index])
            ax.set_xticklabels([])
        else:
            ax.set_xlabel("Distance")
        if index % 2:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel("Density")

    ps.panel_labels(fig, (validity, distribution_axes[0]), ("a", "b"))
    fig.legend(
        handles=validity.lines,
        labels=names,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.055),
        ncols=3,
    )
    save(fig, "iclr_panels")


if __name__ == "__main__":
    lines()
    bars()
    scatter()
    variants()
    distributions()
    iclr_panels()
