# Docking reference-pose audit — synthesis v0.1

## Purpose and scope

This report combines, in one place, the inclusion criteria, the full candidate
registry outcome, the strict receptor-preparation results, and the two
completed reference-pose recoveries produced under protocol v0.1
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

All 12 clean cases were carried through strict receptor preparation. None of
the 18 contextual cases have been processed: no case-specific policy has yet
been declared for any of them, and none may be processed without one under
protocol v0.1.

## Strict receptor preparation

Every clean case was extracted (`scripts/extract_strict_receptors.py`, fixed
policy: single declared chain, all waters and the declared ligand removed)
and passed to Meeko 0.7.1 (`scripts/run_strict_meeko_preparation.py`) with no
alternate-location choice, no repair, no residue deletion, no template
addition, and `--allow_bad_res` never enabled.

| Outcome | Count |
| --- | ---: |
| prepared | 2 |
| failed | 12 |

| Failure class | Count |
| --- | ---: |
| `meeko_alternate_location_requires_choice` | 7 |
| `meeko_alternate_location_and_template_matching_failed` | 4 |
| `meeko_template_matching_failed` | 1 |

Eleven of the twelve failures (92%) involve an alternate-location component.
A rejection under this policy is a recorded audit outcome, not evidence that
the underlying PDB entry is defective; it reflects incompatibility with one
specific no-repair preparation choice.

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

Two cases had both a strictly prepared receptor and a prepared reference
ligand, and were docked with AutoDock Vina 1.2.5 (WSL, fixed seed 20260812,
one CPU, exhaustiveness 8, box derived from the experimental ligand
coordinates). Each retained all nine requested poses.

| Case | PDB | Ligand | Top-score affinity (kcal/mol) | Top-score RMSD to experiment (Å) | Lowest RMSD to experiment (Å) |
| --- | --- | --- | ---: | ---: | ---: |
| pilot-001 | 1STP | BTN (biotin) | -7.244 | 0.689 | 0.689 |
| pilot-007 | 3D4Q | SM5 | -10.960 | 0.769 | 0.769 |

RMSD to experiment is identity-mapped, aligned, heavy-atom RMSD after
verifying RCSB CCD-to-SDF atom order, matching heavy-atom sets, isomeric
heavy-atom SMILES, and pose counts (`data/reference_pose_rmsd.csv`). It is
distinct from the Vina-internal RMSD-to-best-pose values in
`data/vina_pose_scores.csv`, which describe pose spread relative to Vina's own
top pose, not recovery of the experimental pose.

In both completed cases, Vina's top-scoring pose was also close to the
experimental pose (<0.8 Å). With n=2, this is not a statistically meaningful
recovery rate and must not be extrapolated to other receptors, ligands, or
preparation policies.

## What this audit does not yet cover

- **18 contextual candidates remain unprocessed.** No case-specific
  chain/cofactor/water policy has been declared for any of them. This is the
  only route left open by protocol v0.1 to add reference-pose cases beyond
  the current two, since the clean stratum of the 30-candidate registry is
  now fully processed (12/12).
- **No independent reproduction.** No one has re-run the full pipeline from
  an empty checkout to confirm it reproduces 30 candidates → 14 strict
  attempts → 2 successes deterministically end to end.
- **No claim of generality.** Findings describe compatibility with Meeko
  0.7.1 under one specific no-repair policy, applied to one specific,
  resolution-skewed candidate pool. They do not describe Meeko, Vina, or
  AutoDock-family tools in general.

## Machine-readable evidence

- `data/candidates.csv`, `data/retrieval_manifest.csv`,
  `data/eligibility_register.csv` — registry and classification;
- `data/strict_preparation_manifest.csv`,
  `data/clean_batch_{01..11}_preparation_manifest.csv` — all 14 preparation
  attempts;
- `data/reference_pose_rmsd.csv`, `data/vina_pose_scores.csv` — the two
  completed reference-pose recoveries;
- `reports/generated/figures/` — figures 01-04, regenerated by
  `scripts/render_audit_figures.py` (see `reports/FIGURE-CATALOG-v0.1.md`);
- `python scripts/verify_subpilot_evidence.py` reproduces the completed-case
  evidence check reported here.
