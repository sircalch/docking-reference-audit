#!/usr/bin/env python3
"""Render 3D binding-site figures for every completed docking case.

For each case with both a strictly prepared receptor and a completed Vina
run, this draws the pocket backbone context, the experimental reference
ligand pose, and Vina's top-scoring docked pose, all from real coordinates
already computed and versioned elsewhere in this project (no simulated
positions). Reuses the identity-verified reference-molecule reconstruction
from calculate_reference_pose_rmsd.py so the experimental pose drawn here is
provably the same one used for RMSD verification.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import gemmi
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3D projection)
from meeko import PDBQTMolecule, RDKitMolCreate
from rdkit import Chem

sys.path.insert(0, str(Path(__file__).parent))
from calculate_reference_pose_rmsd import reference_molecule  # noqa: E402


NAVY = "#17324D"
TEAL = "#007C83"
CORAL = "#B5473C"
GRAY = "#98A2AC"

CASES = [
    {
        "case_id": "pilot-001", "pdb_id": "1STP",
        "candidates": "data/strict_subpilot.csv",
        "ligand_manifest": "data/ligand_preparation_manifest.csv",
        "runs": "data/vina_run_manifest.csv",
        "rmsd": "data/reference_pose_rmsd.csv",
    },
    {
        "case_id": "pilot-007", "pdb_id": "3D4Q",
        "candidates": "data/strict_subpilot.csv",
        "ligand_manifest": "data/ligand_preparation_manifest.csv",
        "runs": "data/vina_run_manifest.csv",
        "rmsd": "data/reference_pose_rmsd.csv",
    },
    {
        "case_id": "pilot-008", "pdb_id": "3CJO",
        "candidates": "data/contextual_batch_04.csv",
        "ligand_manifest": "data/contextual_batch_04_ligand_preparation_manifest.csv",
        "runs": "data/contextual_batch_04_vina_run_manifest.csv",
        "rmsd": "data/contextual_batch_04_reference_pose_rmsd.csv",
    },
    {
        "case_id": "pilot-006", "pdb_id": "3PTB",
        "candidates": "data/contextual_batch_05.csv",
        "ligand_manifest": "data/contextual_batch_05_ligand_preparation_manifest.csv",
        "runs": "data/contextual_batch_05_vina_run_manifest.csv",
        "rmsd": "data/contextual_batch_05_reference_pose_rmsd.csv",
    },
    {
        "case_id": "pilot-002", "pdb_id": "1HVR",
        "candidates": "data/contextual_batch_06.csv",
        "ligand_manifest": "data/contextual_batch_06_ligand_preparation_manifest.csv",
        "runs": "data/contextual_batch_06_vina_run_manifest.csv",
        "rmsd": "data/contextual_batch_06_reference_pose_rmsd.csv",
    },
    {
        "case_id": "pilot-003", "pdb_id": "1IEP",
        "candidates": "data/contextual_batch_07.csv",
        "ligand_manifest": "data/contextual_batch_07_ligand_preparation_manifest.csv",
        "runs": "data/contextual_batch_07_vina_run_manifest.csv",
        "rmsd": "data/contextual_batch_07_reference_pose_rmsd.csv",
    },
    {
        "case_id": "expansion-001", "pdb_id": "1B9V",
        "candidates": "data/contextual_batch_08.csv",
        "ligand_manifest": "data/contextual_batch_08_ligand_preparation_manifest.csv",
        "runs": "data/contextual_batch_08_vina_run_manifest.csv",
        "rmsd": "data/contextual_batch_08_reference_pose_rmsd.csv",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pocket_backbone(case_id: str, pdb_id: str, receptor_chain: str, center: np.ndarray, radius: float = 9.0) -> np.ndarray:
    structure = gemmi.read_structure(f"raw/structures/{case_id}_{pdb_id}.cif")
    model = structure[0]
    chain = model.find_chain(receptor_chain)
    points = []
    for residue in chain:
        ca = residue.find_atom("CA", "*")
        if ca is None:
            continue
        pos = np.array([ca.pos.x, ca.pos.y, ca.pos.z])
        if np.linalg.norm(pos - center) <= radius:
            points.append(pos)
    return np.array(points)


def mol_to_lines(mol: Chem.Mol, conf_id: int = 0) -> tuple[np.ndarray, list[tuple[int, int]]]:
    conf = mol.GetConformer(conf_id)
    positions = np.array([list(conf.GetAtomPosition(i)) for i in range(mol.GetNumAtoms())])
    bonds = [(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()) for bond in mol.GetBonds()]
    return positions, bonds


def draw_mol(axis, positions: np.ndarray, bonds: list[tuple[int, int]], color: str, label: str) -> None:
    for start, end in bonds:
        axis.plot(*zip(positions[start], positions[end]), color=color, linewidth=2.4, zorder=5)
    axis.scatter(positions[:, 0], positions[:, 1], positions[:, 2], color=color, s=26, label=label, zorder=6, edgecolor="white", linewidth=0.4)


def render_case(case: dict[str, str], output_dir: Path) -> str:
    candidates = {row["case_id"]: row for row in read_csv(Path(case["candidates"]))}
    ligands = {row["case_id"]: row for row in read_csv(Path(case["ligand_manifest"])) if row["status"] == "prepared"}
    runs = {row["case_id"]: row for row in read_csv(Path(case["runs"])) if row["status"] == "completed"}
    rmsd_rows = [row for row in read_csv(Path(case["rmsd"])) if row["case_id"] == case["case_id"]]

    case_id = case["case_id"]
    pdb_id = case["pdb_id"]
    component = ligands[case_id]["component_id"]
    receptor_chain = candidates[case_id]["receptor_chain"]

    reference = reference_molecule(case_id, pdb_id, component, candidates, Path("raw"))
    ref_positions, ref_bonds = mol_to_lines(reference)
    center = ref_positions.mean(axis=0)

    pdbqt_path = Path(runs[case_id]["output_path"])
    poses = RDKitMolCreate.from_pdbqt_mol(PDBQTMolecule(pdbqt_path.read_text(encoding="utf-8")))[0]
    docked = Chem.RemoveHs(poses)
    top_positions, top_bonds = mol_to_lines(docked, conf_id=0)

    backbone = pocket_backbone(case_id, pdb_id, receptor_chain, center)

    verified = [row for row in rmsd_rows if row["mapping_status"] == "verified" and row["mode"] == "1"]
    rmsd_label = f"{float(verified[0]['experimental_reference_heavy_atom_rmsd_angstrom']):.2f} Å" if verified else "not verified"

    figure = plt.figure(figsize=(6.4, 6.0))
    axis = figure.add_subplot(111, projection="3d")
    if len(backbone):
        axis.plot(backbone[:, 0], backbone[:, 1], backbone[:, 2], color=GRAY, linewidth=1.1, alpha=0.75, zorder=1)
        axis.scatter(backbone[:, 0], backbone[:, 1], backbone[:, 2], color=GRAY, s=8, alpha=0.55, zorder=1, label="Receptor backbone (Cα, chain " + receptor_chain + ")")
    draw_mol(axis, ref_positions, ref_bonds, TEAL, f"Experimental {component}")
    draw_mol(axis, top_positions, top_bonds, CORAL, "Vina top pose")

    axis.set_title(f"{case_id} — {pdb_id} / {component}\ntop-score RMSD to experiment: {rmsd_label}", fontsize=10.5, color=NAVY)
    axis.set_xticks([]); axis.set_yticks([]); axis.set_zticks([])
    for pane in (axis.xaxis, axis.yaxis, axis.zaxis):
        pane.pane.set_visible(False)
    axis.legend(loc="upper left", fontsize=7.5, frameon=False)
    figure.tight_layout()

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = output_dir / f"binding-site-{case_id}-{pdb_id}"
    figure.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    figure.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    plt.close(figure)
    return f"{case_id} ({pdb_id}): rendered, RMSD {rmsd_label}"


def main() -> int:
    output_dir = Path("reports/generated/figures/binding-sites")
    for case in CASES:
        print(render_case(case, output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
