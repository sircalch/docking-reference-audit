#!/usr/bin/env python3
"""Extract frozen clean-subpilot receptor PDBs without repair operations."""

from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import gemmi


FIELDS = (
    "case_id", "pdb_id", "receptor_chain", "source_path", "source_sha256",
    "output_path", "output_sha256", "output_bytes", "operations", "created_at_utc",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_subpilot(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "accepted"]


def parse_ligand_name(reference_ligand_instance: str) -> str:
    # Format is "<chain>:<component>:<auth_seq_id>", e.g. "B:K30:603".
    parts = reference_ligand_instance.split(":")
    if len(parts) != 3:
        raise ValueError(f"unexpected reference_ligand_instance format: {reference_ligand_instance!r}")
    return parts[1]


def strip_ligand_and_water(chain: "gemmi.Chain", ligand_name: str, retained_components: set[str]) -> None:
    # Declared policy: always remove water and the declared reference ligand.
    # Any other non-polymer component is removed unless explicitly retained by
    # a per-case policy (e.g. a covalently bound or physiological cofactor
    # unrelated to the docked ligand). Standard polymer residues (het_flag "A")
    # are never touched. This must not repair, delete polymer residues, or
    # choose an alternate location.
    to_delete = [
        index
        for index, residue in enumerate(chain)
        if residue.is_water()
        or (residue.het_flag != "A" and residue.name not in retained_components)
    ]
    for index in reversed(to_delete):
        del chain[index]


def extract(row: dict[str, str], raw_dir: Path, output_dir: Path) -> dict[str, str]:
    pdb_id = row["pdb_id"].upper()
    source = raw_dir / f"{row['case_id']}_{pdb_id}.cif"
    structure = gemmi.read_structure(str(source)).clone()
    if len(structure) != 1:
        raise ValueError(f"{pdb_id}: strict subpilot requires exactly one model")
    model = structure[0]
    chain_name = row["receptor_chain"]
    if model.find_chain(chain_name) is None:
        raise ValueError(f"{pdb_id}: selected receptor chain {chain_name} is absent")
    for name in [chain.name for chain in model if chain.name != chain_name]:
        model.remove_chain(name)
    retained_components = {
        component.strip().upper()
        for component in row.get("retained_components", "").split(";")
        if component.strip()
    }
    if retained_components:
        ligand_name = parse_ligand_name(row["reference_ligand_instance"])
        strip_ligand_and_water(model.find_chain(chain_name), ligand_name, retained_components)
        operations = (
            "select declared chain; remove other chains; remove water and declared ligand; "
            f"retain declared non-polymer components ({', '.join(sorted(retained_components))}); "
            "no repair/altloc selection/residue deletion"
        )
    else:
        # The clean-case policy declares no retained non-polymeric components.
        # This removes water and all ligands after the selected receptor chain is fixed.
        model.remove_ligands_and_waters()
        operations = "select declared chain; remove other chains; remove ligands and waters; no repair/altloc selection"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{row['case_id']}_{pdb_id}_chain-{chain_name}_strict.pdb"
    structure.write_pdb(str(output))
    return {
        "case_id": row["case_id"],
        "pdb_id": pdb_id,
        "receptor_chain": chain_name,
        "source_path": source.as_posix(),
        "source_sha256": sha256(source),
        "output_path": output.as_posix(),
        "output_sha256": sha256(output),
        "output_bytes": str(output.stat().st_size),
        "operations": operations,
        "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpilot", type=Path, default=Path("data/strict_subpilot.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw/structures"))
    parser.add_argument("--output-dir", type=Path, default=Path("derived/strict-receptors"))
    parser.add_argument("--manifest", type=Path, default=Path("data/receptor_extraction_manifest.csv"))
    args = parser.parse_args()
    rows = [extract(row, args.raw_dir, args.output_dir) for row in load_subpilot(args.subpilot)]
    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} strict receptor extractions to {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
