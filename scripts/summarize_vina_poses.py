#!/usr/bin/env python3
"""Parse every Vina pose score from completed frozen subpilot logs.

The RMSD columns reported by Vina are pose-to-best-pose distances, not RMSD to
the experimental reference. They are retained under unambiguous names and are
not used as reference-pose recovery results.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


HEADER = re.compile(r"^\s*(\d+)\s+(-?\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*$")
FIELDS = ("case_id", "pdb_id", "mode", "affinity_kcal_mol", "rmsd_to_best_lower_bound_angstrom", "rmsd_to_best_upper_bound_angstrom")


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "completed"]


def parse_modes(log_path: Path) -> list[tuple[str, str, str, str]]:
    text = log_path.read_text(encoding="utf-8")
    parsed = [match.groups() for line in text.splitlines() if (match := HEADER.match(line))]
    if not parsed:
        raise ValueError(f"No Vina pose table found in {log_path}")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("data/vina_run_manifest.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/vina_pose_scores.csv"))
    args = parser.parse_args()
    rows: list[dict[str, str]] = []
    for run in read_manifest(args.manifest):
        for mode, affinity, rmsd_lb, rmsd_ub in parse_modes(Path(run["log_path"])):
            rows.append({
                "case_id": run["case_id"], "pdb_id": run["pdb_id"], "mode": mode,
                "affinity_kcal_mol": affinity,
                "rmsd_to_best_lower_bound_angstrom": rmsd_lb,
                "rmsd_to_best_upper_bound_angstrom": rmsd_ub,
            })
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} pose rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
