#!/usr/bin/env python3
"""Write a conservative, traceable report from subpilot manifests."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preparation", type=Path, default=Path("data/strict_preparation_manifest.csv"))
    parser.add_argument("--runs", type=Path, default=Path("data/vina_run_manifest.csv"))
    parser.add_argument("--poses", type=Path, default=Path("data/vina_pose_scores.csv"))
    parser.add_argument("--reference-rmsd", type=Path, default=Path("data/reference_pose_rmsd.csv"))
    parser.add_argument("--output", type=Path, default=Path("reports/SUBPILOT-RESULTS-v0.1.md"))
    args = parser.parse_args()
    preparation = read_rows(args.preparation)
    runs = read_rows(args.runs)
    poses = read_rows(args.poses)
    reference_rmsd = read_rows(args.reference_rmsd)
    prepared = [row for row in preparation if row["status"] == "prepared"]
    failed = [row for row in preparation if row["status"] == "failed"]
    completed = [row for row in runs if row["status"] == "completed"]
    by_case: dict[str, list[dict[str, str]]] = {}
    for pose in poses:
        by_case.setdefault(pose["case_id"], []).append(pose)
    rmsd_by_case: dict[str, list[dict[str, str]]] = {}
    for row in reference_rmsd:
        if row.get("mapping_status") == "verified":
            rmsd_by_case.setdefault(row["case_id"], []).append(row)

    lines = [
        "# Strict docking-reference subpilot — results v0.1",
        "",
        "## Scope",
        "",
        "This report is generated from versioned manifests in this repository. It is a feasibility subpilot, not a docking-performance benchmark, binding-affinity estimate, or biological validation.",
        "",
        "## Strict receptor preparation",
        "",
        f"The frozen clean-case subpilot contained {len(preparation)} receptors. {len(prepared)} completed strict Meeko preparation and {len(failed)} were rejected without repair, residue deletion, manual alternate-location selection, or changed parameters.",
        "",
        "| Case | PDB | Outcome | Recorded cause |",
        "|---|---|---|---|",
    ]
    for row in preparation:
        cause = row.get("normalized_error_class") or "—"
        lines.append(f"| {row['case_id']} | {row['pdb_id']} | {row['status']} | {cause} |")
    lines += [
        "",
        "## Eligible Vina executions",
        "",
        f"{len(completed)} cases had both a strictly prepared receptor and a prepared reference ligand. Each used AutoDock Vina 1.2.5 through WSL with a fixed seed (20260812), one CPU, exhaustiveness 8, and a box derived from the experimental ligand coordinates. Each completed case retained all nine requested poses.",
        "",
        "| Case | PDB | Poses retained | Top-score affinity (kcal/mol) | Top-score RMSD to experiment (Å) | Lowest RMSD to experiment (Å) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for run in completed:
        case_poses = sorted(by_case.get(run["case_id"], []), key=lambda row: int(row["mode"]))
        affinities = [float(row["affinity_kcal_mol"]) for row in case_poses]
        case_rmsd = rmsd_by_case.get(run["case_id"], [])
        top_mode = min(case_poses, key=lambda row: float(row["affinity_kcal_mol"]))["mode"]
        top_rmsd = next(float(row["experimental_reference_heavy_atom_rmsd_angstrom"]) for row in case_rmsd if row["mode"] == top_mode)
        lowest_rmsd = min(float(row["experimental_reference_heavy_atom_rmsd_angstrom"]) for row in case_rmsd)
        lines.append(
            f"| {run['case_id']} | {run['pdb_id']} | {len(case_poses)} | {min(affinities):.3f} | {top_rmsd:.3f} | {lowest_rmsd:.3f} |"
        )
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "The Vina RMSD values in `data/vina_pose_scores.csv` describe each returned pose relative to Vina's best-scoring pose. They are not RMSD to the experimental ligand pose and must not be interpreted as pose recovery. The experimental-reference values in `data/reference_pose_rmsd.csv` are identity-mapped, aligned heavy-atom RMSD after verifying the RCSB CCD-to-SDF atom order, the experimental heavy atoms, isomeric heavy-atom SMILES and pose counts.",
        "",
        "The 1FPU preparation failure is a retained outcome of the strict policy. It must not be converted into a success by enabling `--allow_bad_res` or by manually repairing coordinates within this protocol version.",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
