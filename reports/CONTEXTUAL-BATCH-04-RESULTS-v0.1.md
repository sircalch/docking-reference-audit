# Contextual execution batch 04 — strict preparation and reference-pose result v0.1

## Scope

This report covers the third completed reference-pose case in the audit,
pilot-008 (PDB 3CJO), processed under an explicit retained-component policy
rather than the default clean-case policy. It is a feasibility case, not a
docking-performance benchmark, binding-affinity estimate, or biological
validation.

## Declared policy

3CJO ("Crystal structure of KSP in complex with inhibitor 30") has two
polymer chains, two declared ligand (K30) instances, and two other
non-polymer components per chain: ADP and MG. Receptor chain B and ligand
instance B:K30:603 were selected by the minimum original-coordinate
ligand-to-polymer atom distance (2.268 A), the same rule used throughout this
audit (`scripts/propose_case_policies.py`).

Unlike every prior case, this policy explicitly **retains** ADP and MG rather
than stripping them: KSP/Eg5 is a kinesin motor protein with a well
characterized ATP/ADP-Mg nucleotide pocket that is structurally and
functionally distinct from the allosteric pocket where K30 binds. Removing a
resolved physiological cofactor would alter the chemistry of the receptor
beyond what a no-repair, no-deletion policy permits; retaining it is the more
conservative choice. Only water and the declared ligand (K30) were removed.

This required extending `scripts/extract_strict_receptors.py` with an
optional `retained_components` column (`data/contextual_batch_04.csv`). When
empty, extraction is byte-identical in intent to the original
`remove_ligands_and_waters()` call used by every clean case; when populated,
extraction removes water and the declared ligand only, keeping named
non-polymer residues untouched. The declared policy was verified empirically,
not assumed: the extracted receptor PDB was inspected directly and confirmed
to contain all 27 ADP atoms and the MG ion, zero K30 atoms, and zero water
atoms.

## Strict receptor preparation

Extraction and Meeko 0.7.1 preparation used the same no-repair pipeline as
every other case, with no alternate-location choice, no repair, no residue
deletion, no template addition, and `--allow_bad_res` never enabled.

**Outcome: prepared.** This is the third successful strict preparation in
the audit, alongside pilot-001 (1STP) and pilot-007 (3D4Q) from the original
subpilot.

## Ligand preparation and docking

The RCSB ideal SDF for K30 was retrieved and prepared with Meeko 0.7.1
(prepared). AutoDock Vina 1.2.5 was run through WSL with the same fixed
protocol used throughout this audit (seed 20260812, one CPU, exhaustiveness
8, box derived from the experimental ligand coordinates). All nine requested
poses were retained.

| Mode | Affinity (kcal/mol) | RMSD to experiment (Å) |
| --- | ---: | ---: |
| 1 | -10.89 | 1.504 |
| 2 | -10.71 | 1.154 |
| 3 | -10.10 | 1.796 |
| 4 | -9.803 | 1.284 |
| 5 | -9.761 | 1.677 |
| 6 | -9.577 | 2.266 |
| 7 | -9.050 | 2.218 |
| 8 | -8.722 | 2.134 |
| 9 | -8.509 | 1.626 |

RMSD to experiment is identity-mapped, aligned, heavy-atom RMSD after
verifying RCSB CCD-to-SDF atom order, matching heavy-atom sets, isomeric
heavy-atom SMILES, and pose count (`data/contextual_batch_04_reference_pose_rmsd.csv`,
mapping_status "verified" for all nine poses). It is distinct from Vina's own
internal pose-to-best-pose RMSD.

Vina's top-scoring pose (mode 1, -10.89 kcal/mol) recovered the experimental
ligand position to 1.504 Å; the closest pose to experiment across all nine
(mode 2, -10.71 kcal/mol, effectively tied for top score) was 1.154 Å. Both
values are higher than the two original-subpilot cases (0.689 Å and 0.769 Å)
but still well under the pocket scale of the ligand itself, and were achieved
with a genuine physiological cofactor present in the receptor rather than an
empty pocket.

## Interpretation boundary

This is a single additional case. It does not change the audit's central,
already-reported finding that strict no-repair preparation succeeds in a
minority of attempts (now 3 of 18, 17%) and fails predominantly on alternate
locations (14 of 15 failures). It does show that the retained-component
extension is mechanically correct and that opening the contextual route can,
in at least one case with a real, chemically justified retention decision,
produce a new verified reference-pose result — which the two prior
contextual attempts (both pure strip-to-declared-chain cases) did not.

## Machine-readable evidence

- `data/contextual_batch_04.csv` (declared policy, including retained
  components);
- `data/contextual_batch_04_receptor_extraction_manifest.csv`;
- `data/contextual_batch_04_preparation_manifest.csv`;
- `data/contextual_batch_04_ligand_preparation_manifest.csv`;
- `data/contextual_batch_04_box_manifest.csv`;
- `data/contextual_batch_04_vina_run_manifest.csv`;
- `data/contextual_batch_04_vina_pose_scores.csv`;
- `data/contextual_batch_04_reference_pose_rmsd.csv`.

This batch's evidence is tracked separately from the original two-case
subpilot evidence (`data/reference_pose_rmsd.csv`,
`data/vina_pose_scores.csv`), which `scripts/verify_subpilot_evidence.py`
continues to check unchanged ("2 completed runs; 18 score rows; 18 RMSD
rows"). The audit now has three completed reference-pose cases in total,
reported together in `reports/AUDIT-SYNTHESIS-v0.1.md`.
