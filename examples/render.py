"""Regenerate the README example figures."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import paperstyle as ps

OUT = Path(__file__).parents[1] / "docs"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(12)


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=180)
    with mpl.rc_context({"svg.fonttype": "path"}):
        fig.savefig(OUT / f"{name}.svg")
    plt.close(fig)


def lines():
    ps.use()
    x = np.linspace(0, 10, 180)
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.32))
    for i, phase in enumerate(np.linspace(0, 3.5, 6)):
        y = np.exp(-0.12 * x) * (0.63 + 0.16 * np.sin(x + phase)) + 0.022 * phase
        ax.plot(x, y, label=f"Model {i + 1}")
    ax.set(xlabel=r"Training step ($\times 10^3$)", ylabel="Validation error", xlim=(0, 10))
    ax.legend(ncols=6)
    save(fig, "lines")


def bars():
    ps.use(palette="gradient")
    names = ["MACE", "ORB", "eqV2", "SevenNet", "GRACE", "MatterSim"]
    values = [0.82, 0.76, 0.88, 0.71, 0.79, 0.84]
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.27))
    ax.bar(names, values, width=0.66, color=ps.colors.GRADIENT[:len(names)])
    ax.grid(axis="y")
    ax.set(ylabel="Success rate", ylim=(0.6, 0.92))
    save(fig, "bars")


def scatter():
    ps.use()
    target = rng.uniform(0, 1, 220)
    pred = target + rng.normal(0, 0.07, len(target))
    fig, ax = plt.subplots(figsize=ps.size("default", ratio=0.78))
    ax.scatter(target, pred, s=12, alpha=0.58, color=ps.colors.CONTRAST[2], rasterized=True)
    ax.plot([0, 1], [0, 1], color=ps.colors.GREY_DARK, zorder=-10)
    ax.set(xlabel="Reference", ylabel="Prediction", xlim=(0, 1), ylim=(0, 1))
    save(fig, "scatter")


def variants():
    ps.use()
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
    ps.use()
    groups = [
        rng.normal(0.73, 0.09, 70),
        rng.normal(0.61, 0.08, 70),
        rng.normal(0.68, 0.11, 70),
        rng.normal(0.54, 0.07, 70),
        rng.normal(0.64, 0.09, 70),
    ]
    fig, ax = plt.subplots(figsize=ps.size("wide", ratio=0.30))
    positions = np.arange(len(groups))
    violins = ax.violinplot(groups, positions=positions, widths=0.65, showmeans=False, showmedians=False, showextrema=False)
    for body in violins["bodies"]:
        body.set_facecolor("none")
        body.set_edgecolor(ps.colors.BLACK)
        body.set_linewidth(0.7)
        body.set_alpha(1)
    for i, values in enumerate(groups):
        jitter = rng.normal(0, 0.045, len(values))
        ax.scatter(positions[i] + jitter, values, s=12, alpha=0.5, color=ps.colors.GRADIENT[i], rasterized=True)
    ax.grid(axis="y")
    ax.set_xticks(positions, ["MACE", "ORB", "eqV2", "SevenNet", "GRACE"])
    ax.set_ylabel("Relative error")
    save(fig, "distributions")


def iclr_panels():
    ps.use("iclr", ncols=2, ratio=0.72)
    fig, axes = plt.subplots(1, 2)
    fig.subplots_adjust(top=0.84)
    for i, ax in enumerate(axes):
        x = np.linspace(0, 1, 120)
        for j in range(3):
            ax.plot(x, (j + 1) * (x ** (1.2 + 0.2 * i)) / 3, label=f"Method {j + 1}")
        ax.set_xlabel("Normalized time")
        ax.set_title(["Reconstruction", "Generation"][i])
        ps.panel_label(ax, chr(ord("a") + i))
    axes[0].set_ylabel("Score")
    axes[1].legend()
    save(fig, "iclr_panels")


if __name__ == "__main__":
    lines()
    bars()
    scatter()
    variants()
    distributions()
    iclr_panels()
