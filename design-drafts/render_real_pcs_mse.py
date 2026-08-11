"""Render the real-data PCS-MSE website visual and its local zoom.

The source table is the case-level discordance export for the IID-sample split.
The main panel preserves the measured coordinates. The zoom separates overlapping
PCS=0 points for visual inspection.
"""

from __future__ import annotations

import argparse
import json
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
    "font.size": 10,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

INK = "#14231d"
MUTED = "#66766f"
GRID = "#d5dfda"
POINT = "#516a78"
CORAL = "#b65349"
CORAL_SOFT = "#f8e3df"
WHITE = "#ffffff"

FAMILY_MARKERS = {
    "LR": "o",
    "MLP": "s",
    "baseMean": "^",
    "CPA": "D",
    "chemCPA": "v",
    "biolord": "P",
    "cycleCDR": "X",
    "MAP": "*",
    "STATE-ST": "<",
    "PRnet": ">",
    "PrePR-CT": "h",
    "XPert": "p",
    "PerturbDiff": "8",
    "Squidiff": "d",
}


def style_axis(ax, label_size=9):
    ax.tick_params(colors=MUTED, labelsize=label_size, length=3)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.grid(color=GRID, linewidth=0.7, alpha=0.72)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(GRID)


def save(fig, path: Path, dpi=220):
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight", facecolor=WHITE)
    fig.savefig(path.with_suffix(".png"), dpi=dpi, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)


def load_source(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data = data.loc[data["expression_metric"].eq("MSE")].copy()
    data = data.dropna(subset=["expression_score", "PCS", "model_id"])
    if data.empty:
        raise ValueError("The source table has no complete MSE rows.")
    return data


def render_main(data: pd.DataFrame, out_dir: Path, threshold: float, pcs_threshold: float):
    # The page supplies the declarative heading; keep the exported chart focused
    # on the measured relationship, threshold region and model-family encoding.
    fig = plt.figure(figsize=(10.2, 5.95), facecolor=WHITE)
    ax = fig.add_axes([0.105, 0.24, 0.84, 0.68])

    ax.axvspan(threshold, 1.0, color=CORAL_SOFT, alpha=0.60, zorder=0)
    ax.axhspan(-0.02, 0.018, color=CORAL_SOFT, alpha=0.60, zorder=0)
    ax.axvline(threshold, color=CORAL, linewidth=1.1, linestyle=(0, (3, 3)), zorder=1)
    ax.axhline(pcs_threshold, color=CORAL, linewidth=1.1, linestyle=(0, (3, 3)), zorder=1)

    for family, marker in FAMILY_MARKERS.items():
        subset = data.loc[(data["model_id"] == family) & ~data["is_discordant"].astype(bool)]
        if subset.empty:
            continue
        ax.scatter(subset["expression_score"], subset["PCS"], s=21, marker=marker,
                   color=POINT, alpha=0.38, edgecolor="none", zorder=2)

    highlighted = data.loc[data["is_discordant"].astype(bool)]
    ax.scatter(highlighted["expression_score"], highlighted["PCS"], s=28, marker="o",
               color=CORAL, alpha=0.80, edgecolor=WHITE, linewidth=0.25, zorder=4)

    ax.text(threshold + 0.012, 0.975, "expression threshold", color=CORAL,
            fontsize=10.5, rotation=90, ha="left", va="top")
    ax.text(threshold + 0.012, 0.022, "local focus", color=CORAL,
            fontsize=10.5, ha="left", va="bottom")
    ax.set(xlim=(0, 1.02), ylim=(-0.02, 1.02),
           xlabel="Similarity-based score (MSE)", ylabel="Mechanism Fidelity Score (PCS)")
    ax.xaxis.label.set_size(12.5)
    ax.yaxis.label.set_size(12.5)
    style_axis(ax, label_size=10.5)

    handles = [Line2D([0], [0], marker=marker, linestyle="None", markersize=5,
                      markerfacecolor=POINT, markeredgecolor="none", alpha=0.82,
                      label=family) for family, marker in FAMILY_MARKERS.items()
               if (data["model_id"] == family).any()]
    fig.legend(handles=handles, title="Model family", ncol=7, loc="lower center",
               bbox_to_anchor=(0.5, 0.015), fontsize=9.5, title_fontsize=10.5,
               handletextpad=0.45, columnspacing=1.0, borderpad=0)

    save(fig, out_dir / "pcs-mse-main")


def render_zoom(data: pd.DataFrame, out_dir: Path, threshold: float):
    highlighted = data.loc[data["is_discordant"].astype(bool)].copy()
    rng = np.random.default_rng(17)
    highlighted["display_pcs"] = rng.uniform(0.003, 0.058, len(highlighted))

    fig = plt.figure(figsize=(4.3, 3.25), facecolor=WHITE)
    ax = fig.add_axes([0.19, 0.24, 0.75, 0.62])
    ax.axvspan(threshold, 1.0, color=CORAL_SOFT, alpha=0.50, zorder=0)
    ax.axvline(threshold, color=CORAL, linewidth=1.0, linestyle=(0, (3, 3)), zorder=1)
    ax.scatter(highlighted["expression_score"], highlighted["display_pcs"], s=23,
               color=CORAL, alpha=0.75, edgecolor=WHITE, linewidth=0.25, zorder=2)
    ax.set(xlim=(threshold - 0.01, 1.0), ylim=(0, 0.06),
           xlabel="Expression score", ylabel="PCS")
    ax.set_xticks([0.80, 0.85, 0.90, 0.95, 1.00])
    ax.set_yticks([0.00, 0.03, 0.06])
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    style_axis(ax, label_size=12.5)
    ax.tick_params(length=2)
    ax.text(0.01, 1.05, "LOCAL VIEW", transform=ax.transAxes, color=CORAL,
            fontsize=12, fontweight="bold", va="bottom")
    save(fig, out_dir / "pcs-mse-zoom", dpi=240)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("assets"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    data = load_source(args.data)
    threshold = float(data["expression_threshold_q80"].dropna().iloc[0])
    pcs_threshold = float(data["pcs_threshold_q20"].dropna().iloc[0])
    render_main(data, args.out_dir, threshold, pcs_threshold)
    render_zoom(data, args.out_dir, threshold)

    summary = {
        "split": str(data["split_type"].iloc[0]),
        "expression_metric": "MSE",
        "complete_rows": int(len(data)),
        "high_expression_rows": int(data["is_high_expression"].astype(bool).sum()),
        "discordant_rows": int(data["is_discordant"].astype(bool).sum()),
        "discordance_rate": float(data["is_discordant"].astype(bool).sum() /
                                   data["is_high_expression"].astype(bool).sum()),
        "discordance_rate_all_complete_rows": float(data["is_discordant"].astype(bool).mean()),
        "expression_threshold": threshold,
        "pcs_threshold": pcs_threshold,
        "model_families": sorted(data["model_id"].dropna().unique().tolist()),
        "source_note": "Zoom display separates overlapping PCS=0 cases for visual inspection.",
    }
    (args.out_dir / "pcs-mse-summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
