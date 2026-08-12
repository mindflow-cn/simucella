#!/usr/bin/env python3
"""Build the browser-ready benchmark summary from the source CSV/XLSX files."""

from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "assets" / "csv" / "xlsx"
OUTPUT_PATH = ROOT / "assets" / "benchmark-results.json"
SCRIPT_OUTPUT_PATH = ROOT / "assets" / "benchmark-results.js"

SPLITS = {
    "iid-sample": "IID sample",
    "ood-cell-line": "OOD cell line",
    "ood-primary-culture": "OOD primary culture",
    "ood-organoid": "OOD organoid",
    "ood-patient-sample": "OOD patient sample",
}

METRICS = {
    "atomic-pcs": ("Atomic-level PCS", "Gene Direction Acc", "higher"),
    "pcs-median": ("PCS (median)", "PCS （median）", "higher"),
    "esr": ("ESR", "ESR", "target-one"),
    "gcs": ("GCS", "GCS", "higher"),
    "mss": ("MSS", "MSS", "higher"),
    "pathway-spearman": ("Pathway Spearman", "Pathway Spearman", "higher"),
    "pathway-sign-accuracy": (
        "Pathway Sign Accuracy",
        "Pathway sign accuracy",
        "higher",
    ),
    "mse": ("MSE", "MSE", "lower"),
    "e-distance": ("E-distance", "E-distance", "lower"),
    "pcc-delta": ("PCC-delta", "PCC-delta", "higher"),
    "de-auprc": ("DE AUPRC", "DE AUPRC", "higher"),
    "de-f1": ("DE F1", "DE F1", "higher"),
    "logfc-spearman": ("logFC Spearman", "logFC Spearman", "higher"),
    "distribution-mmd": ("Distribution MMD", "Distribution MMD", "lower"),
}

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
    ("scgpt", "scGPT"),
    ("scimilarity", "scimilarity"),
    ("stack", "stack"),
    ("transcriptformer", "transcriptformer"),
]


def normalize_columns(frame):
    frame = frame.copy()
    frame.columns = [str(column).strip() for column in frame.columns]
    frame = frame.rename(columns={"Atomic-level PCS": "Gene Direction Acc"})
    return frame


def mean_by_model(frame, source_column, split_key, representation_key):
    values = {}
    for model in MODELS:
        series = pd.to_numeric(
            frame.loc[frame["model"] == model, source_column], errors="coerce"
        ).dropna()

        # Temporary source-data workaround requested on 2026-08-13. Remove once
        # scgpt!PRnet run 3 is present in scFM-all-source-iid-sample.xlsx.
        if (
            split_key == "iid-sample"
            and representation_key == "scgpt"
            and model == "PRnet"
            and len(series) == 2
        ):
            series = pd.concat([series, series.iloc[[1]]], ignore_index=True)

        values[model] = round(float(series.mean()), 10) if len(series) else None
    return values


def main():
    payload = {
        "splits": [{"id": key, "label": label} for key, label in SPLITS.items()],
        "metrics": [
            {
                "id": key,
                "label": definition[0],
                "direction": definition[2],
                "family": "mechanism" if index < 7 else "similarity",
            }
            for index, (key, definition) in enumerate(METRICS.items())
        ],
        "models": MODELS,
        "representations": [
            {"id": key, "label": label} for key, label in REPRESENTATIONS
        ],
        "results": {},
        "notes": {
            "aggregation": "Mean of three runs",
            "rawOnlyModels": ["baseMean", "PrePR-CT"],
            "temporaryImputation": (
                "IID sample / scGPT / PRnet run 3 temporarily duplicates run 2."
            ),
        },
    }

    for split_key in SPLITS:
        raw_path = SOURCE_DIR / f"raw-all-source-{split_key}.csv"
        embedding_path = SOURCE_DIR / f"scFM-all-source-{split_key}.xlsx"
        raw_frame = normalize_columns(pd.read_csv(raw_path))
        workbook = pd.ExcelFile(embedding_path)
        representation_frames = {"raw": raw_frame}

        for sheet_name in workbook.sheet_names:
            frame = normalize_columns(
                pd.read_excel(embedding_path, sheet_name=sheet_name, header=1)
            )
            frame = frame.rename(columns={frame.columns[0]: "model"})
            representation_frames[sheet_name] = frame

        split_results = {}
        for metric_key, (_, source_column, _) in METRICS.items():
            metric_results = {}
            for representation_key, _ in REPRESENTATIONS:
                frame = representation_frames[representation_key]
                metric_results[representation_key] = mean_by_model(
                    frame,
                    source_column,
                    split_key,
                    representation_key,
                )
            split_results[metric_key] = metric_results
        payload["results"][split_key] = split_results

    serialized = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
    OUTPUT_PATH.write_text(serialized, encoding="utf-8")
    SCRIPT_OUTPUT_PATH.write_text(
        f"window.SIMUCELLA_BENCHMARK_RESULTS={serialized};\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
