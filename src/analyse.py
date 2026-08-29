"""Reproduce the phase-angle and AIx@75 analysis from an authorised workbook.

Participant-level outputs are deliberately not written to disk.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


def find_column(columns, fragment: str) -> str:
    labels = [str(column) for column in columns]
    exact = [label for label in labels if label.strip().casefold() == fragment.strip().casefold()]
    if exact:
        return exact[0]
    matches = [label for label in labels if fragment.lower() in label.lower()]
    if len(matches) != 1:
        raise ValueError(f"Expected one column containing {fragment!r}; found {matches}")
    return matches[0]


def load_analysis_data(path: Path, sheet: str = "DATA_23_24") -> pd.DataFrame:
    frame = pd.read_excel(path, sheet_name=sheet, header=1)
    selected = frame[[
        find_column(frame.columns, "BEI PIC Master List"),
        find_column(frame.columns, "Age"),
        find_column(frame.columns, "PHASE ANGLE"),
        find_column(frame.columns, "AIx75"),
    ]].copy()
    selected.columns = ["participant_code", "age", "phase_angle", "aix75"]
    for column in ["age", "phase_angle", "aix75"]:
        selected[column] = pd.to_numeric(selected[column], errors="coerce")
    return selected


def analyse(frame: pd.DataFrame) -> tuple[dict[str, float], pd.DataFrame]:
    eligible = frame.loc[frame["age"].between(18, 30), ["phase_angle", "aix75"]].dropna()
    if len(eligible) < 3:
        raise ValueError("At least three complete age-eligible observations are required")
    correlation = stats.pearsonr(eligible["phase_angle"], eligible["aix75"])
    regression = stats.linregress(eligible["phase_angle"], eligible["aix75"])
    summary = {
        "n": int(len(eligible)),
        "phase_angle_mean": float(eligible["phase_angle"].mean()),
        "phase_angle_sd": float(eligible["phase_angle"].std(ddof=1)),
        "aix75_mean": float(eligible["aix75"].mean()),
        "aix75_sd": float(eligible["aix75"].std(ddof=1)),
        "pearson_r": float(correlation.statistic),
        "p_value": float(correlation.pvalue),
        "slope": float(regression.slope),
        "intercept": float(regression.intercept),
        "r_squared": float(regression.rvalue**2),
    }
    return summary, eligible


def save_aggregate_outputs(summary: dict[str, float], eligible: pd.DataFrame, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "analysis_summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    figure, axis = plt.subplots(figsize=(7, 5))
    axis.scatter(eligible["phase_angle"], eligible["aix75"], alpha=0.65, color="#1f6f8b")
    x_min, x_max = eligible["phase_angle"].min(), eligible["phase_angle"].max()
    axis.plot(
        [x_min, x_max],
        [summary["intercept"] + summary["slope"] * x_min,
         summary["intercept"] + summary["slope"] * x_max],
        color="#c44e52",
        linewidth=2,
    )
    axis.set(xlabel="Phase angle (degrees)", ylabel="AIx@75 (%)",
             title="Phase angle and heart-rate-standardised augmentation index")
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(output / "phase_angle_vs_aix75.png", dpi=180)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results/local_run"))
    args = parser.parse_args()
    summary, eligible = analyse(load_analysis_data(args.workbook))
    save_aggregate_outputs(summary, eligible, args.output)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
