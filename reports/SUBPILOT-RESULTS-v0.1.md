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

| Case | PDB | Poses retained | Top-score affinity (kcal/mol) | Lowest-score affinity (kcal/mol) |
|---|---|---:|---:|---:|
| pilot-001 | 1STP | 9 | -7.244 | -4.964 |
| pilot-007 | 3D4Q | 9 | -10.960 | -8.843 |

## Interpretation boundary

The Vina RMSD values in `data/vina_pose_scores.csv` describe each returned pose relative to Vina's best-scoring pose. They are not RMSD to the experimental ligand pose and must not be interpreted as pose recovery. Experimental-reference RMSD remains pending a validated atom-identity map between the crystallographic ligand and the docked PDBQT output.

The 1FPU preparation failure is a retained outcome of the strict policy. It must not be converted into a success by enabling `--allow_bad_res` or by manually repairing coordinates within this protocol version.
