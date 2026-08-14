#!/usr/bin/env python3
"""Real buried surface area (ΔSASA) upon complex formation, all 7 cases.

Computes solvent-accessible surface area (SASA, Shrake-Rupley algorithm,
1973) for the receptor alone, the top-scoring (mode 1) docked ligand pose
alone, and the two combined, from real atomic coordinates. The buried
interface area is DeltaSASA = SASA(receptor) + SASA(ligand) - SASA(complex).

Algorithm (deterministic Fibonacci-spiral sphere sampling, van der Waals +
probe radius, point-in-any-other-sphere occlusion test) is an intentional
parity match with the scAMH platform's
src/features/sasa-surface/sasaAnalysis.ts, reimplemented independently here
in Python/NumPy (vectorized for tractable runtime on receptors with
thousands of heavy atoms) so this repository has no code dependency on that
platform.

Known, declared limitation shared with any Shrake-Rupley implementation
(including professional tools such as FreeSASA): finite point sampling per
sphere means the result converges to, but does not exactly equal, the
analytic SASA; it is not an implementation error. Probe radius 1.4 A (water),
Bondi (1964) van der Waals radii, 200 points per sphere. Heavy atoms only
(hydrogens not modeled in these strict-prepared receptors or ligand poses).
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


PROBE_RADIUS_ANGSTROM = 1.4
POINTS_PER_SPHERE = 200

# Bondi (1964) van der Waals radii, Angstrom. Fallback 1.70 (carbon) for any
# unlisted heavy element actually encountered.
BONDI_RADII = {
    "C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80, "P": 1.80,
    "F": 1.47, "CL": 1.75, "BR": 1.85, "I": 1.98,
    "FE": 1.63, "ZN": 1.39, "MG": 1.73, "CA": 2.31, "MN": 1.61, "CU": 1.40,
    "NA": 2.27, "K": 2.75,
}
DEFAULT_RADIUS = 1.70


def fibonacci_sphere_points(n: int) -> np.ndarray:
    points = np.empty((n, 3))
    golden_angle = math.pi * (3 - math.sqrt(5))
    i = np.arange(n)
    y = 1 - (i / (n - 1)) * 2
    radius_at_y = np.sqrt(np.clip(1 - y * y, 0, None))
    theta = golden_angle * i
    points[:, 0] = np.cos(theta) * radius_at_y
    points[:, 1] = y
    points[:, 2] = np.sin(theta) * radius_at_y
    return points


UNIT_SPHERE = fibonacci_sphere_points(POINTS_PER_SPHERE)


def compute_sasa(centers: np.ndarray, radii: np.ndarray, probe_radius: float = PROBE_RADIUS_ANGSTROM) -> float:
    n = centers.shape[0]
    expanded = radii + probe_radius
    total = 0.0
    for i in range(n):
        r = expanded[i]
        sphere_points = centers[i] + UNIT_SPHERE * r  # (P, 3)
        # distance^2 from each sphere point to every other atom center
        diff = sphere_points[:, None, :] - centers[None, :, :]  # (P, N, 3)
        dist_sq = np.einsum("pnc,pnc->pn", diff, diff)  # (P, N)
        occluded_by = dist_sq < (expanded ** 2)[None, :]
        occluded_by[:, i] = False
        buried = occluded_by.any(axis=1)
        exposed_fraction = 1.0 - buried.mean()
        total += exposed_fraction * 4 * math.pi * r * r
    return total


def parse_pdb_heavy_atoms(text: str) -> tuple[np.ndarray, np.ndarray]:
    coords = []
    radii = []
    for line in text.splitlines():
        if not (line.startswith("ATOM") or line.startswith("HETATM")):
            continue
        try:
            atom_name = line[12:16].strip()
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            element_raw = line[76:78].strip()
        except (ValueError, IndexError):
            continue
        element = (element_raw or "".join(c for c in atom_name if not c.isdigit())[:2]).upper()
        if element == "H":
            continue
        coords.append((x, y, z))
        radii.append(BONDI_RADII.get(element, DEFAULT_RADIUS))
    return np.array(coords), np.array(radii)


def first_pose_block(pdbqt_text: str) -> str:
    blocks = pdbqt_text.split("MODEL")
    block = blocks[1] if len(blocks) > 1 else pdbqt_text
    return block.split("ENDMDL")[0]


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
    parser.add_argument("--output", type=Path, default=Path("data/sasa_burial_top_pose.csv"))
    args = parser.parse_args()

    rows = []
    for case in CASES:
        rec_coords, rec_radii = parse_pdb_heavy_atoms(Path(case["receptor"]).read_text(encoding="utf-8"))
        pose_text = first_pose_block(Path(case["poses"]).read_text(encoding="utf-8"))
        lig_coords, lig_radii = parse_pdb_heavy_atoms(pose_text)

        sasa_receptor = compute_sasa(rec_coords, rec_radii)
        sasa_ligand = compute_sasa(lig_coords, lig_radii)
        complex_coords = np.vstack([rec_coords, lig_coords])
        complex_radii = np.concatenate([rec_radii, lig_radii])
        sasa_complex = compute_sasa(complex_coords, complex_radii)
        buried = sasa_receptor + sasa_ligand - sasa_complex

        rows.append({
            "case_id": case["case_id"], "pdb_id": case["pdb_id"],
            "receptor_heavy_atoms": rec_coords.shape[0], "ligand_heavy_atoms": lig_coords.shape[0],
            "sasa_receptor_alone_A2": round(sasa_receptor, 1),
            "sasa_ligand_alone_A2": round(sasa_ligand, 1),
            "sasa_complex_A2": round(sasa_complex, 1),
            "buried_interface_area_A2": round(buried, 1),
        })
        print(f"{case['case_id']} {case['pdb_id']}: buried interface = {buried:.1f} A^2 "
              f"(receptor {sasa_receptor:.0f} + ligand {sasa_ligand:.0f} - complex {sasa_complex:.0f})")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
