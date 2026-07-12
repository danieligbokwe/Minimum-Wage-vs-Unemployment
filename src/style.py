import matplotlib.pyplot as plt
import seaborn as sns

PALETTE = {
    "primary": "#1F3864",    # dark navy — headline series, key lines
    "secondary": "#2E5395",  # medium blue — comparison series
    "neutral": "#BFBFBF",    # gray — non-highlighted states, gridlines
    "accent": "#C00000",     # red — the one thing you want the eye to land on
}

def set_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "axes.edgecolor": PALETTE["neutral"],
        "axes.labelcolor": "#333333",
        "text.color": "#333333",
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "font.size": 11,
        "axes.titleweight": "bold",
        "axes.titlecolor": PALETTE["primary"],
    })