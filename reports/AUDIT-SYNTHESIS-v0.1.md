# Docking reference-pose audit — synthesis v0.1

## Purpose and scope

This report combines, in one place, the inclusion criteria, the full candidate
registry outcome, the strict receptor-preparation results, and the four
completed docking runs produced under protocol v0.1
(`protocol/PROTOCOL-v0.1.md`). It supersedes no other report; it is a synthesis
generated from the same versioned manifests that back `SUBPILOT-RESULTS-v0.1.md`
and `STRICT-PREPARATION-SUMMARY-v0.1.md`.

**This is not a docking-performance benchmark.** It makes no claim about
AutoDock Vina's general accuracy, no claim about Meeko's general robustness,
and no biological-activity, binding-affinity, or clinical inference is drawn
from any score or RMSD reported here. It describes the observed compatibility
of one frozen, no-repair receptor-preparation policy with a declared set of
public RCSB structures.

## Inclusion criteria (frozen)

A candidate qualifies for registration only if, at the time of screening:

- deposition method is X-ray;
- reported resolution is ≤2.0 Å;
- the RCSB entry lists exactly one non-polymer entity, excluding solvent,
  buffer, crystallization additives, and simple ions, verified per-candidate
  via the RCSB Data API rather than trusted from entry-level summary counts
  alone (summary counts alone produced two false positives during discovery,
  see Limitations);
- the reference ligand pose is auditable directly from the deposited
  coordinates;
- a full receptor/ligand/water/cofactor policy can be declared before any
  processing occurs.

Candidates meeting these criteria but containing additional structural
complexity (multiple chains, multiple ligand instances, extra non-polymer
components, glycans/metals) are classified **contextual** and are left
pending a case-specific predeclared policy; they are never processed under
the default clean-case policy. Candidates with a single model, single
declared polymer chain, single ligand instance, and no other non-polymeric
component are classified **clean** and follow the fixed preparation pipeline
described below.

## Candidate registry outcome

The registry reached its documented cap of 30 candidates
(`protocol/EXPANSION-PLAN-v0.1.md`). All 30 were retrieved and checksummed
from RCSB (`data/retrieval_manifest.csv`). Structural classification
(`scripts/classify_structural_eligibility.py`, output in
`data/eligibility_register.csv`) found:

| Stratum | Count |
| --- | ---: |
| clean | 12 |
| contextual | 18 |
| review required | 0 |

All 12 clean cases were carried through strict receptor preparation. Of the
18 contextual cases, five have since been assigned an explicit, auditable
policy and processed: expansion-009/9CY0 and expansion-021/2BT9 (multi-chain,
multi-instance, receptor chain and ligand instance selected by minimum
ligand-to-polymer contact distance), expansion-019/9HOO, whose flagged
"extra non-polymer component" (CSS) was investigated and found to be a
covalently modified in-chain residue rather than a free ligand, pilot-008/3CJO,
whose two extra components (ADP, MG) were retained as the physiological
KSP/Eg5 nucleotide cofactor rather than stripped, and pilot-006/3PTB, whose
extra component (CA) was retained as trypsin's structural calcium-binding
site — see "Strict receptor preparation" below. The remaining 13 contextual
cases have no declared policy and have not been processed.

## Strict receptor preparation

Every clean case was extracted (`scripts/extract_strict_receptors.py`, fixed
policy: single declared chain, all waters and the declared ligand removed)
and passed to Meeko 0.7.1 (`scripts/run_strict_meeko_preparation.py`) with no
alternate-location choice, no repair, no residue deletion, no template
addition, and `--allow_bad_res` never enabled. The three processed contextual cases
used the same extraction and preparation pipeline. For expansion-009 and
expansion-021, receptor chain and ligand instance were selected by the
minimum original-coordinate ligand-to-polymer atom distance, computed by
`scripts/propose_case_policies.py`, rather than an arbitrary default chain.
For expansion-019 (9HOO), the receptor-chain/ligand-instance selection used
the same rule, and the flagged "other non-polymer component" CSS was
investigated directly: it is a covalently modified residue (S-mercaptocysteine)
at auth_seq_id 304 within chain A's own backbone (`covale` bonds to the
flanking Lys303 and His305 in the deposited mmCIF), not a free ligand — it is
only flagged as "non-polymer" because mmCIF records any non-standard residue
as HETATM. The declared policy retained CSS as part of the receptor chain and
removed only water and the declared ligand (U5P); this was confirmed by
inspecting the extracted PDB directly rather than assumed (11 atoms retained
at residue 304, zero U5P/HOH coordinate lines). No extraction-script change
was required for this case.

