#!/usr/bin/env python3
"""Derive frozen Vina boxes from registered experimental ligand coordinates."""

from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import gemmi


PADDING_ANGSTROM = 8.0
MINIMUM_SIZE_ANGSTROM = 20.0
EXHAUSTIVENESS = 8
NUM_MODES = 9
ENERGY_RANGE = 3
FIELDS = (
    "case_id", "pdb_id", "reference_ligand_instance", "config_path", "config_sha256",
    "center_x", "center_y", "center_z", "size_x", "size_y", "size_z", "padding_angstrom",
    "minimum_size_angstrom", "exhaustiveness", "num_modes", "energy_range", "created_at_utc",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_subpilot(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row.get("status") == "accepted"]


def find_ligand(structure: gemmi.Structure, label: str) -> gemmi.Residue:
    chain_name, component, sequence = label.split(":", maxsplit=2)
    chain = structure[0].find_chain(chain_name)
    if chain is None:
        raise ValueError(f"Ligand chain {chain_name} not found")
    for residue in chain:
        if residue.name == component and str(residue.seqid) == sequence:
            return residue
    raise ValueError(f"Ligand instance {label} not found")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subpilot", type=Path, default=Path("data/strict_subpilot.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw/structures"))
    parser.add_argument("--output-dir", type=Path, default=Path("derived/vina-configs"))
    parser.add_argument("--manifest", type=Path, default=Path("data/vina_box_manifest.csv"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for case in load_subpilot(args.subpilot):
        pdb_id = case["pdb_id"].upper()
        source = args.raw_dir / f"{case['case_id']}_{pdb_id}.cif"
        ligand = find_ligand(gemmi.read_structure(str(source)), case["reference_ligand_instance"])
        positions = [atom.pos for atom in ligand]
        if len(positions) < 3:
            raise ValueError(f"{case['case_id']}: reference ligand has fewer than three atoms")
        minima = [min(getattr(position, axis) for position in positions) for axis in ("x", "y", "z")]
        maxima = [max(getattr(position, axis) for position in positions) for axis in ("x", "y", "z")]
        center = [(low + high) / 2 for low, high in zip(minima, maxima)]
        size = [max(MINIMUM_SIZE_ANGSTROM, high - low + 2 * PADDING_ANGSTROM) for low, high in zip(minima, maxima)]
        config = args.output_dir / f"{case['case_id']}_{pdb_id}.txt"
        config.write_text(
            "# Frozen reference-pose box; derived from the original experimental ligand.\n"
            + f"center_x = {center[0]:.3f}\ncenter_y = {center[1]:.3f}\ncenter_z = {center[2]:.3f}\n"
            + f"size_x = {size[0]:.3f}\nsize_y = {size[1]:.3f}\nsize_z = {size[2]:.3f}\n"
            + f"exhaustiveness = {EXHAUSTIVENESS}\nnum_modes = {NUM_MODES}\nenergy_range = {ENERGY_RANGE}\n",
            encoding="utf-8",
        )
        rows.append({
            "case_id": case["case_id"], "pdb_id": pdb_id,
            "reference_ligand_instance": case["reference_ligand_instance"],
            "config_path": config.as_posix(), "config_sha256": sha256(config),
            "center_x": f"{center[0]:.3f}", "center_y": f"{center[1]:.3f}", "center_z": f"{center[2]:.3f}",
            "size_x": f"{size[0]:.3f}", "size_y": f"{size[1]:.3f}", "size_z": f"{size[2]:.3f}",
            "padding_angstrom": f"{PADDING_ANGSTROM:.1f}", "minimum_size_angstrom": f"{MINIMUM_SIZE_ANGSTROM:.1f}",
            "exhaustiveness": str(EXHAUSTIVENESS), "num_modes": str(NUM_MODES), "energy_range": str(ENERGY_RANGE),
            "created_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        })
        print(f"{case['case_id']} {pdb_id}: box derived")
    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
