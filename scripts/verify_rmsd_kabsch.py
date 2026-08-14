#!/usr/bin/env python3
"""Independent Kabsch-Horn cross-check of the reported reference-pose RMSD.

For each of the 6 cases with a verified reference-pose RMSD, this
reconstructs the same identity-mapped atom correspondence already computed
and verified by calculate_reference_pose_rmsd.py (RDKit substructure
matching between the experimental reference molecule and the docked
top-scoring pose), then computes the optimal rigid-superposition RMSD
independently with the classical Kabsch algorithm (Kabsch, 1976; SVD form),
implemented here in plain NumPy with no dependency on RDKit's own alignment
routine (rdMolAlign.GetBestRMS, used to produce the numbers this script
checks).

This is a reproducibility cross-check, not a new metric: it deliberately
answers "does a second, independently implemented rigid-alignment algorithm
agree with the number already reported for this case?" A close match is not
proof either implementation is bug-free, but two independent
implementations converging on the same instance of a well-defined
mathematical optimum (the minimum-RMSD rigid superposition for a fixed atom
correspondence) is meaningful corroboration.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from meeko import PDBQTMolecule, RDKitMolCreate
from rdkit import Chem

sys.path.insert(0, str(Path(__file__).parent))
from calculate_reference_pose_rmsd import reference_molecule, read_csv  # noqa: E402


def kabsch_rmsd(p: np.ndarray, q: np.ndarray) -> float:
    """Optimal rigid-superposition RMSD between two matched point sets (Kabsch, SVD form)."""
    p_centered = p - p.mean(axis=0)
    q_centered = q - q.mean(axis=0)
    h = p_centered.T @ q_centered
    u, _, vt = np.linalg.svd(h)
    d = np.sign(np.linalg.det(vt.T @ u.T))
    correction = np.diag([1.0, 1.0, d])
    rotation = vt.T @ correction @ u.T
    p_rotated = (rotation @ p_centered.T).T
    diff = p_rotated - q_centered
    return float(np.sqrt(np.mean(np.sum(diff * diff, axis=1))))


CASES = [
    {"case_id": "pilot-001", "pdb_id": "1STP", "ligand": "BTN", "candidates": "data/strict_subpilot.csv", "runs": "data/vina_run_manifest.csv", "reported_rmsd": 0.689},
    {"case_id": "pilot-007", "pdb_id": "3D4Q", "ligand": "SM5", "candidates": "data/strict_subpilot.csv", "runs": "data/vina_run_manifest.csv", "reported_rmsd": 0.769},
    {"case_id": "expansion-001", "pdb_id": "1B9V", "ligand": "RA2", "candidates": "data/contextual_batch_08.csv", "runs": "data/contextual_batch_08_vina_run_manifest.csv", "reported_rmsd": 0.930},
    {"case_id": "pilot-008", "pdb_id": "3CJO", "ligand": "K30", "candidates": "data/contextual_batch_04.csv", "runs": "data/contextual_batch_04_vina_run_manifest.csv", "reported_rmsd": 1.504},
    {"case_id": "pilot-002", "pdb_id": "1HVR", "ligand": "XK2", "candidates": "data/contextual_batch_06.csv", "runs": "data/contextual_batch_06_vina_run_manifest.csv", "reported_rmsd": 2.493},
    {"case_id": "pilot-006", "pdb_id": "3PTB", "ligand": "BEN", "candidates": "data/contextual_batch_05.csv", "runs": "data/contextual_batch_05_vina_run_manifest.csv", "reported_rmsd": 5.594},
]


def main() -> int:
    output = Path("data/kabsch_rmsd_crosscheck.csv")
    rows = []
    for case in CASES:
        candidates = {row["case_id"]: row for row in read_csv(Path(case["candidates"]))}
        reference = reference_molecule(case["case_id"], case["pdb_id"], case["ligand"], candidates, Path("raw"))

        runs = {row["case_id"]: row for row in read_csv(Path(case["runs"]))}
        pdbqt_path = Path(runs[case["case_id"]]["output_path"])
        poses = RDKitMolCreate.from_pdbqt_mol(PDBQTMolecule(pdbqt_path.read_text(encoding="utf-8")))[0]
        docked = Chem.RemoveHs(poses)

        # Molecular symmetry (e.g. a locally symmetric ring or terminal group)
        # can give more than one valid atom correspondence. GetBestRMS searches
        # all of them; a fair independent cross-check must do the same instead
        # of trusting the first match returned, or it can compare against a
        # needlessly worse correspondence and look like a disagreement that
        # is really just an unexplored symmetry equivalent.
        matches = docked.GetSubstructMatches(reference, uniquify=False, maxMatches=1000)
        if not matches:
            print(f"{case['case_id']}: no substructure match found, skipping")
            continue

        ref_conf = reference.GetConformer(0)
        doc_conf = docked.GetConformer(0)
        ref_pos = np.array([list(ref_conf.GetAtomPosition(i)) for i in range(reference.GetNumAtoms())])

        kabsch_value = min(
            kabsch_rmsd(
                np.array([list(doc_conf.GetAtomPosition(match[i])) for i in range(reference.GetNumAtoms())]),
                ref_pos,
            )
            for match in matches
        )
        delta = kabsch_value - case["reported_rmsd"]
        rows.append({
            "case_id": case["case_id"], "pdb_id": case["pdb_id"],
            "reported_rmsd_angstrom": case["reported_rmsd"],
            "kabsch_crosscheck_rmsd_angstrom": round(kabsch_value, 3),
            "delta_angstrom": round(delta, 3),
        })
        print(f"{case['case_id']} {case['pdb_id']}: reported {case['reported_rmsd']:.3f} A | "
              f"Kabsch cross-check {kabsch_value:.3f} A | delta {delta:+.3f} A")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
