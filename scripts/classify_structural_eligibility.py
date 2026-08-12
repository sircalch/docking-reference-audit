#!/usr/bin/env python3
"""Classify frozen inventories without preparing or modifying structures.

The register deliberately distinguishes an entry that is structurally clean
from one that requires a case-specific receptor-context decision.  It is an
audit aid only: a ``clean`` classification does not assert that preparation,
ligand conversion, docking, or reference-pose verification has succeeded.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = (
    "case_id",
    "pdb_id",
    "ligand_component_id",
    "stratum",
    "classification_reason",
    "execution_status",
)


def split_count(value: str) -> int:
    return len([item for item in value.split(";") if item])


def load_completed_runs(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            row["case_id"]
            for row in csv.DictReader(handle)
            if row.get("status") == "completed"
        }


def classify(row: dict[str, str], completed_runs: set[str]) -> dict[str, str]:
    case_id = row["case_id"]
    base = {
        "case_id": case_id,
        "pdb_id": row["pdb_id"],
        "ligand_component_id": row["ligand_component_id"],
        "execution_status": (
            "completed_reference_pose_existing_subpilot"
            if case_id in completed_runs
            else "not_run_by_this_register"
        ),
    }

    if row["status"] != "ready_for_policy_review":
        return {
            **base,
            "stratum": "review_required",
            "classification_reason": row["review_note"],
        }

    chains = split_count(row["polymer_chains"])
    ligand_instances = int(row["ligand_instances"])
    other_components = row["other_nonpolymer_components"]
    if chains == 1 and ligand_instances == 1 and not other_components:
        return {
            **base,
            "stratum": "clean",
            "classification_reason": "one polymer chain; one declared ligand instance; no other non-polymeric components",
        }

    reasons: list[str] = []
    if chains != 1:
        reasons.append(f"{chains} polymer chains")
    if ligand_instances != 1:
        reasons.append(f"{ligand_instances} declared ligand instances")
    if other_components:
        reasons.append(f"other components: {other_components}")
    return {
        **base,
        "stratum": "contextual",
        "classification_reason": "; ".join(reasons),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=Path("data/structure_inventory.csv"))
    parser.add_argument("--runs", type=Path, default=Path("data/vina_run_manifest.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/eligibility_register.csv"))
    args = parser.parse_args()

    with args.inventory.open(newline="", encoding="utf-8") as handle:
        completed_runs = load_completed_runs(args.runs)
        rows = [classify(row, completed_runs) for row in csv.DictReader(handle)]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    counts = {stratum: sum(row["stratum"] == stratum for row in rows) for stratum in ("clean", "contextual", "review_required")}
    print(f"Wrote {len(rows)} rows to {args.output}: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
