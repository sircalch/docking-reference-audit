#!/usr/bin/env python3
"""Render 2D ligand-receptor interaction diagrams (LigPlot+/PLIP-style schematic).

For each of the 7 completed docking cases, draws the docked top-scoring
ligand's real 2D bond skeleton (RDKit-generated depiction of the same
identity-verified molecule graph used throughout this project) with the
contacting receptor residues arranged schematically around it: green dashed
lines for hydrogen-bond candidates (labelled with the real donor-acceptor
distance, from data/hydrogen_bonds_top_pose.csv) and red lines for other
non-bonded contacts within the 4.5 A cutoff (labelled with the real minimum
heavy-atom distance, from data/interface_contacts_top_pose.csv).

This mirrors the schematic layout convention used by LigPlot+ and PLIP
(Laskowski & Swindells, 2011; Salentin et al., 2015): residue placement
around the ligand is for readability, not a to-scale 2D projection of the
real 3D geometry. Every distance, residue identity, and bond drawn is real
data already computed elsewhere in this project — nothing here is a new
measurement, only a new visualization of existing verified numbers.
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import rdDepictor

sys.path.insert(0, str(Path(__file__).parent))
from calculate_reference_pose_rmsd import reference_molecule  # noqa: E402
from render_binding_site_figures import CASES, read_csv  # noqa: E402


NAVY = "#17324D"
HBOND_GREEN = "#1E8A5F"
CONTACT_RED = "#B5473C"
LIGAND_INK = "#17324D"


def ligand_2d(case_id: str, pdb_id: str, component: str, candidates: dict[str, dict[str, str]]) -> tuple[list[tuple[float, float]], list[tuple[int, int]]]:
    reference = reference_molecule(case_id, pdb_id, component, candidates, Path("raw"))
    mol = Chem.Mol(reference)
    rdDepictor.Compute2DCoords(mol)
    conf = mol.GetConformer()
    coords = [(conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y) for i in range(mol.GetNumAtoms())]
    bonds = [(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()) for bond in mol.GetBonds()]
    return coords, bonds


def render_case(case: dict[str, str], contacts_by_case: dict, hbonds_by_case: dict, output_dir: Path) -> str:
    candidates = {row["case_id"]: row for row in read_csv(Path(case["candidates"]))}
    ligands = {row["case_id"]: row for row in read_csv(Path(case["ligand_manifest"])) if row["status"] == "prepared"}
    case_id = case["case_id"]
    pdb_id = case["pdb_id"]
    component = ligands[case_id]["component_id"]

    coords, bonds = ligand_2d(case_id, pdb_id, component, candidates)
    xs = [x for x, _ in coords]
    ys = [y for _, y in coords]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    ligand_radius = max(math.hypot(x - cx, y - cy) for x, y in coords) + 0.6

    hbond_residues = {(row["receptor_chain"], row["receptor_resseq"]) for row in hbonds_by_case.get(case_id, [])}
    hbond_min_distance = {}
    for row in hbonds_by_case.get(case_id, []):
        key = (row["receptor_chain"], row["receptor_resseq"])
        distance = float(row["distance_angstrom"])
        hbond_min_distance[key] = min(distance, hbond_min_distance.get(key, distance))

    contact_rows = sorted(contacts_by_case.get(case_id, []), key=lambda r: float(r["min_distance_angstrom"]))
    residues = []
    for row in contact_rows:
        key = (row["receptor_chain"], row["receptor_resseq"])
        label = f"{row['receptor_resname'].title()}{row['receptor_resseq']}"
        is_hbond = key in hbond_residues
        distance = hbond_min_distance[key] if is_hbond else float(row["min_distance_angstrom"])
        residues.append({"label": label, "is_hbond": is_hbond, "distance": distance})

    ring_radius = ligand_radius + 2.4
    n = len(residues)

    figure, axis = plt.subplots(figsize=(7.2, 7.2))
    for start, end in bonds:
        axis.plot([coords[start][0], coords[end][0]], [coords[start][1], coords[end][1]], color=LIGAND_INK, linewidth=2.0, zorder=5)
    for x, y in coords:
        axis.scatter([x], [y], color=LIGAND_INK, s=18, zorder=6)

    for index, residue in enumerate(residues):
        angle = 2 * math.pi * index / n - math.pi / 2 if n else 0.0
        rx, ry = cx + ring_radius * math.cos(angle), cy + ring_radius * math.sin(angle)
        color = HBOND_GREEN if residue["is_hbond"] else CONTACT_RED
        linestyle = "--" if residue["is_hbond"] else "-"
        # anchor the contact line on the ligand ring boundary nearest the residue, not a specific atom
        anchor_x = cx + ligand_radius * math.cos(angle)
        anchor_y = cy + ligand_radius * math.sin(angle)
        axis.plot([anchor_x, rx], [anchor_y, ry], color=color, linewidth=1.3, linestyle=linestyle, zorder=3, alpha=0.85)
        axis.scatter([rx], [ry], s=420, facecolor="white", edgecolor=color, linewidth=1.6, zorder=4)
        axis.text(rx, ry, residue["label"], ha="center", va="center", fontsize=7.6, color=NAVY, zorder=7)
        mid_x, mid_y = (anchor_x + rx) / 2, (anchor_y + ry) / 2
        axis.text(mid_x, mid_y, f"{residue['distance']:.2f} Å", ha="center", va="center", fontsize=6.4, color=color,
                   bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85), zorder=8)

    axis.set_title(f"{case_id} — {pdb_id} / {component}: top-pose contacts within 4.5 Å", fontsize=10.5, color=NAVY)
    axis.set_aspect("equal")
    axis.axis("off")
    handles = [
        plt.Line2D([0], [0], color=HBOND_GREEN, linestyle="--", label="Hydrogen-bond candidate (donor–acceptor ≤ 3.5 Å)"),
        plt.Line2D([0], [0], color=CONTACT_RED, linestyle="-", label="Other contact (min. heavy-atom distance ≤ 4.5 Å)"),
    ]
    axis.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02), fontsize=7.6, frameon=False, ncol=1)
    figure.tight_layout()

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / f"interaction-diagram-{case_id}-{pdb_id}"
    figure.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    figure.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(figure)
    return f"{case_id} ({pdb_id}): {len(residues)} contacting residues, {len(hbond_residues)} H-bond candidates"


def main() -> int:
    contacts_by_case: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(Path("data/interface_contacts_top_pose.csv")):
        contacts_by_case.setdefault(row["case_id"], []).append(row)
    hbonds_by_case: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(Path("data/hydrogen_bonds_top_pose.csv")):
        hbonds_by_case.setdefault(row["case_id"], []).append(row)

    output_dir = Path("reports/generated/figures/interaction-diagrams")
    for case in CASES:
        print(render_case(case, contacts_by_case, hbonds_by_case, output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
