#!/usr/bin/env python3
"""Render publication-oriented figures from versioned audit manifests.

No figure contains simulated values.  The outputs are descriptive snapshots of
the registered data and retain the distinction between structural inventory,
strict preparation, and completed reference-pose recovery.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


NAVY = "#17324D"
TEAL = "#007C83"
GOLD = "#C78B1B"
CORAL = "#B5473C"
GRAY = "#6C7781"
LIGHT = "#F4F7F8"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(figure: plt.Figure, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(destination.with_suffix(".svg"), bbox_inches="tight")
    figure.savefig(destination.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(figure)


def setup() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titleweight": "bold",
        "axes.labelcolor": NAVY,
        "axes.edgecolor": "#B9C3CA",
        "xtick.color": "#46535E",
        "ytick.color": "#46535E",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def inventory_disposition(rows: list[dict[str, str]], destination: Path) -> None:
    counts = Counter(row["stratum"] for row in rows)
    labels = ["Clean", "Contextual", "Review\nrequired"]
    values = [counts["clean"], counts["contextual"], counts["review_required"]]
    colors = [TEAL, GOLD, CORAL]
    figure, axis = plt.subplots(figsize=(7.2, 4.5))
    bars = axis.bar(labels, values, color=colors, width=0.62)
    axis.set_ylabel("Registered cases")
    axis.set_title("Structural inventory disposition")
    axis.set_ylim(0, max(values) + 3)
    axis.grid(axis="y", alpha=0.2)
    axis.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 0.35, str(value), ha="center", color=NAVY, weight="bold")
    axis.text(
        0.5,
        -0.22,
        "Classification is based on frozen original-coordinate mmCIF inventory; it is not a docking result.",
        transform=axis.transAxes,
        ha="center",
        va="top",
        color=GRAY,
        fontsize=8.5,
    )
    save(figure, destination / "figure-01-structural-inventory")


def preparation_outcomes(rows: list[dict[str, str]], destination: Path) -> None:
    rows = sorted(rows, key=lambda row: row["case_id"])
    figure, axis = plt.subplots(figsize=(9.2, 4.7))
    for index, row in enumerate(rows):
        prepared = row["status"] == "prepared"
        color = TEAL if prepared else CORAL
        axis.hlines(index, 0, 1, color="#D7DEE2", linewidth=6, zorder=1)
        axis.scatter(1 if prepared else 0, index, s=150, color=color, zorder=2, edgecolor="white", linewidth=1.2)
        detail = "prepared" if prepared else row["normalized_error_class"].replace("meeko_", "")
        axis.text(1.06 if prepared else 0.06, index, detail.replace("_", " "), va="center", color=NAVY, fontsize=8.5)
    axis.set_yticks(range(len(rows)), [f"{row['pdb_id']}  ({row['case_id']})" for row in rows])
    axis.set_xticks([0, 1], ["Rejected under\nstrict policy", "Prepared"])
    axis.set_xlim(-0.04, 1.68)
    axis.set_title("Strict receptor-preparation outcomes")
    axis.spines[["top", "right", "bottom"]].set_visible(False)
    axis.tick_params(axis="x", length=0)
    axis.invert_yaxis()
    axis.legend(
        handles=[
            Line2D([0], [0], marker="o", color="w", markerfacecolor=TEAL, label="prepared", markersize=9),
            Line2D([0], [0], marker="o", color="w", markerfacecolor=CORAL, label="rejected", markersize=9),
        ],
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.5, -0.27),
    )
    save(figure, destination / "figure-02-strict-preparation")


def pose_recovery(rows: list[dict[str, str]], destination: Path) -> None:
    rows = [row for row in rows if row.get("mapping_status") == "verified"]
    cases = sorted({row["pdb_id"] for row in rows})
    palette = [TEAL, NAVY, GOLD, CORAL]
    colors = {case: palette[index % len(palette)] for index, case in enumerate(cases)}
    figure, axis = plt.subplots(figsize=(7.6, 5.2))
    for case in cases:
        selected = [row for row in rows if row["pdb_id"] == case]
        axis.scatter(
            [float(row["affinity_kcal_mol"]) for row in selected],
            [float(row["experimental_reference_heavy_atom_rmsd_angstrom"]) for row in selected],
            s=58,
            color=colors[case],
            edgecolor="white",
            linewidth=0.8,
            label=case,
            alpha=0.95,
        )
    axis.axhline(2.0, color=GOLD, linestyle="--", linewidth=1.2, label="2 Å reference")
    axis.set_xlabel("Vina affinity (kcal/mol)")
    axis.set_ylabel("Experimental-reference heavy-atom RMSD (Å)")
    axis.set_title("All retained reference-pose outcomes")
    axis.grid(alpha=0.22)
    axis.spines[["top", "right"]].set_visible(False)
    axis.legend(frameon=False, title="PDB entry")
    axis.text(
        0.5,
        -0.22,
        "Each point is one retained Vina pose. RMSD is identity-mapped and aligned to the experimental ligand pose.",
        transform=axis.transAxes,
        ha="center",
        va="top",
        color=GRAY,
        fontsize=8.5,
    )
    save(figure, destination / "figure-03-reference-pose-outcomes")


def evidence_flow(
    candidates: list[dict[str, str]],
    retrieval: list[dict[str, str]],
    inventory: list[dict[str, str]],
    preparation: list[dict[str, str]],
    rmsd: list[dict[str, str]],
    destination: Path,
) -> None:
    retrieved = sum(row["status"] == "retrieved" for row in retrieval)
    retrieval_failed = sum(row["status"] != "retrieved" for row in retrieval)
    clean = sum(row["stratum"] == "clean" for row in inventory)
    contextual = sum(row["stratum"] == "contextual" for row in inventory)
    prepared = sum(row["status"] == "prepared" for row in preparation)
    rejected = sum(row["status"] == "failed" for row in preparation)
    completed_cases = len({row["case_id"] for row in rmsd})
    stages = [
        ("Registered\ncandidates", len(candidates), NAVY),
        ("Original mmCIF\nretrieved", retrieved, TEAL),
        ("Frozen\ninventory", len(inventory), NAVY),
        ("Strict preparation\nprepared", prepared, TEAL),
        ("Completed\nreference-pose runs", completed_cases, TEAL),
    ]
    figure, axis = plt.subplots(figsize=(11.0, 4.8))
    axis.set_xlim(-0.6, len(stages) - 0.4)
    axis.set_ylim(-1.1, 1.2)
    axis.axis("off")
    for index, (label, value, color) in enumerate(stages):
        axis.scatter(index, 0.2, s=2200, color=color, zorder=3, edgecolor="white", linewidth=2)
        axis.text(index, 0.28, str(value), ha="center", va="center", color="white", weight="bold", fontsize=15, zorder=4)
        axis.text(index, -0.43, label, ha="center", va="top", color=NAVY, weight="bold", fontsize=9)
        if index < len(stages) - 1:
            axis.annotate("", xy=(index + 0.73, 0.2), xytext=(index + 0.27, 0.2), arrowprops={"arrowstyle": "-|>", "color": "#B6C2C8", "lw": 2.3})
    axis.text(
        1.0,
        0.83,
        f"{retrieval_failed} retrieval failures retained",
        ha="center",
        color=CORAL,
        weight="bold",
        fontsize=9,
    )
    axis.annotate("", xy=(1.0, 0.43), xytext=(1.0, 0.72), arrowprops={"arrowstyle": "-|>", "color": CORAL, "lw": 1.5})
    axis.text(
        2.0,
        0.83,
        f"{clean} clean; {contextual} contextual",
        ha="center",
        color=GOLD,
        weight="bold",
        fontsize=9,
    )
    axis.annotate("", xy=(2.0, 0.43), xytext=(2.0, 0.72), arrowprops={"arrowstyle": "-|>", "color": GOLD, "lw": 1.5})
    axis.text(
        3.0,
        0.83,
        f"{rejected} strict rejections retained",
        ha="center",
        color=CORAL,
        weight="bold",
        fontsize=9,
    )
    axis.annotate("", xy=(3.0, 0.43), xytext=(3.0, 0.72), arrowprops={"arrowstyle": "-|>", "color": CORAL, "lw": 1.5})
    axis.set_title("Evidence flow from public structures to verified reference poses", color=NAVY, pad=16)
    axis.text(2.0, -0.92, "Counts are a manifest snapshot; branches are retained rather than removed from the record.", ha="center", color=GRAY, fontsize=8.5)
    save(figure, destination / "figure-04-evidence-flow")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output-dir", type=Path, default=Path("reports/generated/figures"))
    args = parser.parse_args()
    setup()
    inventory = read_rows(args.data_dir / "eligibility_register.csv")
    candidates = read_rows(args.data_dir / "candidates.csv")
    retrieval = read_rows(args.data_dir / "retrieval_manifest.csv")
    preparation = read_rows(args.data_dir / "strict_preparation_manifest.csv")
    for manifest in sorted(args.data_dir.glob("clean_batch_[0-9][0-9]_preparation_manifest.csv")):
        preparation.extend(read_rows(manifest))
    for manifest in sorted(args.data_dir.glob("contextual_batch_[0-9][0-9]_preparation_manifest.csv")):
        preparation.extend(read_rows(manifest))
    rmsd = read_rows(args.data_dir / "reference_pose_rmsd.csv")
    for manifest in sorted(args.data_dir.glob("contextual_batch_[0-9][0-9]_reference_pose_rmsd.csv")):
        rmsd.extend(read_rows(manifest))
    inventory_disposition(inventory, args.output_dir)
    preparation_outcomes(preparation, args.output_dir)
    pose_recovery(rmsd, args.output_dir)
    evidence_flow(candidates, retrieval, inventory, preparation, rmsd, args.output_dir)
    print(f"Rendered 4 figures to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
