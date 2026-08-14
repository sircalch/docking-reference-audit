#!/usr/bin/env python3
"""Classify each completed case against standard redocking success thresholds.

Reads the already-computed reference-pose RMSD CSVs (all Vina poses, all
batches) and reports, for the top-scoring pose and for the best pose found
in any mode, whether each of the 6 verified cases succeeds at the RMSD
thresholds conventionally used in docking-methodology benchmarks
(<=1.0, <=2.0, <=3.0 A; the 2.0 A threshold is the de facto standard used
by CASF and similar benchmarking campaigns). This adds no new measurement —
every RMSD value already exists in data/*_reference_pose_rmsd.csv — it only
classifies the existing numbers against a standard, citable convention.
"""

from __future__ import annotations

import csv
from pathlib import Path


RMSD_FILES = [
    "data/reference_pose_rmsd.csv",
    "data/contextual_batch_04_reference_pose_rmsd.csv",
    "data/contextual_batch_05_reference_pose_rmsd.csv",
    "data/contextual_batch_06_reference_pose_rmsd.csv",
    "data/contextual_batch_07_reference_pose_rmsd.csv",
    "data/contextual_batch_08_reference_pose_rmsd.csv",
]

THRESHOLDS = (1.0, 2.0, 3.0)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def classify(rmsd: float) -> dict[str, str]:
    return {f"success_le_{t:.1f}A".replace(".", "_"): ("yes" if rmsd <= t else "no") for t in THRESHOLDS}


def main() -> int:
    rows_by_case: dict[str, list[dict[str, str]]] = {}
    for file in RMSD_FILES:
        for row in read_csv(Path(file)):
            rows_by_case.setdefault(row["case_id"], []).append(row)

    output_rows = []
    for case_id in sorted(rows_by_case):
        case_rows = rows_by_case[case_id]
        pdb_id = case_rows[0]["pdb_id"]
        verified = [r for r in case_rows if r["mapping_status"] == "verified"]
        if not verified:
            output_rows.append({
                "case_id": case_id, "pdb_id": pdb_id,
                "top_score_rmsd_angstrom": "", "best_rmsd_angstrom": "",
                **{f"success_le_{t:.1f}A".replace(".", "_"): "not_verified" for t in THRESHOLDS},
                "mapping_status": "not_verified",
            })
            continue
        top = next(r for r in verified if r["mode"] == "1")
        top_rmsd = float(top["experimental_reference_heavy_atom_rmsd_angstrom"])
        best_rmsd = min(float(r["experimental_reference_heavy_atom_rmsd_angstrom"]) for r in verified)
        row = {
            "case_id": case_id, "pdb_id": pdb_id,
            "top_score_rmsd_angstrom": f"{top_rmsd:.3f}",
            "best_rmsd_angstrom": f"{best_rmsd:.3f}",
            "mapping_status": "verified",
        }
        row.update(classify(best_rmsd))
        output_rows.append(row)
        print(f"{case_id} ({pdb_id}): top-score {top_rmsd:.3f} A | best {best_rmsd:.3f} A | "
              + " ".join(f"<=%.1fA:%s" % (t, row[f'success_le_{t:.1f}A'.replace('.', '_')]) for t in THRESHOLDS))

    output = Path("data/success_thresholds.csv")
    fieldnames = ["case_id", "pdb_id", "top_score_rmsd_angstrom", "best_rmsd_angstrom",
                  "success_le_1_0A", "success_le_2_0A", "success_le_3_0A", "mapping_status"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    print(f"Wrote {len(output_rows)} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