For pilot-008 (3CJO, "KSP in complex with inhibitor 30"), the extraction
script itself was extended: an optional `retained_components` column was
added so a case can explicitly keep named non-polymer components instead of
the default strip-everything-except-declared-ligand policy. 3CJO's two extra
components, ADP and MG, are the physiological nucleotide cofactor of the KSP
(Eg5) motor domain, bound at a site distinct from the allosteric K30
inhibitor pocket; removing them would have altered pocket chemistry beyond
what a no-repair policy should do, so they were retained and only water and
K30 were removed. This was verified empirically by inspecting the extracted
receptor PDB directly (27 ADP atoms and the MG ion retained, zero K30/HOH
atoms).

pilot-006 (3PTB, bovine trypsin with the benzamidine inhibitor BEN) used the
same mechanism for a second, independently justified retention: CA, trypsin's
well-characterized structural calcium-binding site (Bode and Schwager, 1975),
distinct from the S1 catalytic pocket where benzamidine binds. Verified the
same way: the extracted PDB retains one CA atom, zero BEN/HOH atoms.

| Outcome | Count |
| --- | ---: |
| prepared | 4 |
| failed | 15 |

| Failure class | Count |
| --- | ---: |
| `meeko_alternate_location_requires_choice` | 10 |
| `meeko_alternate_location_and_template_matching_failed` | 4 |
| `meeko_template_matching_failed` | 1 |

Fourteen of the fifteen failures (93%) involve an alternate-location
component. A rejection under this policy is a recorded audit outcome, not
evidence that the underlying PDB entry is defective; it reflects
incompatibility with one specific no-repair preparation choice. Opening the
contextual route produced three further failures (9CY0, 2BT9, 9HOO, all on
the pure alternate-location class, matching the dominant failure mode already
observed across the clean stratum) and two new prepared receptors, pilot-008
and pilot-006, whose retained-cofactor policies are chemically distinct from
every other case in the audit and are the first contextual cases to reach
docking.

**Observation on resolution.** Candidates in this registry were drawn
disproportionately from the sub-1-angstrom stratum of the frozen
clean-discovery ranking (`protocol/CANDIDATE-DISCOVERY-v0.1.md`), because that
stratum dominates the ranking itself. Within the subset of clean cases for
which resolution was recorded at registration time (expansion-013, -014,
-015, -016, -017, -018, -020, -022 — clean batches 04 through 11, all
0.8-0.99 Å), all eight failed strict preparation, and all eight failures
involve an alternate-location component (six on the pure alternate-location
class, two on the combined alternate-location-and-template-matching class).
A deliberate attempt this audit made to find a lower-resolution comparator
(roughly 1.5-2.0 Å) did not locate an eligible clean candidate within the
frozen ranking using reasonable manual sampling effort. This pattern — very
high nominal resolution co-occurring with explicitly modeled alternate
side-chain conformers, which this policy declines to resolve automatically —
is descriptive of the present eight-case sample only and is not a general
claim about resolution and Meeko compatibility.

## Reference-pose recovery (completed cases)

Four cases had both a strictly prepared receptor and a prepared reference
ligand, and were docked with AutoDock Vina 1.2.5 (WSL, fixed seed 20260812,
one CPU, exhaustiveness 8, box derived from the experimental ligand
coordinates). Each retained all nine requested poses.

| Case | PDB | Ligand | Top-score affinity (kcal/mol) | Top-score RMSD to experiment (Å) | Lowest RMSD to experiment (Å) |
| --- | --- | --- | ---: | ---: | ---: |
| pilot-001 | 1STP | BTN (biotin) | -7.244 | 0.689 | 0.689 |
| pilot-007 | 3D4Q | SM5 | -10.960 | 0.769 | 0.769 |
| pilot-008 | 3CJO | K30 | -10.890 | 1.504 | 1.154 |
| pilot-006 | 3PTB | BEN | -6.058 | 5.594 | 5.578 |

