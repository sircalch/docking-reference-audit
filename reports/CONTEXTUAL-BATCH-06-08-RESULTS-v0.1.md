# Contextual execution batches 06-08 — strict preparation and reference-pose results v0.1

## Scope

This report covers three contextual cases processed together in one round,
all using the retained-component mechanism first built for pilot-008 (3CJO):
pilot-002 (1HVR, HIV protease with the cyclic-urea inhibitor XK2), pilot-003
(1IEP, c-Abl kinase with imatinib/STI), and expansion-001 (1B9V, influenza
neuraminidase with the inhibitor RA2). A fourth case processed in the same
round, expansion-005 (1KZK), failed strict preparation and is recorded only
in `reports/STRICT-PREPARATION-SUMMARY-v0.1.md`. This is a feasibility
report, not a docking-performance benchmark, binding-affinity estimate, or
biological validation.

## Declared policies

- **pilot-002 (1HVR):** two polymer chains (HIV protease is a homodimer);
  ligand instance A:XK2:263 selected by minimum ligand-to-polymer contact
  distance (2.209 Å). The other non-polymer component, CSO:2
  (S-hydroxycysteine), was inspected directly in the deposited mmCIF and
  found to be a covalently modified residue at auth_seq_id 67 in both chains
  (`covale` bonds Ile66-C to Cys67-N and Cys67-C to Gly68-N, annotated as a
  named protein modification), not a free ligand — the same pattern already
  established for CSS in 9HOO. Retained as part of the receptor chain; only
  water and the declared ligand XK2 were removed.
- **pilot-003 (1IEP):** two polymer chains; ligand instance A:STI:201
  selected the same way (2.668 Å). The other non-polymer component, CL:6, is
  registered as its own separate non-polymer entity (crystallization/buffer
  chloride ions) with no documented catalytic or structural role in c-Abl
  kinase. Stripped along with water and the declared ligand, matching the
  default clean-case policy — no retention needed here.
- **expansion-001 (1B9V):** single chain; ligand instance A:RA2:468 selected
  the same way (2.758 Å). Two other components: CA:2 (retained — influenza
  neuraminidase's well-characterized structural calcium-binding site,
  distinct from the sialic-acid-mimetic pocket where RA2 binds) and NAG:1
  (stripped — verified directly to carry no `covale` bond records to the
  polymer chain in the deposited mmCIF, unlike the CSO/CSS cases, so treated
  as an unlinked, non-catalytic occupant rather than glycosylation).

All three retention/stripping decisions were verified empirically by
inspecting the extracted receptor PDBs directly, not assumed: 1HVR retains
15 CSO-associated atoms with zero XK2/HOH atoms; 1B9V retains 2 CA atoms
with zero NAG/RA2/HOH atoms; 1IEP retains zero STI/CL/HOH atoms.

## Strict receptor preparation

All three were extracted and passed to Meeko 0.7.1 under the same no-repair
policy as every other case (no alternate-location choice, no repair, no
residue deletion, no template addition, `--allow_bad_res` never enabled).

**All three prepared successfully** — bringing the cumulative prepared-receptor
count in the audit to 7 of 23 attempts (30%).

## Ligand preparation and docking

Each ligand was retrieved from RCSB, prepared with Meeko 0.7.1, and docked
with AutoDock Vina 1.2.5 under the same frozen protocol used throughout this
audit (WSL, seed 20260812, one CPU, exhaustiveness 8, box derived from the
experimental ligand coordinates).

| Case | PDB | Ligand | Top-score affinity (kcal/mol) | Top-score RMSD (Å) | Best RMSD (Å) | Status |
| --- | --- | --- | ---: | ---: | ---: | --- |
| pilot-002 | 1HVR | XK2 | -6.033 | 2.493 | 1.664 (mode 2) | verified, weak recovery |
| pilot-003 | 1IEP | STI | -12.68 | — | — | **not verified — see below** |
| expansion-001 | 1B9V | RA2 | -7.501 | 0.930 | 0.591 (mode 9) | verified, strong recovery |

expansion-001/1B9V is the third case in the audit (after 1STP and 3D4Q) with
sub-1-Å reference-pose recovery, and the first among the contextual cases to
reach that level. pilot-002/1HVR completed and produced a verified RMSD but
did not recover the pose closely — a third distinct outcome tier alongside
the strong (1STP, 3D4Q, 1B9V), moderate (3CJO), and failed (3PTB) cases
already in the audit.

### pilot-003 (1IEP): a genuine verification failure, reported as such

Vina's log reported 9 scored poses (`data/contextual_batch_07_vina_pose_scores.csv`
has 9 rows, affinities -12.68 to -8.468 kcal/mol), but the corresponding
output PDBQT file (`derived/vina-runs/pilot-003_1IEP_out.pdbqt`) contains
only 4 `MODEL` blocks, confirmed both by direct grep of the file and by
independently parsing it with Meeko's `PDBQTMolecule`/`RDKitMolCreate` (4
conformers). `calculate_reference_pose_rmsd.py` correctly refused to compute
RMSD under this mismatch (`mapping_status = not_verified`, note: "PDBQT pose
count differs from parsed Vina score count") rather than silently pairing
scores to the wrong poses. No repair or re-run with different settings was
attempted, consistent with the audit's run-once, no-retry policy; this is
recorded as an unresolved technical outcome for imatinib/1IEP specifically,
not extrapolated to any other case.

## Interpretation boundary

With this round, the audit has 7 completed docking runs total (adding these
three to the four already reported): three strong recoveries under 1 Å
(1STP, 3D4Q, 1B9V), one moderate recovery (3CJO, 1.1-1.5 Å), one weak
recovery (1HVR, 1.7-2.5 Å), one failed recovery (3PTB, ~5.6 Å), and one
technically unverifiable case (1IEP). This spread — rather than a single
number — is the honest picture at this sample size and must not be averaged
into an accuracy estimate or extrapolated to other receptors, ligands, or
preparation policies.

## Machine-readable evidence

- `data/contextual_batch_06.csv`, `_07.csv`, `_08.csv` (declared policies);
- `data/contextual_batch_{06,07,08}_receptor_extraction_manifest.csv`;
- `data/contextual_batch_{06,07,08}_preparation_manifest.csv`;
- `data/contextual_batch_{06,07,08}_ligand_preparation_manifest.csv`;
- `data/contextual_batch_{06,07,08}_box_manifest.csv`;
- `data/contextual_batch_{06,07,08}_vina_run_manifest.csv`;
- `data/contextual_batch_{06,07,08}_vina_pose_scores.csv`;
- `data/contextual_batch_{06,08}_reference_pose_rmsd.csv` (verified);
- `data/contextual_batch_07_reference_pose_rmsd.csv` (not verified, pose-count
  mismatch, recorded in full rather than omitted);
- `data/contextual_batch_09.csv` and `data/contextual_batch_09_preparation_manifest.csv`
  (expansion-005/1KZK, failed strict preparation, recorded only in
  `reports/STRICT-PREPARATION-SUMMARY-v0.1.md`).

Tracked separately from the original two-case subpilot evidence, which
`scripts/verify_subpilot_evidence.py` continues to check unchanged ("2
completed runs; 18 score rows; 18 RMSD rows").
