#!/usr/bin/env python3
"""Real per-case receptor-ligand contact and hydrogen-bond analysis.

Computes, directly from atomic coordinates, the receptor residues within
4.5 A of the top-scoring (mode 1) docked ligand pose for each of the 7
completed docking-reference-audit cases, plus a heavy-atom-only hydrogen-bond
list (N/O-N/O <= 3.5 A, no explicit-hydrogen angle check).

Algorithm and thresholds are an intentional parity match with the scAMH
platform's src/features/interface-contacts/interfaceContacts.ts (residue
contact cutoff 4.5 A, H-bond heuristic 3.5 A N/O-N/O, LigPlot/PLIP-style
approximation for structures without explicit hydrogens) — reimplemented
here in Python, independently, so this repository has no code dependency on
that platform. Both are free to diverge; this file is the source of truth
for the numbers reported in this repository.

Not a substitute for a validated hydrogen-bond network with explicit
hydrogens and donor-acceptor angle geometry (e.g. PLIP, LigPlot+). No
biological-activity or affinity inference is drawn from any contact listed
here.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path


RESIDUE_CONTACT_CUTOFF_ANGSTROM = 4.5
HBOND_CUTOFF_ANGSTROM = 3.5
HBOND_ELEMENTS = {"N", "O"}


@dataclass(frozen=True)
class Atom:
    chain: str
    res_name: str
    res_seq: int
    atom_name: str
    element: str
    x: float
    y: float
    z: float


def parse_pdb_atoms(text: str, chain_override: str | None = None) -> list[Atom]:
    atoms: list[Atom] = []
    for line in text.splitlines():
        if not (line.startswith("ATOM") or line.startswith("HETATM")):
            continue
        try:
            atom_name = line[12:16].strip()
            res_name = line[17:20].strip()
            chain = (line[21:22].strip() or "_") if chain_override is None else chain_override
            res_seq = int(line[22:26].strip())
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            element_raw = line[76:78].strip()
        except (ValueError, IndexError):
            continue
        element = (element_raw or "".join(c for c in atom_name if not c.isdigit())[:2]).upper()
        atoms.append(Atom(chain, res_name, res_seq, atom_name, element, x, y, z))
    if not atoms:
        raise ValueError("No valid ATOM/HETATM records found")
    return atoms


def first_pose_block(pdbqt_text: str) -> str:
    blocks = pdbqt_text.split("MODEL")
    # blocks[0] is any preamble; blocks[1] is mode 1 (top score)
    block = blocks[1] if len(blocks) > 1 else pdbqt_text
    return block.split("ENDMDL")[0]


def distance(a: Atom, b: Atom) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)


def residue_contacts(receptor: list[Atom], ligand: list[Atom], cutoff: float = RESIDUE_CONTACT_CUTOFF_ANGSTROM):
    contacts: dict[tuple, dict] = {}
    for ra in receptor:
        for la in ligand:
            d = distance(ra, la)
            if d > cutoff:
                continue
            key = (ra.chain, ra.res_seq, ra.res_name)
            entry = contacts.get(key)
            if entry is None or d < entry["min_dist"]:
                contacts[key] = {"min_dist": d, "count": entry["count"] + 1 if entry else 1}
            elif entry is not None:
                entry["count"] += 1
    rows = [
        {
            "receptor_chain": key[0], "receptor_resseq": key[1], "receptor_resname": key[2],
            "min_distance_angstrom": round(v["min_dist"], 3), "atom_pair_count": v["count"],
        }
        for key, v in contacts.items()
    ]
    rows.sort(key=lambda r: r["min_distance_angstrom"])
    return rows


def hydrogen_bonds(receptor: list[Atom], ligand: list[Atom], cutoff: float = HBOND_CUTOFF_ANGSTROM):
    rows = []
    for ra in receptor:
        if ra.element not in HBOND_ELEMENTS:
            continue
        for la in ligand:
            if la.element not in HBOND_ELEMENTS:
                continue
            d = distance(ra, la)
            if d > cutoff:
                continue
            rows.append({
                "receptor_chain": ra.chain, "receptor_resseq": ra.res_seq, "receptor_resname": ra.res_name,
                "receptor_atom": ra.atom_name,
                "ligand_atom": la.atom_name, "distance_angstrom": round(d, 3),
            })
    rows.sort(key=lambda r: r["distance_angstrom"])
    return rows


CASES = [
    {"case_id": "pilot-001", "pdb_id": "1STP", "receptor": "derived/strict-receptors/pilot-001_1STP_chain-A_strict.pdb", "poses": "derived/vina-runs/pilot-001_1STP_out.pdbqt"},
    {"case_id": "pilot-007", "pdb_id": "3D4Q", "receptor": "derived/strict-receptors/pilot-007_3D4Q_chain-A_strict.pdb", "poses": "derived/vina-runs/pilot-007_3D4Q_out.pdbqt"},
    {"case_id": "expansion-001", "pdb_id": "1B9V", "receptor": "derived/strict-receptors/expansion-001_1B9V_chain-A_strict.pdb", "poses": "derived/vina-runs/expansion-001_1B9V_out.pdbqt"},
    {"case_id": "pilot-008", "pdb_id": "3CJO", "receptor": "derived/strict-receptors/pilot-008_3CJO_chain-B_strict.pdb", "poses": "derived/vina-runs/pilot-008_3CJO_out.pdbqt"},
    {"case_id": "pilot-002", "pdb_id": "1HVR", "receptor": "derived/strict-receptors/pilot-002_1HVR_chain-A_strict.pdb", "poses": "derived/vina-runs/pilot-002_1HVR_out.pdbqt"},
    {"case_id": "pilot-006", "pdb_id": "3PTB", "receptor": "derived/strict-receptors/pilot-006_3PTB_chain-A_strict.pdb", "poses": "derived/vina-runs/pilot-006_3PTB_out.pdbqt"},
    {"case_id": "pilot-003", "pdb_id": "1IEP", "receptor": "derived/strict-receptors/pilot-003_1IEP_chain-A_strict.pdb", "poses": "derived/vina-runs/pilot-003_1IEP_out.pdbqt"},
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-contacts", type=Path, default=Path("data/interface_contacts_top_pose.csv"))
    parser.add_argument("--output-hbonds", type=Path, default=Path("data/hydrogen_bonds_top_pose.csv"))
    args = parser.parse_args()

    contact_rows: list[dict] = []
    hbond_rows: list[dict] = []
    for case in CASES:
        receptor_atoms = parse_pdb_atoms(Path(case["receptor"]).read_text(encoding="utf-8"))
        pose_text = first_pose_block(Path(case["poses"]).read_text(encoding="utf-8"))
        ligand_atoms = parse_pdb_atoms(pose_text, chain_override="LIG")

        contacts = residue_contacts(receptor_atoms, ligand_atoms)
        bonds = hydrogen_bonds(receptor_atoms, ligand_atoms)
        for row in contacts:
            contact_rows.append({"case_id": case["case_id"], "pdb_id": case["pdb_id"], **row})
        for row in bonds:
            hbond_rows.append({"case_id": case["case_id"], "pdb_id": case["pdb_id"], **row})
        print(f"{case['case_id']} {case['pdb_id']}: {len(contacts)} residue contacts, {len(bonds)} candidate H-bonds")

    args.output_contacts.parent.mkdir(parents=True, exist_ok=True)
    with args.output_contacts.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_id", "pdb_id", "receptor_chain", "receptor_resseq", "receptor_resname", "min_distance_angstrom", "atom_pair_count"])
        writer.writeheader()
        writer.writerows(contact_rows)
    with args.output_hbonds.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["case_id", "pdb_id", "receptor_chain", "receptor_resseq", "receptor_resname", "receptor_atom", "ligand_atom", "distance_angstrom"])
        writer.writeheader()
        writer.writerows(hbond_rows)
    print(f"Wrote {len(contact_rows)} contact rows to {args.output_contacts}")
    print(f"Wrote {len(hbond_rows)} H-bond rows to {args.output_hbonds}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
