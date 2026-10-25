#!/usr/bin/env python3
"""Generate the three publication figures for the HA-Expert preprint.

All numbers are taken from eval/results/s6-full-report.md (S6 run,
bench v3 keys). Palette: Okabe--Ito colorblind-safe, with one consistent
color per configuration across Figures 2 and 3.

Typography: figures are designed AT their final print width
(Fig. 1/2: \\textwidth = 6.5in; Fig. 3: 0.85\\textwidth = 5.5in), so
the point sizes below are the printed point sizes (minimum 9pt).
Figure 1 wraps its Training and Retrieval lanes over two rows each so
that every label fits its box at >= 9pt. Exports: vector PDF + PNG at
300 dpi.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, PathPatch
from matplotlib.path import Path
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
})


def save(fig, name, tight=True):
    kw = {"bbox_inches": "tight", "pad_inches": 0.02} if tight else {}
    fig.savefig(os.path.join(OUT, name + ".pdf"), **kw)
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=300, **kw)
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- Figure 1
def fig1():
    # Canvas: 130 x-units = 6.5in wide (20 units/in), 92 units = 4.6in.
    # Box widths were set from measured DejaVu text widths at the sizes
    # used below (titles 10pt bold, subs 9pt) plus 3.2 units of padding,
    # so no label overflows its box.
    fig, ax = plt.subplots(figsize=(6.5, 4.6))
    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    ax.set_xlim(0, 130)
    ax.set_ylim(0, 92)
    ax.axis("off")

    lanes = [  # (y_bottom, y_top, label, facecolor)
        (61.0, 92.0, "Training", "#FDF3E0"),
        (25.0, 57.6, "Retrieval", "#E8F1F8"),
        (1.0, 21.6, "Evaluation", "#EAF5F0"),
    ]
    for yb, yt, label, fc in lanes:
        ax.add_patch(FancyBboxPatch((0.5, yb), 129.0, yt - yb,
                                    boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=fc, ec="#BBBBBB", lw=0.8, zorder=0))
        ax.text(3.5, yt - 2.6, label, fontsize=10.5, fontweight="bold",
                va="center", ha="left", color="#555555", zorder=5)

    def box(x, cy, w, lines, fc="white", tc=EDGE):
        """lines: list of (text, kind); kind 't' = title (10pt bold),
        's' = sub (9pt). Box height grows with the number of lines."""
        nl = len(lines)
        h = 3.0 * nl + 1.8
        ax.add_patch(FancyBboxPatch((x, cy - h / 2), w, h,
                                    boxstyle="round,pad=0,rounding_size=1.0",
                                    fc=fc, ec=EDGE, lw=1.0, zorder=3))
        cx = x + w / 2
        for i, (txt, kind) in enumerate(lines):
            ly = cy + (nl - 1) * 1.55 - i * 3.1
            if kind == "t":
                ax.text(cx, ly, txt, fontsize=10, fontweight="bold",
                        va="center", ha="center", zorder=4, color=tc)
            else:
                ax.text(cx, ly, txt, fontsize=9,
                        va="center", ha="center", zorder=4, color=tc)
        return {"x": x, "w": w, "cx": cx, "cy": cy, "h": h,
                "top": cy + h / 2, "bot": cy - h / 2,
                "left": x, "right": x + w}

    def arrow(x1, y1, x2, y2, color=EDGE):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="-|>", mutation_scale=12,
                                     lw=1.3, color=color, zorder=2,
                                     shrinkA=0, shrinkB=0))

    def elbow(points, color):
        verts = np.array(points, dtype=float)
        codes = [Path.MOVETO] + [Path.LINETO] * (len(points) - 1)
        ax.add_patch(PathPatch(Path(verts, codes), fill=False,
                               lw=1.3, color=color, zorder=2))
        (x1, y1), (x2, y2) = points[-2], points[-1]
        arrow(x1, y1, x2, y2, color=color)

    T, S = "t", "s"
    # --- Training lane: row 1 (cy=81), row 2 (cy=66.8)
    corpus = box(2.0, 81.0, 28.4, [("Corpus", T), ("12,306 papers", S),
                                   ("~126M tokens", S)])
    tok = box(36.4, 81.0, 28.0, [("Tokenize", T), ("seq. len 4,096", S)])
    dapt = box(70.4, 81.0, 30.8, [("DAPT", T), ("Qwen3-8B-Base", S),
                                  ("212 steps", S)])
    sftdata = box(20.0, 66.8, 31.3, [("SFT data", T), ("self-generated", S),
                                     ("12,003 QA pairs", S)])
    sft = box(53.7, 66.8, 20.3, [("SFT", T), ("752 steps", S)])
    model = box(76.4, 66.8, 25.3, [("HA-Expert", T), ("model", S)],
                fc="#0072B2", tc="white")
    arrow(corpus["right"], 81.0, tok["left"], 81.0)
    arrow(tok["right"], 81.0, dapt["left"], 81.0)
    # DAPT -> SFT data: orthogonal elbow through the empty inter-row gap
    elbow([(dapt["cx"], dapt["bot"]), (dapt["cx"], 73.6),
           (sftdata["cx"], 73.6), (sftdata["cx"], sftdata["top"])], EDGE)
    ax.text(60.5, 75.3, "DAPT model generates", fontsize=8.5,
            color="#555555", va="center", ha="center")
    arrow(sftdata["right"], 66.8, sft["left"], 66.8)
    arrow(sft["right"], 66.8, model["left"], 66.8)

    # --- Retrieval lane: single row (cy=40), boxes left to right
    chunks = box(2.0, 40.0, 24.0, [("Text chunks", T), ("~900 chars", S)])
    embed = box(29.0, 40.0, 37.0, [("Embedding", T),
                                   ("Qwen3-Embedding-0.6B", S),
                                   ("1,024-dim vectors", S)])
    faiss = box(69.0, 40.0, 28.0, [("FAISS index", T),
                                   ("636,959 passages", S)])
    top4 = box(100.0, 40.0, 23.0, [("Top-4", T), ("retrieval", T),
                                   ("at inference", S)])
    arrow(chunks["right"], 40.0, embed["left"], 40.0)
    arrow(embed["right"], 40.0, faiss["left"], 40.0)
    arrow(faiss["right"], 40.0, top4["left"], 40.0)
    # corpus feeds the retrieval lane (long vertical at the left)
    arrow(16.35, corpus["bot"], 16.35, chunks["top"], color="#0072B2")
    ax.text(18.6, 59.3, "same corpus", fontsize=9, color="#0072B2",
            va="center", ha="left")
    # retrieval feeds the model (RAG on/off): orthogonal elbow up through
    # the inter-lane gap, then into the model box from below
    elbow([(top4["cx"], top4["top"]), (top4["cx"], 59.3),
           (model["cx"], 59.3), (model["cx"], model["bot"])],
          color="#0072B2")
    ax.text(109.0, 52.0, "RAG on/off", fontsize=9, color="#0072B2",
            va="center", ha="right")

    # --- Evaluation lane (cy=9.5)
    bench = box(2.0, 9.5, 42.5, [("HA-Expert-Bench", T),
                                 ("240 evidence-checked", S),
                                 ("questions", S)])
    configs = box(47.0, 9.5, 38.8, [("4 configurations", T),
                                    ("Base / DAPT+SFT /", S),
                                    ("Base+RAG /", S),
                                    ("DAPT+SFT+RAG", S)])
    scores = box(88.3, 9.5, 26.5, [("Scores", T), ("0.300 · 0.601", S),
                                   ("0.710 · 0.662", S)])
    arrow(bench["right"], 9.5, configs["left"], 9.5)
    arrow(configs["right"], 9.5, scores["left"], 9.5)
    # model is evaluated: orthogonal spine down the far-right margin,
    # along the evaluation lane, and into the Scores box from above
    elbow([(model["right"], model["cy"]), (125.5, model["cy"]),
           (125.5, 17.8), (scores["cx"], 17.8),
           (scores["cx"], scores["top"])], color="#009E73")
    ax.text(113.5, 19.9, "evaluate", fontsize=9, color="#009E73",
            va="center", ha="center")

    save(fig, "fig1-pipeline", tight=False)


# ---------------------------------------------------------------- Figure 2
def fig2():
    # Designed at final print width 6.5in; fonts are true print sizes.
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.6),
                             gridspec_kw={"width_ratios": [1, 1.85],
                                          "wspace": 0.26})
    # (a) overall
    ax = axes[0]
    bars = ax.bar(range(4), OVERALL,
                  color=[COLORS[c] for c in CONFIGS],
                  edgecolor=EDGE, linewidth=0.8, width=0.66, zorder=3)
    for b, v in zip(bars, OVERALL):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.025, f"{v:.3f}",
                ha="center", va="bottom", fontsize=9.5)
    ax.set_xticks(range(4))
    ax.set_xticklabels(["Base", "DAPT+SFT", "Base+RAG", "DAPT+SFT+RAG"],
                       fontsize=9, rotation=30, ha="right")
    ax.set_ylim(0, 0.84)
    ax.set_ylabel("Accuracy", fontsize=10.5)
    ax.set_title("(a) Overall accuracy", fontsize=11.5, loc="left",
                 fontweight="bold", pad=9)
    ax.tick_params(axis="y", labelsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    # (b) by question type, with value labels on every bar
    ax = axes[1]
    x = np.arange(len(TYPES))
    w = 0.19
    for i, cfg in enumerate(CONFIGS):
        bars = ax.bar(x + (i - 1.5) * w, BY_TYPE[cfg], width=w, label=cfg,
                      color=COLORS[cfg], edgecolor=EDGE, linewidth=0.7,
                      zorder=3)
        for b, v in zip(bars, BY_TYPE[cfg]):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}",
                    ha="center", va="bottom", fontsize=8.5, rotation=90)
    ax.set_xticks(x)
    ax.set_xticklabels(TYPES, fontsize=9.5)
    ax.set_ylim(0, 1.13)
    ax.set_ylabel("Accuracy", fontsize=10.5)
    ax.set_title("(b) Accuracy by question type", fontsize=11.5, loc="left",
                 fontweight="bold", pad=9)
    ax.tick_params(axis="y", labelsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#DDDDDD", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center",
               bbox_to_anchor=(0.5, 1.03), ncol=4, frameon=False,
               fontsize=8.6, handlelength=1.1, handleheight=0.9,
               columnspacing=1.0)

    save(fig, "fig2-results")


# ---------------------------------------------------------------- Figure 3
def fig3():
    # Designed at final print width 0.85 * 6.5in = 5.5in.
    fig, ax = plt.subplots(figsize=(5.5, 3.3))
    bars = ax.bar(CONFIGS, REPETITION,
                  color=[COLORS[c] for c in CONFIGS],
                  edgecolor=EDGE, linewidth=0.8, width=0.56, zorder=3)
    for b, v in zip(bars, REPETITION):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.9, str(v),
                ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.annotate("+ 5 citation-marker loops",
                xy=(3, 22), xytext=(1.45, 31.0),
                fontsize=9.5, color="#009E73",
                arrowprops=dict(arrowstyle="->", color="#009E73", lw=1.2))
    ax.set_ylim(0, 40)
    ax.set_ylabel("Responses with heavy repetition\n(per 240 responses)",
                  fontsize=10.5)
    ax.tick_params(axis="x", labelsize=9.5)
    ax.tick_params(axis="y", labelsize=9.5)
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
