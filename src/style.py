"""
Shared chart style for every notebook in the project.

One place for the theme, colors, labels, and figure export, so every chart in
the notebooks and the policy brief reads as one system.

Usage (from a notebook in notebooks/):
    import sys; sys.path.append("../src")
    from style import *
    apply_style()
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
INK = "#0B0B0B"          # titles
INK_SECONDARY = "#52514E"  # axis labels, subtitles, legend text
INK_MUTED = "#898781"    # tick labels, source notes
GRID = "#E1E0D9"
BASELINE = "#C3C2B7"
SURFACE = "#FFFFFF"
CONTEXT = "#D3D2CC"      # the "all other states" background lines
SHADE = "#F0EFEC"        # recession bands

# Focus states, in a fixed order. Each state keeps its color on every chart.
# Categorical palette validated for colorblind separation (adjacent pairs).
FOCUS_STATES = ["CA", "MA", "AZ", "FL", "MN", "TN"]
STATE_COLORS = {
    "CA": "#2A78D6",  # blue
    "MA": "#EB6834",  # orange
    "AZ": "#1BAF7A",  # aqua
    "FL": "#EDA100",  # yellow
    "MN": "#E87BA4",  # magenta
    "TN": "#008300",  # green
}

# Single-series charts use the first slot; diverging maps use blue <-> red.
PRIMARY = "#2A78D6"
SECONDARY = "#EB6834"
DIVERGING_CMAP = "RdBu_r"

# NBER recessions inside the panel window (annual resolution)
RECESSIONS = [(2001.2, 2001.9), (2007.9, 2009.5), (2020.1, 2020.3)]

# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------
STATE_NAMES = {
    "AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "IA": "Iowa",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland",
    "ME": "Maine", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri",
    "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina",
    "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NV": "Nevada", "NY": "New York",
    "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia",
    "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin",
    "WV": "West Virginia", "WY": "Wyoming",
}

VAR_LABELS = {
    "effective_min_wage": "Minimum wage ($/hr)",
    "pct_unemployed": "Unemployment rate (%)",
    "pct_poverty": "Poverty rate (%)",
    "median_income": "Median household income ($)",
}

SOURCE_FRED = "Source: FRED (BLS, DOL, Census SAIPE). 50 states, 1995-2024."


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------
def apply_style():
    """Set the project-wide matplotlib/seaborn theme."""
    sns.set_theme(style="white", context="notebook")
    plt.rcParams.update({
        "figure.figsize": (10, 5.5),
        "figure.dpi": 110,
        "figure.facecolor": SURFACE,
        "savefig.dpi": 200,
        "savefig.facecolor": SURFACE,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.25,

        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "text.color": INK,

        "axes.facecolor": SURFACE,
        "axes.edgecolor": BASELINE,
        "axes.linewidth": 1.0,
        "axes.labelcolor": INK_SECONDARY,
        "axes.labelsize": 11,
        "axes.labelpad": 8,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "grid.linestyle": "-",

        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "xtick.labelcolor": INK_MUTED,
        "ytick.labelcolor": INK_MUTED,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.major.size": 4,
        "ytick.major.size": 0,

        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",

        "legend.frameon": False,
        "legend.fontsize": 10,
        "legend.labelcolor": INK_SECONDARY,
    })


# ---------------------------------------------------------------------------
# Figure helpers
# ---------------------------------------------------------------------------
def titles(fig, title, subtitle=None, legend=False):
    """Headline (the takeaway) + subtitle (what is plotted), left-aligned above the plot.

    Anchored to the top of the plot area in points, so spacing is identical on
    every chart regardless of figure height. Pass legend=True when a legend_row()
    or panel titles sit between the subtitle and the plot.
    """
    top = fig.subplotpars.top
    gap = 34 if legend else 12
    sub_at = transforms.offset_copy(fig.transFigure, fig=fig, y=gap, units="points")
    title_at = transforms.offset_copy(fig.transFigure, fig=fig, y=gap + (20 if subtitle else 0),
                                      units="points")
    fig.text(0.0, top, title, transform=title_at, ha="left", va="bottom",
             fontsize=15, fontweight="bold", color=INK)
    if subtitle:
        fig.text(0.0, top, subtitle, transform=sub_at, ha="left", va="bottom",
                 fontsize=11, color=INK_SECONDARY)


def source_note(fig, text=SOURCE_FRED):
    """Small source line under the plot area."""
    fig.text(0.0, -0.02, text, ha="left", va="top", fontsize=9, color=INK_MUTED)


def legend_row(ax, ncol=None, **kwargs):
    """Single-row legend above the plot, in place of a boxed legend inside the data."""
    handles, labels = ax.get_legend_handles_labels()
    return ax.legend(handles, labels, loc="lower left", bbox_to_anchor=(0, 1.0),
                     ncol=ncol or len(labels), handlelength=1.6, columnspacing=1.4,
                     borderaxespad=0.4, **kwargs)


def shade_recessions(ax, label=True):
    """Light bands for national recessions - context for the unemployment charts."""
    for start, end in RECESSIONS:
        ax.axvspan(start, end, color=SHADE, zorder=0, lw=0)
    if label:
        ymax = ax.get_ylim()[1]
        for start, end in RECESSIONS:
            ax.text((start + end) / 2, ymax, "Recession", ha="center", va="top",
                    fontsize=8, color=INK_MUTED)


def year_axis(ax, start=1995, end=2024, step=5):
    ax.set_xlim(start - 0.5, end + 0.5)
    ax.set_xticks(range(start, end + 1, step))


def save_fig(fig, name):
    """Export to figures/<name>.png at the project's standard resolution."""
    FIG_DIR.mkdir(exist_ok=True)
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path)
    return path


__all__ = [
    "apply_style", "titles", "source_note", "legend_row", "shade_recessions",
    "year_axis", "save_fig",
    "INK", "INK_SECONDARY", "INK_MUTED", "GRID", "BASELINE", "CONTEXT", "SHADE",
    "PRIMARY", "SECONDARY", "DIVERGING_CMAP",
    "FOCUS_STATES", "STATE_COLORS", "STATE_NAMES", "VAR_LABELS", "SOURCE_FRED",
]
