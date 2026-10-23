#!/usr/bin/env python3
"""Generate the three publication figures for the HA-Expert preprint.

All numbers are taken from eval/results/s6-full-report.md (S6 run,
bench v3 keys). Palette: Okabe--Ito colorblind-safe, with one consistent
color per configuration across Figures 2 and 3.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

CONFIGS = ["Base", "DAPT+SFT", "Base+RAG", "DAPT+SFT+RAG"]
COLORS = {
    "Base": "#999999",          # grey
    "DAPT+SFT": "#E69F00",      # orange
    "Base+RAG": "#0072B2",      # blue
    "DAPT+SFT+RAG": "#009E73",  # bluish green
}
EDGE = "#333333"

OVERALL = [0.300, 0.601, 0.710, 0.662]
BY_TYPE = {  # MCQ / Quantitative / Open / Trap
    "Base":         [0.800, 0.250, 0.282, 0.267],
    "DAPT+SFT":     [0.900, 0.300, 0.631, 0.500],
    "Base+RAG":     [0.900, 0.450, 0.719, 0.867],
    "DAPT+SFT+RAG": [0.700, 0.550, 0.676, 0.633],
}
TYPES = ["MCQ\n(n=10)", "Quantitative\n(n=20)", "Open\n(n=195)", "Trap\n(n=15)"]
REPETITION = [10, 35, 7, 22]  # heavy repetition, per 240 responses

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": EDGE,
    "axes.linewidth": 0.8,
    "xtick.color": EDGE,
    "ytick.color": EDGE,
    "text.color": EDGE,
    "axes.labelcolor": EDGE,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight")
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- Figure 1
def fig1():
    # Designed 10in wide, printed at \textwidth (~6.5in): scale 0.65,
    # so 12pt design text -> ~8pt in print.
    fig, ax = plt.subplots(figsize=(10.0, 5.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 58)
    ax.axis("off")

    lanes = [  # (y_bottom, height, label, facecolor)
        (40.5, 16.0, "Training", "#FDF3E0"),
        (21.0, 16.0, "Retrieval", "#E8F1F8"),
        (1.5, 16.0, "Evaluation", "#EAF5F0"),
    ]
    for yb, h, label, fc in lanes:
        ax.add_patch(FancyBboxPatch((0.3, yb), 99.4, h,
                                    boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=fc, ec="#BBBBBB", lw=0.8, zorder=0))
        ax.text(1.8, yb + h - 2.3, label, fontsize=13, fontweight="bold",
                va="center", ha="left", color="#555555")

    def box(x, cy, w, title, sub="", fc="white", bold=False, tc=EDGE,
            h=10.0, sfs=10.5):
        y = cy - h / 2
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0,rounding_size=1.0",
                                    fc=fc, ec=EDGE, lw=1.1, zorder=3))
        cx = x + w / 2
        if sub and "\n" in sub:
            ax.text(cx, cy + 2.9, title, fontsize=12,
                    fontweight="bold" if bold else "normal",
                    va="center", ha="center", zorder=4, color=tc)
            ax.text(cx, cy - 2.1, sub, fontsize=sfs, linespacing=1.5,
                    va="center", ha="center", zorder=4, color=tc)
        elif sub:
            ax.text(cx, cy + 1.9, title, fontsize=12,
                    fontweight="bold" if bold else "normal",
                    va="center", ha="center", zorder=4, color=tc)
            ax.text(cx, cy - 2.4, sub, fontsize=sfs,
                    va="center", ha="center", zorder=4, color=tc)
        else:
            ax.text(cx, cy, title, fontsize=12,
                    fontweight="bold" if bold else "normal",
                    va="center", ha="center", zorder=4, color=tc)

    def arrow(x1, y1, x2, y2, color=EDGE):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="-|>", mutation_scale=16,
                                     lw=1.4, color=color, zorder=2,
                                     shrinkA=0, shrinkB=0))

    # --- Training lane (box centre y = 45.7)
    cy = 45.7
    box(2.0, cy, 16.0, "Corpus", "12,306 papers\n~126M tokens")
    box(20.5, cy, 13.0, "Tokenize", "seq. len 4,096", sfs=9.5)
    box(36.0, cy, 17.0, "DAPT", "Qwen3-8B-Base\n212 steps")
    box(55.5, cy, 16.5, "SFT data", "self-generated\n12,003 QA pairs")
    box(74.5, cy, 10.0, "SFT", "752 steps")
    box(86.5, cy, 12.5, "HA-Expert", "model", fc="#0072B2", bold=True, tc="white")
    for x1, x2 in [(18.0, 20.5), (33.5, 36.0), (53.0, 55.5),
                   (72.0, 74.5), (84.5, 86.5)]:
        arrow(x1, cy, x2, cy)

    # --- Retrieval lane (box centre y = 26.2)
    ry = 26.2
    box(2.0, ry, 16.0, "Text chunks", "~900 chars")
    box(20.5, ry, 22.0, "Embedding", "Qwen3-Embedding-0.6B\n1,024-dim vectors",
        sfs=9.5)
    box(45.0, ry, 18.0, "FAISS index", "636,959 passages")
    box(65.5, ry, 17.0, "Top-4 retrieval", "at inference")
    for x1, x2 in [(18.0, 20.5), (42.5, 45.0), (63.0, 65.5)]:
        arrow(x1, ry, x2, ry)
    # corpus feeds the retrieval lane
    arrow(10.0, cy - 5.0, 10.0, ry + 5.0, color="#0072B2")
    ax.text(11.4, 38.8, "same corpus", fontsize=10.5, color="#0072B2",
            va="center")
    # retrieval feeds the model (RAG on/off)
    arrow(82.5, ry + 1.5, 90.0, cy - 5.0, color="#0072B2")
    ax.text(89.8, 35.8, "RAG on/off", fontsize=10.5, color="#0072B2",
            ha="center", va="center", rotation=52)

    # --- Evaluation lane (box centre y = 6.7)
    ey = 6.7
    box(2.0, ey, 23.0, "HA-Expert-Bench", "240 evidence-checked\nquestions")
    box(28.0, ey, 31.0, "4 configurations",
        "Base / DAPT+SFT\nBase+RAG / DAPT+SFT+RAG")
    box(66.0, ey, 21.0, "Scores", "0.300 · 0.601\n0.710 · 0.662")
    arrow(25.0, ey, 28.0, ey)
    arrow(59.0, ey, 66.0, ey)
    # model is evaluated in the four cells
    arrow(94.5, cy - 5.0, 76.5, ey + 5.0, color="#009E73")
    ax.text(80.2, 18.6, "evaluate", fontsize=10.5, color="#009E73",
            ha="center", va="center", rotation=-63)

    save(fig, "fig1-pipeline")


# ---------------------------------------------------------------- Figure 2
def fig2():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.3),
                             gridspec_kw={"width_ratios": [1, 1.9], "wspace": 0.22})
    # (a) overall
    ax = axes[0]
    bars = ax.bar(range(4), OVERALL,
                  color=[COLORS[c] for c in CONFIGS],
                  edgecolor=EDGE, linewidth=0.8, width=0.68)
    for b, v in zip(bars, OVERALL):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.3f}",
                ha="center", va="bottom", fontsize=12)
    ax.set_xticks(range(4))
    ax.set_xticklabels(["Base", "DAPT+SFT", "Base+RAG", "DAPT+SFT\n+RAG"],
                       fontsize=10.5)
    ax.set_ylim(0, 0.82)
    ax.set_ylabel("Accuracy", fontsize=13)
    ax.set_title("(a) Overall accuracy", fontsize=13.5, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    # (b) by question type
    ax = axes[1]
    x = np.arange(len(TYPES))
    w = 0.19
    for i, cfg in enumerate(CONFIGS):
        ax.bar(x + (i - 1.5) * w, BY_TYPE[cfg], width=w, label=cfg,
               color=COLORS[cfg], edgecolor=EDGE, linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(TYPES, fontsize=11.5)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Accuracy", fontsize=13)
    ax.set_title("(b) Accuracy by question type", fontsize=13.5, loc="left",
                 pad=64)
    ax.legend(fontsize=11, frameon=False, ncol=2, loc="lower left",
              bbox_to_anchor=(0.0, 1.01))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    save(fig, "fig2-results")


# ---------------------------------------------------------------- Figure 3
def fig3():
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    bars = ax.bar(CONFIGS, REPETITION,
                  color=[COLORS[c] for c in CONFIGS],
                  edgecolor=EDGE, linewidth=0.8, width=0.58)
    for b, v in zip(bars, REPETITION):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.8, str(v),
                ha="center", va="bottom", fontsize=12)
    ax.annotate("+ 5 citation-marker loops",
                xy=(3, 22), xytext=(1.55, 30.5),
                fontsize=11.5, color="#009E73",
                arrowprops=dict(arrowstyle="->", color="#009E73", lw=1.2))
    ax.set_ylim(0, 40)
    ax.set_ylabel("Responses with heavy repetition\n(per 240 responses)",
                  fontsize=12)
    ax.tick_params(axis="x", labelsize=10.5)
    for lbl in ax.get_xticklabels():
        lbl.set_text(lbl.get_text().replace("DAPT+SFT+RAG", "DAPT+SFT\n+RAG"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    save(fig, "fig3-failure-modes")


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
