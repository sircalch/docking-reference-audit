# Strict docking-reference subpilot — results v0.1

## Scope

This report is generated from versioned manifests in this repository. It is a feasibility subpilot, not a docking-performance benchmark, binding-affinity estimate, or biological validation.

## Strict receptor preparation

The frozen clean-case subpilot contained 3 receptors. 2 completed strict Meeko preparation and 1 were rejected without repair, residue deletion, manual alternate-location selection, or changed parameters.

| Case | PDB | Outcome | Recorded cause |
|---|---|---|---|
| pilot-001 | 1STP | prepared | — |
| pilot-004 | 1FPU | failed | meeko_template_matching_failed |
| pilot-007 | 3D4Q | prepared | — |

## Eligible Vina executions

2 cases had both a strictly prepared receptor and a prepared reference ligand. Each used AutoDock Vina 1.2.5 through WSL with a fixed seed (20260812), one CPU, exhaustiveness 8, and a box derived from the experimental ligand coordinates. Each completed case retained all nine requested poses.

| Case | PDB | Poses retained | Top-score affinity (kcal/mol) | Top-score RMSD to experiment (Å) | Lowest RMSD to experiment (Å) |
|---|---|---:|---:|---:|---:|
| pilot-001 | 1STP | 9 | -7.244 | 0.689 | 0.689 |
| pilot-007 | 3D4Q | 9 | -10.960 | 0.769 | 0.769 |

## Interpretation boundary

The Vina RMSD values in `data/vina_pose_scores.csv` describe each returned pose relative to Vina's best-scoring pose. They are not RMSD to the experimental ligand pose and must not be interpreted as pose recovery. The experimental-reference values in `data/reference_pose_rmsd.csv` are identity-mapped, aligned heavy-atom RMSD after verifying the RCSB CCD-to-SDF atom order, the experimental heavy atoms, isomeric heavy-atom SMILES and pose counts.

The 1FPU preparation failure is a retained outcome of the strict policy. It must not be converted into a success by enabling `--allow_bad_res` or by manually repairing coordinates within this protocol version.
