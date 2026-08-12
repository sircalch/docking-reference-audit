#!/usr/bin/env python3
"""Propose, but never apply, deterministic receptor/ligand case policies.

For entries with multiple crystallographic copies, the closest polymer chain to
each declared ligand is measured from the original coordinates.  The resulting
CSV is a review queue: all rows remain pending until a researcher approves or
edits the policy.  It does not alter structures or launch docking.
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
    "declared_ligand",
    "proposed_ligand_instance",
    "proposed_receptor_chain",
    "closest_contact_angstrom",
    "water_policy",
    "other_nonpolymer_components",
    "other_components_policy",
    "selection_rule",
    "status",
)


def load_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "candidate"]


def residue_label(chain: gemmi.Chain, residue: gemmi.Residue) -> str:
    return f"{chain.name}:{residue.name}:{residue.seqid}"


def closest_chain_distance(ligand: gemmi.Residue, chain: gemmi.Chain) -> float:
    polymer_atoms = [atom for residue in chain.get_polymer() for atom in residue]
    if not polymer_atoms:
        return float("inf")
    return min(ligand_atom.pos.dist(polymer_atom.pos) for ligand_atom in ligand for polymer_atom in polymer_atoms)


def propose(candidate: dict[str, str], raw_dir: Path) -> dict[str, str]:
    pdb_id = candidate["pdb_id"].upper()
    structure = gemmi.read_structure(str(raw_dir / f"{candidate['case_id']}_{pdb_id}.cif"))
    model = structure[0]
    ligand_id = candidate["ligand_component_id"].upper()
    polymer_chains = [chain for chain in model if len(chain.get_polymer()) > 0]
    ligand_instances = [
        (chain, residue)
        for chain in model
        for residue in chain
        if residue.het_flag != "A" and residue.name == ligand_id
    ]
    if not ligand_instances or not polymer_chains:
        raise ValueError(f"{pdb_id}: no declared ligand instance or polymer chain available")

    possibilities = []
    for ligand_chain, ligand_residue in ligand_instances:
        nearest_chain, distance = min(
            ((chain, closest_chain_distance(ligand_residue, chain)) for chain in polymer_chains),
            key=lambda item: (item[1], item[0].name),
        )
        possibilities.append((distance, ligand_chain.name, str(ligand_residue.seqid), ligand_chain, ligand_residue, nearest_chain))
    distance, _, _, ligand_chain, ligand_residue, nearest_chain = min(
        possibilities,
        key=lambda item: (item[0], item[1], item[2]),
    )

    others: Counter[str] = Counter()
    for chain in model:
        for residue in chain:
            if residue.het_flag != "A" and not residue.is_water() and residue.name != ligand_id:
                others[residue.name] += 1
    other_text = ";".join(f"{name}:{count}" for name, count in sorted(others.items()))
    return {
        "case_id": candidate["case_id"],
        "pdb_id": pdb_id,
        "declared_ligand": ligand_id,
        "proposed_ligand_instance": residue_label(ligand_chain, ligand_residue),
        "proposed_receptor_chain": nearest_chain.name,
        "closest_contact_angstrom": f"{distance:.3f}",
        "water_policy": "remove_all_waters_pending_review",
        "other_nonpolymer_components": other_text,
        "other_components_policy": "manual_review_required" if other_text else "none_detected",
        "selection_rule": "minimum original-coordinate ligand-to-polymer atom distance; lexical tie-break",
        "status": "proposal_pending_researcher_review",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("data/candidates.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw/structures"))
    parser.add_argument("--output", type=Path, default=Path("data/case_policy_proposals.csv"))
    args = parser.parse_args()

    rows = [propose(candidate, args.raw_dir) for candidate in load_candidates(args.candidates)]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} policy proposals to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
