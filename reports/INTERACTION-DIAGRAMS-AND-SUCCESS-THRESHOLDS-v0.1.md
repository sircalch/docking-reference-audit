# 2D interaction diagrams and standard success-threshold classification v0.1

## Scope

Two new, publication-oriented outputs built from data already computed and
verified elsewhere in this project — no new measurement, only new
visualizations/classifications of existing numbers:

1. Schematic 2D ligand-receptor interaction diagrams (LigPlot+/PLIP-style)
   for the top-scoring pose of all 7 completed docking cases.
2. Classification of each case's RMSD against the standard success
   thresholds used in docking-methodology benchmarking literature.

## 1. Interaction diagrams

`scripts/render_interaction_diagrams.py` draws the real 2D bond skeleton of
each docked ligand (RDKit-generated depiction of the same identity-verified
molecule graph used throughout this project) with the contacting receptor
residues arranged around it: green dashed lines mark hydrogen-bond
candidates (donor-acceptor distance <= 3.5 A, from
`data/hydrogen_bonds_top_pose.csv`), red lines mark other non-bonded
contacts within the 4.5 A cutoff (from
`data/interface_contacts_top_pose.csv`). Every residue, distance, and bond
drawn is real data already reported in
`reports/INTERFACE-CONTACTS-v0.1.md`.

As with LigPlot+ and PLIP themselves, residue placement around the ligand
is a schematic layout for readability (ordered by contact distance), not a
to-scale projection of the real 3D geometry — the distances labelled on
each line are the real, quantitative claim; the diagram's geometry is not.

Output: `reports/generated/figures/interaction-diagrams/interaction-diagram-<case>-<PDB>.svg`/`.png`,
one per completed case (7 total).

## 2. Success-threshold classification

`scripts/compute_success_thresholds.py` re-derives, from the already
committed `data/*_reference_pose_rmsd.csv` files (all Vina poses, all
batches), the top-scoring-pose RMSD and the best RMSD found in any pose for
each of the 6 verified cases, then classifies each against the RMSD
thresholds conventionally reported in docking-benchmark literature
(<=1.0 A, <=2.0 A, <=3.0 A; <=2.0 A is the threshold most commonly used as
the de facto "correct pose" cutoff in benchmarking campaigns such as CASF).

| Case | PDB | Top-score RMSD (Å) | Best RMSD (Å) | ≤1.0 Å | ≤2.0 Å | ≤3.0 Å |
| --- | --- | ---: | ---: | :---: | :---: | :---: |
| pilot-001 | 1STP | 0.689 | 0.689 | yes | yes | yes |
| pilot-007 | 3D4Q | 0.769 | 0.769 | yes | yes | yes |
| expansion-001 | 1B9V | 0.930 | 0.591 | yes | yes | yes |
| pilot-008 | 3CJO | 1.504 | 1.154 | no | yes | yes |
| pilot-002 | 1HVR | 2.493 | 1.664 | no | yes | yes |
| pilot-006 | 3PTB | 5.594 | 5.578 | no | no | no |
| pilot-003 (1IEP) | — | — | — | not verified | not verified | not verified |

At the conventional <=2.0 A threshold, 5 of the 6 verified cases succeed
(83%); pilot-006/3PTB is the one case that fails at every threshold tested,
consistent with the "right pocket, wrong orientation" characterization
already established by `reports/INTERFACE-CONTACTS-v0.1.md` (correct S1
pocket residues) and `reports/SASA-BURIAL-v0.1.md` (physically reasonable
buried area). pilot-003/1IEP is excluded from this classification, not
counted as a failure, because its RMSD was never verified in the first
place (PDBQT pose-count mismatch).

## Interpretation boundary

A 6-case sample is not a statistically powered benchmark and this
percentage should not be read as an estimate of general strict-preparation
redocking performance — it describes exactly these 6 cases, consistent
with the rest of this project's small, individually-justified sample.

## Machine-readable evidence

- `data/success_thresholds.csv`;
- `reports/generated/figures/interaction-diagrams/*.svg`/`.png`;
- `scripts/render_interaction_diagrams.py`, `scripts/compute_success_thresholds.py`
  — both reproduce these outputs from data already versioned in this
  repository.
