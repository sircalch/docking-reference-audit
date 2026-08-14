# Docking reference-pose audit — synthesis v0.1

## Purpose and scope

This report combines, in one place, the inclusion criteria, the full candidate
registry outcome, the strict receptor-preparation results, and the seven
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
18 contextual cases, nine have since been assigned an explicit, auditable
policy and processed: expansion-009/9CY0 and expansion-021/2BT9 (multi-chain,
multi-instance, receptor chain and ligand instance selected by minimum
ligand-to-polymer contact distance), expansion-019/9HOO and pilot-002/1HVR,
both flagged for an "extra non-polymer component" that turned out to be a
covalently modified in-chain residue (CSS and CSO respectively) rather than a
free ligand, pilot-008/3CJO (retained ADP/MG, the physiological KSP/Eg5
nucleotide cofactor), pilot-006/3PTB (retained CA, trypsin's structural
calcium-binding site), pilot-003/1IEP (its extra component, CL, is a
genuine crystallization ion and was stripped under the default policy, no
retention needed), expansion-001/1B9V (retained CA, influenza neuraminidase's
structural calcium site, while stripping NAG after verifying it carries no
covalent bond to the polymer), and expansion-005/1KZK (its extra components,
CL and EDO, are crystallization/cryoprotectant additives, stripped under the
default policy) — see "Strict receptor preparation" below. The remaining 9
contextual cases have no declared policy and have not been processed.

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

A further round added four more contextual cases. pilot-002 (1HVR, HIV
protease with the cyclic-urea inhibitor XK2) retained CSO, a covalently
modified in-chain residue (Ile66-Cys67-Gly68 backbone, annotated
hydroxylation) — the same false-"extra component" pattern already seen in
9HOO, now confirmed in a second, independent case. pilot-003 (1IEP, c-Abl
kinase with imatinib/STI) needed no retention: its extra component, CL, is a
genuinely separate crystallization ion. expansion-001 (1B9V, influenza
neuraminidase with RA2) retained CA — neuraminidase's documented structural
calcium site — while stripping NAG, verified directly to carry no covalent
bond to the polymer and therefore not glycosylation. All three prepared
successfully. expansion-005 (1KZK, HIV protease with JE2147) failed on the
combined alternate-location-and-template-matching class.

| Outcome | Count |
| --- | ---: |
| prepared | 7 |
| failed | 16 |

| Failure class | Count |
| --- | ---: |
| `meeko_alternate_location_requires_choice` | 10 |
| `meeko_alternate_location_and_template_matching_failed` | 5 |
| `meeko_template_matching_failed` | 1 |

Fifteen of the sixteen failures (94%) involve an alternate-location
component. A rejection under this policy is a recorded audit outcome, not
evidence that the underlying PDB entry is defective; it reflects
incompatibility with one specific no-repair preparation choice. Opening the
contextual route has now produced four further failures (9CY0, 2BT9, 9HOO,
1KZK, mostly on the pure alternate-location class, matching the dominant
failure mode already observed across the clean stratum) and five new
prepared receptors — pilot-008, pilot-006, pilot-002, pilot-003,
expansion-001 — bringing the overall strict-preparation success rate to 7 of
23 (30%).

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

Seven cases had both a strictly prepared receptor and a prepared reference
ligand, and were docked with AutoDock Vina 1.2.5 (WSL, fixed seed 20260812,
one CPU, exhaustiveness 8, box derived from the experimental ligand
coordinates). Each retained all nine requested poses.

| Case | PDB | Ligand | Top-score affinity (kcal/mol) | Top-score RMSD to experiment (Å) | Best RMSD to experiment (Å) | RMSD verified? |
| --- | --- | --- | ---: | ---: | ---: | --- |
| pilot-001 | 1STP | BTN (biotin) | -7.244 | 0.689 | 0.689 | yes |
| pilot-007 | 3D4Q | SM5 | -10.960 | 0.769 | 0.769 | yes |
| expansion-001 | 1B9V | RA2 | -7.501 | 0.930 | 0.591 | yes |
| pilot-008 | 3CJO | K30 | -10.890 | 1.504 | 1.154 | yes |
| pilot-002 | 1HVR | XK2 | -6.033 | 2.493 | 1.664 | yes |
| pilot-006 | 3PTB | BEN | -6.058 | 5.594 | 5.578 | yes |
| pilot-003 | 1IEP | STI | -12.68 | — | — | **no — pose-count mismatch** |

