#!/usr/bin/env python3
"""Render one benchmark split/metric view as a publication-style raster image."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
from matplotlib.patches import Circle, Polygon
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "design-drafts" / "benchmark-static" / "iid-sample--atomic-pcs.png"
)
DEFAULT_OUTPUT_DIR = ROOT / "design-drafts" / "benchmark-static"

COLORS = [
    "#46504C",
    "#6F8F83",
    "#94ADA3",
    "#BDCBC4",
    "#667C9E",
    "#96A7C4",
    "#90819D",
    "#B39AA7",
    "#B18D72",
    "#C5B482",
]
MEDALS = [
    ("#D4A72C", "#946B13"),
    ("#AEB8C1", "#707B84"),
    ("#B77B55", "#7E4D34"),
]
BASELINE_MODELS = {"LR", "MLP", "baseMean"}
MODELS = [
    "LR",
    "MLP",
    "baseMean",
    "biolord",
    "cycleCDR",
    "chemCPA",
    "PrePR-CT",
    "PerturbDiff",
    "Squidiff",
    "XPert",
    "STATE-ST",
    "PRnet",
    "MAP",
    "LPM",
    "CPA",
]
REPRESENTATIONS = [
    ("raw", "Raw"),
    ("Geneformer", "Geneformer"),
    ("PCA", "PCA"),
    ("State-SE", "State-SE"),
    ("nicheformer", "nicheformer"),
    ("scFoundation", "scFoundation"),
    ("scGPT", "scGPT"),
    ("scimilarity", "scimilarity"),
    ("stack", "stack"),
    ("transcriptformer", "transcriptformer"),
]
METRICS = [
    ("atomic-pcs", "Atomic-level PCS", "Gene Direction Acc", "higher", "mechanism"),
    ("pcs-median", "PCS (median)", "PCS （median）", "higher", "mechanism"),
    ("esr", "ESR", "ESR", "target-one", "mechanism"),
    ("gcs", "GCS", "GCS", "higher", "mechanism"),
    ("mss", "MSS", "MSS", "higher", "mechanism"),
    (
        "pathway-spearman",
        "Pathway Spearman",
        "Pathway Spearman",
        "higher",
        "mechanism",
    ),
    (
        "pathway-sign-accuracy",
        "Pathway Sign Accuracy",
        "Pathway sign accuracy",
        "higher",
        "mechanism",
    ),
    ("mse", "MSE", "MSE", "lower", "similarity"),
    ("e-distance", "E-distance", "E-distance", "lower", "similarity"),
    ("pcc-delta", "PCC-delta", "PCC-delta", "higher", "similarity"),
    ("de-auprc", "DE AUPRC", "DE AUPRC", "higher", "similarity"),
    ("de-f1", "DE F1", "DE F1", "higher", "similarity"),
    (
        "logfc-spearman",
        "logFC Spearman",
        "logFC Spearman",
        "higher",
        "similarity",
    ),
    (
        "distribution-mmd",
        "Distribution MMD",
        "Distribution MMD",
        "lower",
        "similarity",
    ),
]
CELL_LINE_SPLITS = [
    (
        "iid-sample",
        "IID sample",
        "iid-sample",
        "scFM-pertub-cell-line-iid-sample.xlsx",
    ),
    (
        "ood-cell",
        "OOD cell",
        "Results of ood-cell",
        "scFM-pertub-cell-line-ood-cell.xlsx",
    ),
    (
        "ood-drug-cell-pairs",
        "OOD drug-cell pairs",
        "Results of ood-drug-cell-pairs",
        "scFM-pertub-cell-line-ood-drug-cell-pairs.xlsx",
    ),
    (
        "ood-drug",
        "OOD drug",
        "Results of ood-drug",
        "scFM-pertub-cell-line-ood-drug.xlsx",
    ),
    (
        "ood-tissue",
        "OOD tissue",
        "Results of ood-tissue",
        "scFM-pertub-cell-line-ood-tissue.xlsx",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--data",
        type=Path,
        help="Read an external browser-ready benchmark JSON file.",
    )
    source.add_argument(
        "--source-dir",
        type=Path,
        help="Read the cell-line XLSX source bundle directly without writing JSON.",
    )
    parser.add_argument("--split", default="iid-sample")
    parser.add_argument("--metric", default="atomic-pcs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Render every split and metric combination.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Destination used with --all.",
    )
    return parser.parse_args()


def normalize_frame(frame):
    frame = frame.copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    frame = frame.rename(columns={frame.columns[0]: "model"})
    frame["model"] = frame["model"].astype(str).str.strip()
    return frame


def mean_by_model(frame, column):
    values = {}
    for model in MODELS:
        series = pd.to_numeric(
            frame.loc[frame["model"] == model, column], errors="coerce"
        ).dropna()
        values[model] = round(float(series.mean()), 10) if len(series) else None
    return values


def build_cell_line_payload(source_dir: Path):
    raw_path = source_dir / "raw-cell-line-results.xlsx"
    required_paths = [raw_path] + [source_dir / split[3] for split in CELL_LINE_SPLITS]
    missing = [path for path in required_paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing source workbooks: {', '.join(map(str, missing))}")

    payload = {
        "splits": [
            {"id": split_id, "label": split_label}
            for split_id, split_label, _, _ in CELL_LINE_SPLITS
        ],
        "metrics": [
            {
                "id": metric_id,
                "label": metric_label,
                "direction": direction,
                "family": family,
            }
            for metric_id, metric_label, _, direction, family in METRICS
        ],
        "models": MODELS,
        "representations": [
            {"id": representation_id, "label": representation_label}
            for representation_id, representation_label in REPRESENTATIONS
        ],
        "results": {},
        "notes": {
            "aggregation": "mean across available runs",
            "rawOnlyModels": ["baseMean", "PrePR-CT"],
        },
    }

    for split_id, _, raw_sheet, embedding_filename in CELL_LINE_SPLITS:
        raw_frame = normalize_frame(
            pd.read_excel(raw_path, sheet_name=raw_sheet, header=1)
        )
        embedding_path = source_dir / embedding_filename
        workbook = pd.ExcelFile(embedding_path)
        representation_frames = {"raw": raw_frame}
        for representation_id, _ in REPRESENTATIONS[1:]:
            if representation_id not in workbook.sheet_names:
                raise ValueError(
                    f"Missing sheet {representation_id!r} in {embedding_path.name}"
                )
            representation_frames[representation_id] = normalize_frame(
                pd.read_excel(
                    embedding_path,
                    sheet_name=representation_id,
                    header=1,
                )
            )

        split_results = {}
        for metric_id, _, source_column, _, _ in METRICS:
            metric_results = {}
            for representation_id, _ in REPRESENTATIONS:
                frame = representation_frames[representation_id]
                if source_column not in frame.columns:
                    raise ValueError(
                        f"Missing column {source_column!r} in {split_id}/{representation_id}"
                    )
                metric_results[representation_id] = mean_by_model(
                    frame,
                    source_column,
                )
            split_results[metric_id] = metric_results
        payload["results"][split_id] = split_results

    return payload


def rank_combinations(payload, metric, metric_results):
    combinations = []
    for representation_index, representation in enumerate(payload["representations"]):
        values = metric_results[representation["id"]]
        for model_index, model in enumerate(payload["models"]):
            value = values[model]
            if value is not None:
                combinations.append(
                    {
                        "model": model,
                        "model_index": model_index,
                        "representation": representation["label"],
                        "representation_index": representation_index,
                        "value": value,
                    }
                )

    if metric["direction"] == "target-one":
        key = lambda item: abs(item["value"] - 1)
    elif metric["direction"] == "higher":
        key = lambda item: -item["value"]
    else:
        key = lambda item: item["value"]
    return sorted(combinations, key=key)[:5]


def format_value(value: float) -> str:
    absolute = abs(value)
    if (0 < absolute < 0.001) or absolute >= 1000:
        return f"{value:.3e}"
    return f"{value:.5g}"


def add_medal(ax, x, y, rank):
    fill, edge = MEDALS[rank]
    drawing = DrawingArea(12, 14, 0, 0)
    drawing.add_artist(
        Polygon(
            [[2.0, 13.5], [5.0, 7.0], [6.0, 5.7]],
            closed=True,
            facecolor="#3F806A",
            edgecolor="none",
        )
    )
    drawing.add_artist(
        Polygon(
            [[10.0, 13.5], [7.0, 7.0], [6.0, 5.7]],
            closed=True,
            facecolor="#3F806A",
            edgecolor="none",
        )
    )
    drawing.add_artist(
        Circle(
            (6.0, 4.8),
            radius=3.8,
            facecolor=fill,
            edgecolor=edge,
            linewidth=0.8,
        )
    )
    ax.add_artist(
        AnnotationBbox(
            drawing,
            (x, y),
            xybox=(0, 1),
            boxcoords="offset points",
            frameon=False,
            box_alignment=(0.5, 0),
            pad=0,
            annotation_clip=False,
            zorder=9,
        )
    )


def render(payload, split_id: str, metric_id: str, output: Path):
    split = next(item for item in payload["splits"] if item["id"] == split_id)
    metric = next(item for item in payload["metrics"] if item["id"] == metric_id)
    metric_results = payload["results"][split_id][metric_id]
    top_five = rank_combinations(payload, metric, metric_results)

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    fig = plt.figure(figsize=(12.8, 5.15), dpi=160, facecolor="white")
    grid = fig.add_gridspec(3, 1, height_ratios=[0.42, 0.55, 3.5], hspace=0.03)
    meta_ax = fig.add_subplot(grid[0])
    rank_ax = fig.add_subplot(grid[1])
    ax = fig.add_subplot(grid[2])

    for info_ax in (meta_ax, rank_ax):
        info_ax.set_axis_off()
        info_ax.set_xlim(0, 1)
        info_ax.set_ylim(0, 1)

    aggregation = payload.get("notes", {}).get("aggregation", "mean across runs")
    meta_ax.text(
        0,
        0.55,
        f"{split['label']}  /  {metric['label']}  /  {aggregation}",
        color="#24352E",
        fontsize=10.5,
        fontweight=650,
        ha="left",
        va="center",
    )
    direction = {
        "higher": "HIGHER IS BETTER",
        "lower": "LOWER IS BETTER",
        "target-one": "CLOSER TO 1 IS BETTER",
    }[metric["direction"]]
    meta_ax.text(
        1,
        0.55,
        direction,
        color="#0D7757" if metric["direction"] == "higher" else "#42554D",
        fontsize=8.2,
        fontweight=750,
        ha="right",
        va="center",
        bbox={
            "boxstyle": "round,pad=0.42,rounding_size=0.12",
            "facecolor": "#EAF4EF",
            "edgecolor": "#B7D4C8",
            "linewidth": 0.8,
        },
    )
    meta_ax.plot([0, 1], [0.03, 0.03], color="#D8E0DC", lw=0.8)

    rank_ax.set_facecolor("#F2F8F5")
    rank_ax.add_patch(
        plt.Rectangle((0, 0.08), 1, 0.84, facecolor="#F2F8F5", edgecolor="#C7DDD3", lw=0.8)
    )
    rank_ax.text(
        0.015,
        0.5,
        "TOP 5 COMBINATIONS",
        color="#0D7757",
        fontsize=8.2,
        fontweight=750,
        ha="left",
        va="center",
    )
    start_x = 0.155
    available = 0.83
    chip_width = available / 5 - 0.008
    for rank, item in enumerate(top_five, start=1):
        x = start_x + (rank - 1) * (chip_width + 0.008)
        rank_ax.text(
            x,
            0.5,
            str(rank),
            color="white",
            fontsize=7.5,
            fontweight=750,
            ha="center",
            va="center",
            bbox={"boxstyle": "circle,pad=0.26", "facecolor": "#0D7757", "edgecolor": "none"},
        )
        rank_ax.text(
            x + 0.014,
            0.58,
            f"{item['model']} / {item['representation']}",
            color="#24352E",
            fontsize=7.2,
            fontweight=650,
            ha="left",
            va="center",
        )
        rank_ax.text(
            x + 0.014,
            0.34,
            format_value(item["value"]),
            color="#0D7757",
            fontsize=7.2,
            fontweight=700,
            ha="left",
            va="center",
        )

    models = payload["models"]
    representations = payload["representations"]
    x_positions = np.arange(len(models))
    group_width = 0.82
    bar_width = group_width / len(representations)
    bar_lookup = {}

    for representation_index, representation in enumerate(representations):
        offset = (representation_index - (len(representations) - 1) / 2) * bar_width
        values = metric_results[representation["id"]]
        for model_index, model in enumerate(models):
            value = values[model]
            if value is None:
                continue
            center = x_positions[model_index] + offset
            ax.bar(
                center,
                value,
                width=bar_width * 0.9,
                color=COLORS[representation_index],
                edgecolor="none",
                zorder=3,
            )
            bar_lookup[(representation_index, model_index)] = (center, value)

    values = [
        value
        for representation in representations
        for value in metric_results[representation["id"]].values()
        if value is not None
    ]
    positive = [value for value in values if value > 0]
    use_log = positive and min(positive) > 0 and max(positive) / min(positive) > 100
    if use_log:
        ax.set_yscale("log")
        y_bottom = min(positive) * 0.75
        y_top = max(positive) * 1.55
    else:
        y_bottom = min(0, min(values))
        y_range = max(values) - y_bottom
        y_top = max(values) + max(y_range * 0.18, 0.04)
    ax.set_ylim(y_bottom, y_top)

    y_range = y_top - y_bottom
    for rank, item in enumerate(top_five[:3]):
        x, value = bar_lookup[(item["representation_index"], item["model_index"])]
        medal_y = value * 1.05 if use_log else value + y_range * 0.012
        add_medal(ax, x, medal_y, rank)

    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color="#E4EAE7", linewidth=0.75)
    ax.xaxis.grid(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#AAB7B1")
    ax.spines["bottom"].set_linewidth(0.8)
    ax.tick_params(axis="x", length=0, pad=8)
    ax.tick_params(axis="y", which="both", colors="#607069", labelsize=8, length=0)
    ax.set_ylabel(
        f"{metric['label']}{' (log scale)' if use_log else ''}",
        color="#24352E",
        fontsize=9.2,
        fontweight=650,
        labelpad=10,
    )
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f"{model}\n(baseline)" if model in BASELINE_MODELS else model for model in models])
    for label, model in zip(ax.get_xticklabels(), models):
        label.set_fontsize(7.4 if model in BASELINE_MODELS else 7.8)
        label.set_fontweight(750 if model in BASELINE_MODELS else 650)
        label.set_color("#A6463D" if model in BASELINE_MODELS else "#24352E")

    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="none") for color in COLORS
    ]
    ax.legend(
        legend_handles,
        [representation["label"] for representation in representations],
        ncol=10,
        loc="upper left",
        bbox_to_anchor=(0, 1.01),
        frameon=False,
        handlelength=1.0,
        handleheight=0.8,
        columnspacing=1.1,
        handletextpad=0.4,
        borderaxespad=0,
        fontsize=7.2,
        labelcolor="#42554D",
    )

    fig.subplots_adjust(left=0.055, right=0.99, top=0.97, bottom=0.105)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, facecolor="white", metadata={"Software": "Matplotlib"})
    plt.close(fig)


def main():
    args = parse_args()
    payload = (
        build_cell_line_payload(args.source_dir)
        if args.source_dir
        else json.loads(args.data.read_text(encoding="utf-8"))
    )
    if args.all:
        outputs = []
        for split in payload["splits"]:
            for metric in payload["metrics"]:
                output = args.output_dir / f"{split['id']}--{metric['id']}.png"
                render(payload, split["id"], metric["id"], output)
                outputs.append(output)
        print(f"Rendered {len(outputs)} images to {args.output_dir}")
    else:
        render(payload, args.split, args.metric, args.output)
        print(args.output)


if __name__ == "__main__":
    main()
