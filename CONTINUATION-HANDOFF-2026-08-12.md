# Continuation handoff — 2026-08-12

## Project identity and boundary

Repository: `C:\visualizassss\docking-reference-audit`

This is an independent, computational-only audit of public protein--ligand
structures for reproducible reference-pose docking. It must **not** use the
doctoral GOx/ZIF-8 project, its files, or its results. The study does not claim
biological activity, binding affinity, ligand potency, or universal docking
performance.

## Current Git state

Last committed revision before this handoff:

```text
cd98f14 Track evidence flow and retrieval states
```

There is one uncommitted improvement made immediately before this handoff:
`scripts/fetch_rcsb_structures.py` now accepts repeatable `--case-id` to retry
only a named registered candidate while preserving every other manifest row.
It has not yet been committed. First validate it with Python compilation and a
read-only argument check; do not run a network retry merely to test it.

No GitHub remote has been created. Do not publish, create a repository, upload
to Zenodo, or make a release without a new explicit user instruction.

## Scientific state

### Registered candidates and retrieval

- 22 candidates are registered in `data/candidates.csv`.
- 20 original mmCIF files have been retrieved and checksummed in
  `data/retrieval_manifest.csv`.
- Two cases have retained temporary RCSB retrieval failures:
  - `expansion-013`, 7TH6 / I56, RCSB 504 gateway timeout;
  - `expansion-014`, 6Q7D / HOT, RCSB 502 bad gateway.

These are infrastructure outcomes, **not** structural/preparation failures.
They have supporting entries in `data/screening_log.csv`. Do not repeatedly
retry them; retry later in a targeted way only, e.g.:

```text
python scripts/fetch_rcsb_structures.py --case-id expansion-013 --timeout 120
```

If a retry succeeds, then run, in order:

```text
python scripts/audit_structure_inventory.py
python scripts/propose_case_policies.py
python scripts/classify_structural_eligibility.py
```

### Strict preparation and docking results

Six strict receptor-preparation attempts have real recorded outcomes:

| PDB | Case | Strict result |
| --- | --- | --- |
| 1STP | pilot-001 | prepared |
| 1FPU | pilot-004 | failed: template matching |
| 3D4Q | pilot-007 | prepared |
| 6FMC | expansion-010 | failed: alternate locations require a choice |
| 7G0Z | expansion-011 | failed: alternate locations plus template matching |
| 7AOT | expansion-012 | failed: alternate locations plus template matching |

The frozen policy prohibits alternate-location choices, repairs, residue
deletion, template addition, and `--allow_bad_res`. Do not make a rejected case
pass by changing this policy retrospectively.

Only the two original prepared cases ran through Vina:

- 1STP / BTN: 9 retained poses;
- 3D4Q / SM5: 9 retained poses.

All 18 experimental-reference heavy-atom RMSD values are in
`data/reference_pose_rmsd.csv`. The original evidence verification must remain
green:

```text
python scripts/verify_subpilot_evidence.py
# Expected: EVIDENCE VERIFIED: 2 completed runs; 18 score rows; 18 RMSD rows.
```

### Eligibility and discovery

- Frozen inventory currently has 4 clean and 16 contextual retrieved cases.
- “Clean” means one model, one polymer chain, one declared ligand instance,
  and no other non-polymeric component in the current inventory. It is not a
  guarantee of Meeko compatibility.
- Contextual cases must not be processed until a predeclared case policy covers
  chains, metals/cofactors/glycans, and water.
- Candidate discovery is governed by
  `protocol/CANDIDATE-DISCOVERY-v0.1.md`: X-ray, resolution <= 2.0 Å, exactly
  one RCSB non-polymer entity excluding solvent; it requires chemical screening
  and original-coordinate inventory afterwards.
- The target-diversity rule is active. Do not let repeated FKBP51 or SARS-CoV-2
  NSP3 structures dominate when distinct-target candidates remain in the queue.
- Discovery-only command (does not register, download, prepare, or dock):

```text
python scripts/discover_clean_candidates.py --limit 300
```

## Figures and publication presentation

`scripts/render_audit_figures.py` renders real, reproducible SVG and 300 dpi
PNG outputs under `reports/generated/figures/` from CSV manifests:

1. `figure-01-structural-inventory` — clean/contextual inventory;
2. `figure-02-strict-preparation` — all six strict preparation outcomes;
3. `figure-03-reference-pose-outcomes` — all 18 Vina poses and experimental
   reference RMSD;
4. `figure-04-evidence-flow` — candidates through verified reference poses.

Their sources and interpretation limits are in `reports/FIGURE-CATALOG-v0.1.md`.
Generated figures, raw files, and derived scientific outputs are gitignored;
the scripts and manifests are versioned. Inspect generated graphics before
using them in a manuscript.

## Recommended next work order

1. Validate and commit the targeted retrieval option, without network retries.
2. At a later time, retry only `expansion-013` and `expansion-014` once each.
   Keep the date/status/error history transparent in manifests and screening log.
3. If a download succeeds, inventory it first. Only clean cases with a fully
   explicit frozen policy can enter a separate execution batch.
4. Continue discovery in the fixed ranking, recording exclusions/skips rather
   than silently omitting them. Stop candidate collection at 30 fully audited
   candidates or 12 completed reference-pose cases, whichever occurs first,
   per `protocol/EXPANSION-PLAN-v0.1.md`.
5. Do not frame the current sample as a docking benchmark. With more cases, add
   descriptive uncertainty and result tables; do not claim comparative accuracy
   unless the protocol and sample genuinely support it.
6. Build a manuscript only after enough independent evidence exists. The likely
   article contribution is provenance-aware strict preparation audit and
   reference-pose recovery, not a new docking algorithm.

## Validation commands

```text
Get-ChildItem scripts -Filter *.py -File | ForEach-Object { python -m py_compile $_.FullName }
python scripts/classify_structural_eligibility.py
python scripts/render_audit_figures.py
python scripts/verify_subpilot_evidence.py
git diff --check
git status --short
```

## Key versioned documents

- `README.md`
- `protocol/PROTOCOL-v0.1.md`
- `protocol/EXPANSION-PLAN-v0.1.md`
- `protocol/CANDIDATE-DISCOVERY-v0.1.md`
- `reports/STRICT-PREPARATION-SUMMARY-v0.1.md`
- `reports/FIGURE-CATALOG-v0.1.md`
- `requirements.txt`

## Authorship and research integrity

All contributors must review and approve any manuscript, results, authorship
order, and submission independently. Describe computational assistance simply
and accurately according to the target journal policy; do not hide it and do
not imply that automated tools produced experimental validation.