RMSD to experiment is identity-mapped, aligned, heavy-atom RMSD after
verifying RCSB CCD-to-SDF atom order, matching heavy-atom sets, isomeric
heavy-atom SMILES, and pose counts. For pilot-001/pilot-007 this is
`data/reference_pose_rmsd.csv`; for the other five (contextual cases
processed after the original subpilot was frozen) it is tracked in the
matching `data/contextual_batch_0N_reference_pose_rmsd.csv`, kept apart
specifically so `scripts/verify_subpilot_evidence.py` continues to check the
original two-case evidence unchanged (see
`reports/CONTEXTUAL-BATCH-04-RESULTS-v0.1.md`,
`-05-RESULTS-v0.1.md`, and `-06-08-RESULTS-v0.1.md` for the full per-case
results). All values are distinct from the Vina-internal RMSD-to-best-pose
values in the respective pose-score files, which describe pose spread
relative to Vina's own top pose, not recovery of the experimental pose.

The five contextual completions differ from the original two cases in
retaining a real physiological or structural non-polymer component (ADP-Mg;
a structural Ca2+ in three separate targets; a covalently modified in-chain
residue) rather than a pocket stripped to the polymer chain alone. Their
outcomes span the full range this audit has observed: expansion-001/1B9V
recovered the experimental pose as closely as the original subpilot (best
pose 0.591 Å); pilot-008/3CJO recovered it closely (1.1-1.5 Å); pilot-002/1HVR
recovered it weakly (1.7-2.5 Å); pilot-006/3PTB did not recover it at all
(~5.6 Å, essentially uniform across all nine poses); and pilot-003/1IEP's
docking completed and produced scores, but its output PDBQT file contained
only 4 pose models against 9 scored modes in Vina's log — a genuine
verification failure, confirmed independently by grepping the file and by
parsing it with Meeko's own PDBQT reader, and left unresolved rather than
silently paired or re-run. No repair, box adjustment, seed change, or retry
was applied to any of these cases — each frozen protocol run happened once
and the result, whatever it was, is reported as obtained.

With n=7 completed runs (six with a verified RMSD, one without), this
remains far too small a sample to draw a recovery-rate conclusion, and none
of it should be extrapolated to other receptors, ligands, or preparation
policies. It does establish, within this audit, that successful strict
preparation, successful reference-pose recovery, and successful RMSD
verification are three separate outcomes that must be reported independently
rather than assumed to track together.

## What this audit does not yet cover

- **9 of 18 contextual candidates remain unprocessed.** Nine
  (expansion-009/9CY0, expansion-021/2BT9, expansion-019/9HOO, pilot-008/3CJO,
  pilot-006/3PTB, pilot-002/1HVR, pilot-003/1IEP, expansion-001/1B9V,
  expansion-005/1KZK) were processed under an explicit, auditable policy;
  four failed strict preparation and five succeeded and were carried through
  to completed docking runs — though only three (1B9V, 3CJO, 1HVR) produced
  a verified RMSD, and only two of those (1B9V, 3CJO) recovered the pose
  closely. The other 9 have no declared policy; most involve genuine free
  non-polymer components (ions, sugars, cofactors) whose retention or
  removal has not yet been decided case by case.
- **No independent reproduction.** No one has re-run the full pipeline from
  an empty checkout to confirm it reproduces 30 candidates → 23 strict
  attempts → 7 successes deterministically end to end.
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
  `data/contextual_batch_{01..09}_preparation_manifest.csv` — all 23
  preparation attempts;
- `data/reference_pose_rmsd.csv`, `data/vina_pose_scores.csv` — the original
  two completed reference-pose recoveries;
- `data/contextual_batch_04_reference_pose_rmsd.csv` — pilot-008 (recovered);
- `data/contextual_batch_05_reference_pose_rmsd.csv` — pilot-006 (did not
  recover);
- `data/contextual_batch_06_reference_pose_rmsd.csv` — pilot-002 (weak
  recovery);
- `data/contextual_batch_07_reference_pose_rmsd.csv` — pilot-003 (RMSD not
  verified, pose-count mismatch);
- `data/contextual_batch_08_reference_pose_rmsd.csv` — expansion-001
  (recovered, best pose 0.591 Å);
- each with a matching `_vina_pose_scores.csv`, all tracked separately from
  the original subpilot by design;
- `reports/generated/figures/` — figures 01-04, regenerated by
  `scripts/render_audit_figures.py` (see `reports/FIGURE-CATALOG-v0.1.md`);
- `python scripts/verify_subpilot_evidence.py` reproduces the original
  two-case evidence check reported here, unchanged by this round.
