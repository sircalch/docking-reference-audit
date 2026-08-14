# Contextual execution batch 05 — strict preparation and reference-pose result v0.1

## Scope

This report covers pilot-006 (PDB 3PTB, bovine trypsin with the benzamidine
inhibitor BEN), the fourth prepared receptor and fourth completed docking run
in the audit, processed under a retained-component policy. It is a
feasibility case, not a docking-performance benchmark, binding-affinity
estimate, or biological validation.

## Declared policy

3PTB is a single-chain structure with one declared ligand (BEN) instance and
one other non-polymer component, CA (a calcium ion). Receptor chain A and
ligand instance A:BEN:1 were selected by the minimum original-coordinate
ligand-to-polymer atom distance (2.815 A). The calcium ion occupies trypsin's
well-characterized structural calcium-binding loop (Bode and Schwager, 1975),
distinct from the S1 catalytic pocket where benzamidine binds, and stabilizes
the fold rather than participating in inhibitor binding. It was retained
(`data/contextual_batch_05.csv`, `retained_components=CA`) rather than
stripped, using the same extraction-script extension built for pilot-008.
Only water and the declared ligand BEN were removed. Verified empirically:
the extracted receptor PDB retains one CA atom, zero BEN atoms, zero water
atoms.

## Strict receptor preparation

Extraction and Meeko 0.7.1 preparation used the same no-repair pipeline as
every other case. **Outcome: prepared** — the fourth successful strict
preparation in the audit (after pilot-001/1STP, pilot-007/3D4Q, and
pilot-008/3CJO).

## Ligand preparation and docking

The RCSB ideal SDF for BEN was retrieved and prepared with Meeko 0.7.1
(prepared). AutoDock Vina 1.2.5 was run through WSL with the same fixed
protocol used throughout this audit (seed 20260812, one CPU, exhaustiveness
8, box derived from the experimental ligand coordinates: 20.0 x 20.0 x 20.5
A). All nine requested poses were retained.

| Mode | Affinity (kcal/mol) | RMSD to experiment (Å) |
| --- | ---: | ---: |
| 1 | -6.058 | 5.594 |
| 2 | -6.048 | 5.593 |
| 3 | -4.944 | 5.601 |
| 4 | -4.931 | 5.580 |
| 5 | -4.783 | 5.578 |
| 6 | -4.349 | 5.585 |
| 7 | -4.152 | 5.585 |
| 8 | -3.937 | 5.578 |
| 9 | -3.901 | 5.578 |

All nine RMSD values were identity-mapped and verified (CCD-to-SDF element
order, experimental heavy atoms, isomeric SMILES, pose count all confirmed;
`mapping_status = verified` for every row,
`data/contextual_batch_05_reference_pose_rmsd.csv`).

## This is a negative pose-recovery result, reported as such

Unlike the three prior completed cases, **no pose in this run recovered the
experimental position**: every RMSD is approximately 5.6 A, essentially
uniform across all nine poses regardless of score. Strict receptor
preparation succeeded and the docking run completed without error, but the
docked poses did not converge on the crystallographic benzamidine site under
this frozen protocol (fixed seed, exhaustiveness 8, box derived automatically
from the experimental ligand coordinates with 8 A padding). Benzamidine is a
very small ligand (9 heavy atoms) bound in a narrow, deep S1 pocket; this
combination is a plausible source of the discrepancy, but no repair,
re-parameterization, box adjustment, or seed change was applied to test that
explanation, consistent with the audit's frozen, no-retry policy. This
negative result is recorded in full rather than omitted, per the project's
transparency commitment: a successful strict preparation does not imply
accurate reference-pose recovery, and this audit reports both outcomes on
equal footing.

## Interpretation boundary

With this case, the audit now has four completed docking runs (pose
generation plus verified experimental-reference RMSD): two with sub-1-A
recovery (1STP, 3D4Q), one with ~1.1-1.5 A recovery under a genuine cofactor
context (3CJO), and one with no meaningful recovery (3PTB). This spread is
itself the honest picture at n=4 and must not be averaged into a single
"accuracy" figure or extrapolated to other receptors, ligands, or box/seed
configurations.

## Machine-readable evidence

- `data/contextual_batch_05.csv` (declared policy, including retained
  components);
- `data/contextual_batch_05_receptor_extraction_manifest.csv`;
- `data/contextual_batch_05_preparation_manifest.csv`;
- `data/contextual_batch_05_ligand_preparation_manifest.csv`;
- `data/contextual_batch_05_box_manifest.csv`;
- `data/contextual_batch_05_vina_run_manifest.csv`;
- `data/contextual_batch_05_vina_pose_scores.csv`;
- `data/contextual_batch_05_reference_pose_rmsd.csv`.

Tracked separately from the original two-case subpilot evidence, which
`scripts/verify_subpilot_evidence.py` continues to check unchanged ("2
completed runs; 18 score rows; 18 RMSD rows").
