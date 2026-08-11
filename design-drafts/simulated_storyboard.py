from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
mpl.rcParams.update({
    "font.size": 11,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "source-data"
DATA.mkdir(exist_ok=True)

INK = "#14231d"
MUTED = "#66766f"
LINE = "#d5dfda"
BLUE = "#2459b8"
BLUE_SOFT = "#dfe9fb"
GREEN = "#0d7757"
GREEN_SOFT = "#dcefe7"
CORAL = "#b65349"
CORAL_SOFT = "#f8e3df"
AMBER = "#a56a00"
AMBER_SOFT = "#fff0cc"
BG = "#ffffff"


def style_axis(ax):
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.grid(color=LINE, linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(LINE)


def add_draft_label(fig, y=0.935):
    fig.text(0.985, y, "SIMULATED DATA  |  CONCEPT DRAFT", ha="right", va="top",
             fontsize=8, color=CORAL, fontweight="bold")


def save(fig, stem):
    fig.savefig(ROOT / f"{stem}.svg", bbox_inches="tight", facecolor=BG)
    fig.savefig(ROOT / f"{stem}.png", dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def complementary_metrics():
    rng = np.random.default_rng(22)
    n, n_high = 683, 399
    families = ["LR", "MLP", "baseMean", "CPA", "chemCPA", "biolord", "cycleCDR",
                "MAP", "STATE-ST", "PRnet", "PrePR-CT", "XPert", "PerturbDiff", "Squidiff"]
    markers = ["o", "s", "^", "D", "v", "P", "X", "*", "<", ">", "h", "p", "8", "d"]

    # The highlighted region is generated first so its count matches the reference
    # composition (399 of 683 cases) while all values remain explicitly synthetic.
    mse_high = 0.78 + 0.19 * rng.beta(3.2, 2.0, n_high)
    pcs_high = 0.06 * rng.beta(1.3, 2.2, n_high)
    n_other = n - n_high
    mse_other = np.clip(rng.beta(3.0, 2.3, n_other), 0.02, 0.98)
    pcs_other = np.clip(rng.choice([0.0, 0.25, 0.5, 0.75, 1.0], size=n_other,
                                   p=[0.16, 0.19, 0.26, 0.18, 0.21])
                        + rng.normal(0, 0.018, n_other), 0.0, 1.0)
    # Keep non-highlighted low-PCS cases outside the high-MSE quadrant.
    low_non = pcs_other <= 0.06
    mse_other[low_non] = np.minimum(mse_other[low_non], 0.75)
    mse = np.concatenate([mse_high, mse_other])
    pcs = np.concatenate([pcs_high, pcs_other])
    highlighted = np.concatenate([np.ones(n_high, dtype=bool), np.zeros(n_other, dtype=bool)])
    family = rng.choice(families, size=n, replace=True)
    data = pd.DataFrame({"mse_similarity_score": mse, "pcs": pcs,
                         "model_family": family, "highlighted": highlighted})
    data.to_csv(DATA / "claim-1-simulated-cases.csv", index=False)

    fig = plt.figure(figsize=(12, 6.8), facecolor=BG)
    ax = fig.add_axes([0.085, 0.17, 0.58, 0.68])
    ax.axvspan(0.78, 1.0, color=CORAL_SOFT, alpha=0.68, zorder=0)
    ax.axhline(0.06, color=CORAL, linewidth=1.1, linestyle=(0, (3, 3)), zorder=1)
    ax.axvline(0.78, color=CORAL, linewidth=1.1, linestyle=(0, (3, 3)), zorder=1)

    for fam, marker in zip(families, markers):
        mask = (family == fam) & ~highlighted
        ax.scatter(mse[mask], pcs[mask], s=22, marker=marker, color="#516a78",
                   alpha=0.42, linewidths=0, zorder=2)
        mask_hi = (family == fam) & highlighted
        ax.scatter(mse[mask_hi], pcs[mask_hi], s=28, marker=marker, color=CORAL,
                   alpha=0.78, edgecolor="white", linewidths=0.25, zorder=3)

    ax.text(0.78, 0.975, "PCS threshold", color=CORAL, fontsize=8.5,
            ha="left", va="top", rotation=90)
    ax.text(0.79, 0.02, "MSE threshold", color=CORAL, fontsize=8.5,
            ha="left", va="bottom")
    ax.set(xlim=(0, 1.02), ylim=(-0.02, 1.02),
           xlabel="Similarity-based score (MSE)", ylabel="Mechanism Fidelity Score (PCS)")
    style_axis(ax)
    ax.tick_params(labelsize=8.5)

    # A clean zoom makes the high-MSE / low-PCS cluster inspectable without
    # duplicating the full three-panel manuscript layout.
    zoom = fig.add_axes([0.715, 0.32, 0.245, 0.20])
    zoom.scatter(mse[highlighted], pcs[highlighted], s=18, color=CORAL,
                 alpha=0.72, edgecolor="white", linewidths=0.25)
    zoom.set(xlim=(0.78, 0.98), ylim=(0, 0.06),
             xticks=[0.78, 0.88, 0.98], yticks=[0.00, 0.03, 0.06])
    zoom.tick_params(labelsize=6, colors=MUTED, length=2)
    zoom.grid(color=LINE, linewidth=0.55, alpha=0.8)
    zoom.set_axisbelow(True)
    for spine in zoom.spines.values():
        spine.set_color(CORAL)
        spine.set_linewidth(0.85)
    zoom.text(0.01, 1.04, "zoom", transform=zoom.transAxes, color=CORAL,
              fontsize=7.5, fontweight="bold", va="bottom")

    fig.text(0.715, 0.77, "Expression-like,\nmechanism-low", color=CORAL,
             fontsize=18, fontweight="bold", va="top", linespacing=1.05)
    fig.text(0.715, 0.655, f"{n_high}/{n} cases", color=INK, fontsize=16,
             fontweight="bold", va="top")
    fig.text(0.715, 0.60, f"({n_high / n:.1%})", color=MUTED, fontsize=12, va="top")
    legend_ax = fig.add_axes([0.70, 0.12, 0.28, 0.17])
    legend_ax.set_axis_off()
    handles = [Line2D([0], [0], marker=marker, linestyle="None", markersize=4.8,
                      markerfacecolor="#516a78", markeredgecolor="none", alpha=0.8,
                      label=fam) for fam, marker in zip(families, markers)]
    legend_ax.legend(handles=handles, title="Model family", ncol=2, loc="upper left",
                     frameon=False, fontsize=7.1, title_fontsize=8,
                     handletextpad=0.45, columnspacing=0.9, borderpad=0)

    fig.suptitle("High expression similarity can mask mechanism failure",
                 x=0.055, y=0.98, ha="left", fontsize=22, fontweight="bold", color=INK)
    fig.text(0.985, 0.91, "SIMULATED DATA  |  CONCEPT DRAFT", ha="right", va="top",
             fontsize=8, color=CORAL, fontweight="bold")
    fig.text(0.085, 0.075, "Each point = one evaluated perturbation case · thresholds are illustrative",
             color=MUTED, fontsize=8.5, ha="left")
    save(fig, "claim-1-complementary-metrics")


def ranking_shift():
    models = [f"Model {c}" for c in "ABCDEFGHIJKL"]
    ess = np.array([0.91, 0.89, 0.87, 0.85, 0.84, 0.82, 0.81, 0.80, 0.79, 0.77, 0.75, 0.73])
    mfs = np.array([0.24, 0.31, 0.28, 0.40, 0.37, 0.26, 0.51, 0.34, 0.45, 0.30, 0.39, 0.22])
    df = pd.DataFrame({"model": models, "ESS": ess, "MFS": mfs})
    df["ESS_rank"] = df["ESS"].rank(ascending=False, method="first").astype(int)
    df["MFS_rank"] = df["MFS"].rank(ascending=False, method="first").astype(int)
    df.to_csv(DATA / "claim-2-simulated-model-ranks.csv", index=False)
    rho = df[["ESS_rank", "MFS_rank"]].corr(method="spearman").iloc[0, 1]

    fig, ax = plt.subplots(figsize=(12, 6.4), facecolor=BG)
    ax.set_xlim(-0.28, 1.28); ax.set_ylim(12.8, 0.2); ax.set_axis_off()
    ax.axvline(0, color=LINE, lw=1); ax.axvline(1, color=LINE, lw=1)
    ess_winner = df.loc[df.ESS_rank.idxmin(), "model"]
    mfs_winner = df.loc[df.MFS_rank.idxmin(), "model"]
    for _, row in df.iterrows():
        color, lw, alpha = (MUTED, 1.2, 0.46)
        if row.model == ess_winner: color, lw, alpha = (BLUE, 3.2, 1)
        if row.model == mfs_winner: color, lw, alpha = (GREEN, 3.2, 1)
        ax.plot([0, 1], [row.ESS_rank, row.MFS_rank], color=color, lw=lw, alpha=alpha, zorder=1)
        ax.scatter([0, 1], [row.ESS_rank, row.MFS_rank], s=38 if lw < 2 else 90,
                   color=color, edgecolor="white", linewidth=0.8, zorder=3)
        ax.text(-0.035, row.ESS_rank, row.model, ha="right", va="center", fontsize=9,
                color=color if lw > 2 else INK, fontweight="bold" if lw > 2 else "normal")
        ax.text(1.035, row.MFS_rank, row.model, ha="left", va="center", fontsize=9,
                color=color if lw > 2 else INK, fontweight="bold" if lw > 2 else "normal")
    ax.text(0, -0.02, "Ranked by reconstruction", transform=ax.transAxes, ha="left", va="bottom", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(1, -0.02, "Ranked by mechanism fidelity", transform=ax.transAxes, ha="right", va="bottom", color=GREEN, fontsize=13, fontweight="bold")
    ax.text(0.5, 0.93, "Top-3 overlap: 0 / 3", transform=ax.transAxes, ha="center", va="top", fontsize=18, color=CORAL, fontweight="bold")
    ax.text(0.5, 0.86, f"Rank correlation: {rho:.2f}", transform=ax.transAxes, ha="center", va="top", fontsize=10, color=MUTED)
    ax.text(0.5, 0.08, "A reconstruction-only leaderboard can select a different winner",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=12, color=INK, fontweight="bold")
    fig.suptitle("The evaluation target changes which model appears best", x=0.06, y=1.01,
                 ha="left", fontsize=22, fontweight="bold", color=INK)
    add_draft_label(fig, y=0.985)
    save(fig, "claim-2-ranking-shift")


def mechanism_failure():
    models = [f"Model {c}" for c in "ABCDEFGHIJKL"]
    ess = np.array([0.91, 0.89, 0.87, 0.85, 0.84, 0.82, 0.81, 0.80, 0.79, 0.77, 0.75, 0.73])
    mfs = np.array([0.24, 0.31, 0.28, 0.40, 0.37, 0.26, 0.51, 0.34, 0.45, 0.30, 0.39, 0.22])
    failures = pd.Series({
        "Signature specificity": 0.91,
        "Generic response": 0.74,
        "Global strength": 0.55,
        "Magnitude mismatch": 0.49,
        "Direction failure": 0.43,
    })
    pd.DataFrame({"model": models, "ESS": ess, "MFS": mfs}).to_csv(DATA / "claim-3-simulated-model-scores.csv", index=False)
    failures.rename("prevalence").to_csv(DATA / "claim-3-simulated-failure-modes.csv")

    fig = plt.figure(figsize=(12, 6.4), facecolor=BG)
    fig.subplots_adjust(top=0.84)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 0.85], wspace=0.28)
    ax = fig.add_subplot(gs[0, 0])
    y = np.arange(len(models))
    for yi, e, m in zip(y, ess, mfs):
        ax.plot([m, e], [yi, yi], color=LINE, lw=2, zorder=1)
    ax.scatter(ess, y, s=64, color=BLUE, label="Expression reconstruction", zorder=3)
    ax.scatter(mfs, y, s=64, color=GREEN, label="Mechanism fidelity", zorder=3)
    ax.set_yticks(y, models); ax.invert_yaxis(); ax.set_xlim(0, 1)
    ax.set_xlabel("Normalized score (illustrative)")
    ax.legend(loc="lower right", ncol=2, fontsize=9)
    style_axis(ax)
    ax.grid(axis="x", color=LINE, linewidth=0.7); ax.grid(axis="y", visible=False)
    ax.set_title("High reconstruction can coexist with low MFS", loc="left", fontsize=14, fontweight="bold", color=INK, pad=14)

    bx = fig.add_subplot(gs[0, 1])
    vals = failures.values[::-1]; labels = failures.index[::-1]
    colors = [CORAL if value >= 0.7 else AMBER for value in vals]
    bars = bx.barh(np.arange(len(labels)), vals, color=colors, height=0.62)
    bx.set_yticks(np.arange(len(labels)), labels); bx.set_xlim(0, 1)
    bx.set_xlabel("Fraction of cases (illustrative)")
    for bar, value in zip(bars, vals):
        bx.text(value + 0.02, bar.get_y() + bar.get_height() / 2, f"{value:.0%}", va="center", fontsize=9, color=INK)
    style_axis(bx)
    bx.grid(axis="x", color=LINE, linewidth=0.7); bx.grid(axis="y", visible=False)
    bx.set_title("Failure modes remain common", loc="left", fontsize=14, fontweight="bold", color=INK, pad=14)
    fig.suptitle("Current models reconstruct expression better than they recover mechanism",
                 x=0.06, y=1.01, ha="left", fontsize=22, fontweight="bold", color=INK)
    add_draft_label(fig, y=0.93)
    save(fig, "claim-3-mechanism-failure")


if __name__ == "__main__":
    complementary_metrics()
    ranking_shift()
    mechanism_failure()
