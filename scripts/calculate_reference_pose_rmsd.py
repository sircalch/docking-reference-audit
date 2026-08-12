#!/usr/bin/env python3
"""Calculate verified experimental-reference heavy-atom RMSD for Vina poses.

Identity bridge: RCSB CCD atom order -> RCSB ideal SDF topology -> original
mmCIF atom identifiers.  The bridge is accepted only if CCD/SDF element order,
experimental heavy-atom identities, and isomeric heavy-atom SMILES all agree.
Symmetry-equivalent atoms are resolved by RDKit's best aligned mapping.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import gemmi
from meeko import PDBQTMolecule, RDKitMolCreate
from rdkit import Chem
from rdkit.Chem import rdMolAlign


FIELDS = (
    "case_id", "pdb_id", "component_id", "mode", "affinity_kcal_mol",
    "experimental_reference_heavy_atom_rmsd_angstrom", "mapping_status", "mapping_note",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def ccd_atom_ids(component: str, raw_dir: Path) -> list[tuple[str, str]]:
    block = gemmi.cif.read_file(str(raw_dir / f"{component}.cif")).sole_block()
    loop = block.find(["_chem_comp_atom.atom_id", "_chem_comp_atom.type_symbol"])
    return [(row[0], row[1]) for row in loop]


def experimental_positions(case_id: str, pdb_id: str, component: str, candidates: dict[str, dict[str, str]], raw_dir: Path) -> dict[str, gemmi.Position]:
    structure = gemmi.read_structure(str(raw_dir / "structures" / f"{case_id}_{pdb_id}.cif"))
    label = candidates[case_id]["reference_ligand_instance"]
    chain_name, _, sequence = label.split(":", maxsplit=2)
    chain = structure[0].find_chain(chain_name)
    if chain is None:
        raise ValueError(f"{case_id}: reference chain absent")
    for residue in chain:
        if residue.name == component and str(residue.seqid) == sequence:
            return {atom.name: atom.pos for atom in residue if atom.element.name != "H"}
    raise ValueError(f"{case_id}: declared experimental ligand instance absent")


def reference_molecule(case_id: str, pdb_id: str, component: str, candidates: dict[str, dict[str, str]], raw_dir: Path) -> Chem.Mol:
    sdf = raw_dir / "ligands" / f"{case_id}_{component}_ideal.sdf"
    molecule = Chem.SDMolSupplier(str(sdf), removeHs=False)[0]
    if molecule is None:
        raise ValueError(f"{case_id}: RCSB ideal SDF cannot be read")
    ccd_atoms = ccd_atom_ids(component, raw_dir / "ligands")
    if molecule.GetNumAtoms() != len(ccd_atoms):
        raise ValueError(f"{case_id}: CCD/SDF atom count mismatch")
    sdf_elements = [atom.GetSymbol().upper() for atom in molecule.GetAtoms()]
    ccd_elements = [element.upper() for _, element in ccd_atoms]
    if sdf_elements != ccd_elements:
        raise ValueError(f"{case_id}: CCD/SDF element order mismatch")
    positions = experimental_positions(case_id, pdb_id, component, candidates, raw_dir)
    heavy_ccd = [(index, atom_id, element) for index, (atom_id, element) in enumerate(ccd_atoms) if element.upper() != "H"]
    missing = [atom_id for _, atom_id, _ in heavy_ccd if atom_id not in positions]
    if missing:
        raise ValueError(f"{case_id}: experimental coordinates missing CCD heavy atoms: {','.join(missing)}")
    conformer = molecule.GetConformer()
    for index, atom_id, _ in heavy_ccd:
        position = positions[atom_id]
        conformer.SetAtomPosition(index, (position.x, position.y, position.z))
    return Chem.RemoveHs(molecule)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=Path("data/strict_subpilot.csv"))
    parser.add_argument("--ligand-manifest", type=Path, default=Path("data/ligand_preparation_manifest.csv"))
    parser.add_argument("--runs", type=Path, default=Path("data/vina_run_manifest.csv"))
    parser.add_argument("--scores", type=Path, default=Path("data/vina_pose_scores.csv"))
    parser.add_argument("--raw-dir", type=Path, default=Path("raw"))
    parser.add_argument("--output", type=Path, default=Path("data/reference_pose_rmsd.csv"))
    args = parser.parse_args()
    candidates = {row["case_id"]: row for row in read_csv(args.candidates)}
    components = {row["case_id"]: row["component_id"] for row in read_csv(args.ligand_manifest) if row["status"] == "prepared"}
    runs = {row["case_id"]: row for row in read_csv(args.runs) if row["status"] == "completed"}
    scores: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(args.scores):
        scores.setdefault(row["case_id"], []).append(row)
    rows: list[dict[str, str]] = []
    for case_id in sorted(set(components) & set(runs) & set(scores)):
        run = runs[case_id]
        component = components[case_id]
        try:
            reference = reference_molecule(case_id, run["pdb_id"], component, candidates, args.raw_dir)
            poses = RDKitMolCreate.from_pdbqt_mol(PDBQTMolecule(Path(run["output_path"]).read_text(encoding="utf-8")))[0]
            docked = Chem.RemoveHs(poses)
            if Chem.MolToSmiles(reference, isomericSmiles=True) != Chem.MolToSmiles(docked, isomericSmiles=True):
                raise ValueError(f"{case_id}: heavy-atom isomeric SMILES differ between reference and docked ligand")
            if docked.GetNumConformers() != len(scores[case_id]):
                raise ValueError(f"{case_id}: PDBQT pose count differs from parsed Vina score count")
            rmsds = [rdMolAlign.GetBestRMS(docked, reference, prbId=index, refId=0) for index in range(docked.GetNumConformers())]
            for score, rmsd in zip(sorted(scores[case_id], key=lambda item: int(item["mode"])), rmsds):
                rows.append({
                    "case_id": case_id, "pdb_id": run["pdb_id"], "component_id": component,
                    "mode": score["mode"], "affinity_kcal_mol": score["affinity_kcal_mol"],
                    "experimental_reference_heavy_atom_rmsd_angstrom": f"{rmsd:.6f}",
                    "mapping_status": "verified", "mapping_note": "CCD-to-SDF element order, experimental heavy atoms, isomeric SMILES and pose count verified",
                })
        except (ValueError, KeyError, OSError) as error:
            for score in scores[case_id]:
                rows.append({
                    "case_id": case_id, "pdb_id": run["pdb_id"], "component_id": component,
                    "mode": score["mode"], "affinity_kcal_mol": score["affinity_kcal_mol"],
                    "experimental_reference_heavy_atom_rmsd_angstrom": "", "mapping_status": "not_verified", "mapping_note": str(error),
                })
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} experimental-reference RMSD rows to {args.output}")
    return 0 if rows and all(row["mapping_status"] == "verified" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
