"""Matplotlib styling and figure-size helpers."""

from __future__ import annotations

import colorsys
import shutil
import warnings
from collections.abc import Sequence
from contextlib import contextmanager
from functools import lru_cache

import matplotlib as mpl
from cycler import cycler
from matplotlib import colors as mpl_colors
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.transforms import offset_copy

from . import colors

_WIDTHS = {
    "default": 4.05,
    "iclr": 5.5,
    "column": 3.25,
    "wide": 6.75,
}

_DEFAULT_RATIO = 0.618

_TEX_PREAMBLE = (
    r"\usepackage{times} "
    r"\renewcommand{\familydefault}{\sfdefault} "
    r"\usepackage{upgreek}"
)

_TEX_WARNING = """paperstyle could not render with LaTeX and fell back to Matplotlib text.

Install the TeX tools used by the style:
  Ubuntu/Debian:
    sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science dvipng
  macOS:
    brew install --cask mactex-no-gui
  Windows:
    install MiKTeX and enable automatic package installation

Restart Python afterwards. To intentionally disable TeX, use paperstyle.use(tex=False).
"""


def size(
    preset: str = "default",
    *,
    ratio: float = _DEFAULT_RATIO,
    nrows: int = 1,
    ncols: int = 1,
) -> tuple[float, float]:
    """Return a publication-aware Matplotlib figure size in inches."""
    width = _WIDTHS[preset]
    subplot_width = width / ncols
    return width, ratio * subplot_width * nrows


def lighten(color: str, amount: float = 1.2) -> str:
    """Scale a color's lightness while preserving its hue."""
    hue, lightness, saturation = colorsys.rgb_to_hls(*mpl_colors.to_rgb(color))
    rgb = colorsys.hls_to_rgb(
        hue,
        min(1.0, max(0.0, amount * lightness)),
        saturation,
    )
    return mpl_colors.to_hex(rgb)


def shades(color: str, n: int = 4, step: float = 0.15) -> tuple[str, ...]:
    """Create related colors with progressively increasing lightness."""
    return tuple(lighten(color, 1.0 + step * i) for i in range(n))


@lru_cache(maxsize=1)
def _tex_available() -> bool:
    if shutil.which("latex") is None:
        return False

    params = {
        "text.usetex": True,
        "font.family": "sans-serif",
        "text.latex.preamble": _TEX_PREAMBLE,
    }
    try:
        with mpl.rc_context(params):
            figure = Figure(figsize=(0.2, 0.2))
            canvas = FigureCanvasAgg(figure)
            figure.text(0.5, 0.5, r"$\alpha + \upmu$")
            canvas.draw()
    except (RuntimeError, OSError):
        return False
    return True


def _resolve_palette(palette: str | Sequence[str]) -> Sequence[str]:
    if isinstance(palette, str):
        return colors.PALETTES[palette]
    return palette


def style(
    preset: str = "default",
    *,
    tex: bool = True,
    palette: str | Sequence[str] = "contrast",
    ratio: float = _DEFAULT_RATIO,
    nrows: int = 1,
    ncols: int = 1,
) -> dict:
    """Return the paperstyle rcParams dictionary."""
    use_tex = tex and _tex_available()
    if tex and not use_tex:
        warnings.warn(_TEX_WARNING, RuntimeWarning, stacklevel=2)

    params = {
        "text.usetex": use_tex,
        "font.family": "sans-serif",
        "font.sans-serif": [
            "Helvetica",
            "Helvetica Neue",
            "Arial",
            "Nimbus Sans",
            "DejaVu Sans",
        ],
        "mathtext.fontset": "stix",
        "font.size": 8.0,
        "axes.labelsize": 8.0,
        "axes.titlesize": 8.0,
        "axes.titlelocation": "center",
        "legend.fontsize": 6.0,
        "xtick.labelsize": 6.0,
        "ytick.labelsize": 6.0,
        "axes.linewidth": 0.5,
        "lines.linewidth": 1.0,
        "lines.markersize": 4.0,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "xtick.minor.width": 0.25,
        "ytick.minor.width": 0.25,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "xtick.minor.size": 2.0,
        "ytick.minor.size": 2.0,
        "axes.axisbelow": True,
        "axes.prop_cycle": cycler(color=_resolve_palette(palette)),
        "axes.grid": False,
        "grid.color": colors.GREY_LIGHT,
        "grid.linewidth": 0.5,
        "grid.alpha": 1.0,
        "legend.frameon": False,
        "legend.fancybox": False,
        "legend.borderaxespad": 0.4,
        "legend.handlelength": 1.6,
        "legend.columnspacing": 1.0,
        "figure.dpi": 144,
        "savefig.dpi": 300,
        "savefig.bbox": None,
        "savefig.pad_inches": 0.04,
        "figure.constrained_layout.use": True,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "figure.figsize": size(
            preset,
            ratio=ratio,
            nrows=nrows,
            ncols=ncols,
        ),
    }
    if use_tex:
        params["text.latex.preamble"] = _TEX_PREAMBLE
    return params


