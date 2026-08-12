#!/usr/bin/env python3
"""Create a conservative structural inventory for retrieved mmCIF cases.

The inventory is not receptor preparation.  It only reports what is present in
the original coordinates so chain selection and cofactor policy can be decided
and documented before any irreversible transformation.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

import gemmi


FIELDS = (
    "case_id",
    "pdb_id",
    "ligand_component_id",
    "models",
    "polymer_chains",
    "ligand_instances",
    "ligand_atom_counts",
    "other_nonpolymer_components",
    "status",
    "review_note",
)


def load_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "candidate"]


def audit_candidate(candidate: dict[str, str], raw_dir: Path) -> dict[str, str]:
    pdb_id = candidate["pdb_id"].upper()
    path = raw_dir / f"{candidate['case_id']}_{pdb_id}.cif"
    structure = gemmi.read_structure(str(path))
    if not len(structure):
        raise ValueError(f"{path}: no models found")

    first_model = structure[0]
    polymer_chains = [chain.name for chain in first_model if len(chain.get_polymer()) > 0]
    ligand = candidate["ligand_component_id"].upper()
    ligand_atoms: list[int] = []
    other_components: Counter[str] = Counter()
    for chain in first_model:
        for residue in chain:
            if residue.het_flag == "A" or residue.is_water():
                continue
            if residue.name == ligand:
                ligand_atoms.append(len(residue))
            else:
                other_components[residue.name] += 1

    status = "ready_for_policy_review"
    notes: list[str] = []
    if not polymer_chains:
        status = "review_required"
        notes.append("no polymer chain detected")
    if not ligand_atoms:
        status = "review_required"
        notes.append("declared ligand not found in coordinates")
    if any(count < 3 for count in ligand_atoms):
        status = "review_required"
        notes.append("declared ligand has fewer than three atoms in at least one instance")
    if other_components:
        notes.append("other non-polymeric components require an explicit retention policy")

    return {
        "case_id": candidate["case_id"],
        "pdb_id": pdb_id,
        "ligand_component_id": ligand,
        "models": str(len(structure)),
        "polymer_chains": ";".join(polymer_chains),
        "ligand_instances": str(len(ligand_atoms)),
        "ligand_atom_counts": ";".join(map(str, ligand_atoms)),
        "other_nonpolymer_components": ";".join(
            f"{component}:{count}" for component, count in sorted(other_components.items())
        ),
        "status": status,
        "review_note": "; ".join(notes) or "no preliminary issue detected",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("data/candidates.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw/structures"))
    parser.add_argument("--output", type=Path, default=Path("data/structure_inventory.csv"))
    args = parser.parse_args()

    rows = [audit_candidate(candidate, args.raw_dir) for candidate in load_candidates(args.candidates)]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} inventory rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