RMSD to experiment is identity-mapped, aligned, heavy-atom RMSD after
verifying RCSB CCD-to-SDF atom order, matching heavy-atom sets, isomeric
heavy-atom SMILES, and pose counts. For pilot-001/pilot-007 this is
`data/reference_pose_rmsd.csv`; for pilot-008 and pilot-006 (contextual cases
processed after the original subpilot was frozen) it is the separately
tracked `data/contextual_batch_04_reference_pose_rmsd.csv` and
`data/contextual_batch_05_reference_pose_rmsd.csv`, kept apart specifically
so `scripts/verify_subpilot_evidence.py` continues to check the original
two-case evidence unchanged (see `reports/CONTEXTUAL-BATCH-04-RESULTS-v0.1.md`
and `reports/CONTEXTUAL-BATCH-05-RESULTS-v0.1.md` for the full per-case
results). All four are distinct from the Vina-internal RMSD-to-best-pose
values in the respective pose-score files, which describe pose spread
relative to Vina's own top pose, not recovery of the experimental pose.

pilot-008 and pilot-006 both differ from the original two cases in retaining
a real physiological cofactor (ADP-Mg; a structural Ca2+) rather than a
pocket stripped to the polymer chain alone. The two outcomes diverge sharply:
pilot-008 recovered the experimental pose to 1.1-1.5 Å, close to the original
subpilot's range; pilot-006 did not recover it at all — all nine poses sit at
≈5.6 Å regardless of score, essentially uniform, which for a 9-heavy-atom
ligand (benzamidine) in a deep, narrow pocket suggests the docked poses
converged on a different site or orientation rather than a near-miss of the
true one. No repair, box adjustment, or seed change was applied to
investigate this — the frozen protocol was run once and the result is
reported as obtained. With n=4 (two strong recoveries, one moderate, one
failed), this remains far too small a sample to draw a recovery-rate
conclusion, and none of it should be extrapolated to other receptors,
ligands, or preparation policies. It does establish, within this audit, that
successful strict preparation and successful reference-pose recovery are
separate outcomes that must be reported independently rather than assumed to
track together.

## What this audit does not yet cover

- **13 of 18 contextual candidates remain unprocessed.** Five
  (expansion-009/9CY0, expansion-021/2BT9, expansion-019/9HOO, pilot-008/3CJO,
  pilot-006/3PTB) were processed under an explicit, auditable policy; three
  failed strict preparation (`meeko_alternate_location_requires_choice`) and
  two (pilot-008, pilot-006) succeeded and were carried through to completed
  docking runs — though only pilot-008 recovered the experimental pose. The
  other 13 have no declared policy; most involve genuine free non-polymer
  components (ions, sugars, cofactors) whose retention or removal has not yet
  been decided case by case.
- **No independent reproduction.** No one has re-run the full pipeline from
  an empty checkout to confirm it reproduces 30 candidates → 19 strict
  attempts → 4 successes deterministically end to end.
- **No claim of generality.** Findings describe compatibility with Meeko
  0.7.1 under one specific no-repair policy (with one documented, explicitly
  justified cofactor-retention extension), applied to one specific,
  resolution-skewed candidate pool. They do not describe Meeko, Vina, or
  AutoDock-family tools in general.

## Machine-readable evidence

- `data/candidates.csv`, `data/retrieval_manifest.csv`,
  `data/eligibility_register.csv` — registry and classification;
- `data/strict_preparation_manifest.csv`,
  `data/clean_batch_{01..11}_preparation_manifest.csv`,
  `data/contextual_batch_{01..05}_preparation_manifest.csv` — all 19
  preparation attempts;
- `data/reference_pose_rmsd.csv`, `data/vina_pose_scores.csv` — the original
  two completed reference-pose recoveries;
- `data/contextual_batch_04_reference_pose_rmsd.csv`,
  `data/contextual_batch_04_vina_pose_scores.csv` — the third completed
  docking run (pilot-008, recovered), tracked separately by design;
- `data/contextual_batch_05_reference_pose_rmsd.csv`,
  `data/contextual_batch_05_vina_pose_scores.csv` — the fourth completed
  docking run (pilot-006, did not recover), tracked separately by design;
- `reports/generated/figures/` — figures 01-04, regenerated by
  `scripts/render_audit_figures.py` (see `reports/FIGURE-CATALOG-v0.1.md`);
- `python scripts/verify_subpilot_evidence.py` reproduces the original
  two-case evidence check reported here, unchanged by this round.