def panel_label(
    ax,
    label: str,
    *,
    x: float = 0.0,
    y: float = 1.12,
    ha: str = "left",
    transform=None,
):
    """Add a panel label with the standard rounded backdrop."""
    transform = ax.transAxes if transform is None else transform

    # Separate artists allow an optical correction without moving the backdrop.
    ax.text(
        x,
        y,
        label,
        transform=transform,
        ha=ha,
        va="center",
        fontweight="bold",
        color="none",
        bbox={
            "boxstyle": "round,pad=0.28",
            "facecolor": colors.SURFACE,
            "edgecolor": "none",
        },
        clip_on=False,
        zorder=100,
    )
    return ax.text(
        x,
        y,
        label,
        transform=offset_copy(
            transform,
            fig=ax.figure,
            y=-0.75,
            units="points",
        ),
        ha=ha,
        va="center",
        fontweight="bold",
        clip_on=False,
        zorder=101,
    )


def panel_labels(
    fig,
    axes: Sequence,
    labels: Sequence[str],
    *,
    x_offset: float = 12.5,
    y_offset: float = 5.0,
):
    """Add major-panel labels on one baseline, aligned to panel left edges.

    Offsets are in points. The shared baseline follows the first panel title,
    or the top of the axes when no panel has a title.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    title_axis = next((ax for ax in axes if ax.get_title()), None)

    if title_axis is None:
        label_y = max(ax.get_window_extent(renderer).y1 for ax in axes)
    else:
        title_bounds = title_axis.title.get_window_extent(renderer)
        label_y = (title_bounds.y0 + title_bounds.y1) / 2
    label_y += y_offset * fig.dpi / 72

    to_figure = fig.transFigure.inverted()
    artists = []
    for label, ax in zip(labels, axes, strict=True):
        label_x = ax.get_window_extent(renderer).x0 - x_offset * fig.dpi / 72
        x, y = to_figure.transform((label_x, label_y))
        artists.append(
            panel_label(
                ax,
                label,
                x=x,
                y=y,
                ha="right",
                transform=fig.transFigure,
            )
        )
    return tuple(artists)


def use(
    preset: str = "default",
    *,
    tex: bool = True,
    palette: str | Sequence[str] = "contrast",
    ratio: float = _DEFAULT_RATIO,
    nrows: int = 1,
    ncols: int = 1,
) -> None:
    """Apply paperstyle globally to Matplotlib."""
    mpl.rcParams.update(
        style(
            preset,
            tex=tex,
            palette=palette,
            ratio=ratio,
            nrows=nrows,
            ncols=ncols,
        )
    )


@contextmanager
def context(
    preset: str = "default",
    *,
    tex: bool = True,
    palette: str | Sequence[str] = "contrast",
    ratio: float = _DEFAULT_RATIO,
    nrows: int = 1,
    ncols: int = 1,
):
    """Temporarily apply paperstyle inside a with block."""
    with mpl.rc_context(
        style(
            preset,
            tex=tex,
            palette=palette,
            ratio=ratio,
            nrows=nrows,
            ncols=ncols,
        )
    ):
        yield
