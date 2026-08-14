# Failure-mode analysis of strict preparation v0.1

## Scope

23 of 30 registered candidates were attempted under the frozen, no-repair
strict preparation policy (Meeko 0.7.1, no altloc selection, no
`--allow_bad_res`, no missing-atom repair); 16 failed. This report exists
because the raw number ("16 failures out of 23 attempts") can misread as
"the pipeline doesn't work" if left unexplained. It does not — every
failure here is a deliberate, correctly-triggered policy rejection, not a
bug, and the failure pattern itself is one of this audit's genuine
findings, not noise to be minimized.

## 1. Failure classes are not evenly distributed — one cause dominates

| Failure class | Count | Share of 16 failures |
| --- | ---: | ---: |
| Alternate-location choice required (pure) | 10 | 63% |
| Alternate-location choice required + template matching failed | 5 | 31% |
| Template matching failed (no altloc involved) | 1 | 6% |

**15 of 16 failures (94%) involve an alternate-location conflict.** This is
not a diffuse basket of unrelated errors — it is overwhelmingly one
specific, well-understood cause.

## 2. What an alternate-location failure actually is

Some crystal structures resolve a residue's side chain (or, less often,
backbone) in more than one physically real conformation — recorded in the
PDB as alternate locations ("altloc" A/B/...). Meeko's receptor preparation
refuses to build a PDBQT until told which conformation to keep, and says so
explicitly. Real log excerpt, case `expansion-010` (PDB 6FMC):

```
Error: Creation of data structure for receptor failed.
Details:
- Residues with alternate location: ['A:272', 'A:277', 'A:288', ... 25 residues]
Either specify an altloc for each with option wanted_altloc
or a general default altloc with option default_altloc.
Recommendations:
1. (for batch processing) Use -a/--allow_bad_res ... and --default_altloc
   to set a default altloc variant. Use these at your own risk.
2. (processing individual structure) ... Use --wanted_altloc to set
   variants for specific residues.
```

Meeko offers exactly the two flags this audit refuses to use
(`--default_altloc`, `--wanted_altloc`). Picking a conformation on the
researcher's behalf is a repair decision — informed by chemical judgment
about which conformer is more likely biologically relevant — and this
audit's entire premise is measuring what a structure yields *without* that
judgment applied. Using either flag would not fix a bug; it would silently
change the experiment being measured.

## 3. The resolution-altloc tension (the actual finding)

Ten of the 30 registered candidates carry an explicit resolution figure in
their registration rationale (recorded when resolution was the stated
reason for selecting that structure, e.g. "ultra-high 0.82 Å resolution").
Cross-referencing those ten against preparation outcomes:

| Resolution | Case | Outcome |
| ---: | --- | --- |
| 0.80 Å | expansion-009 | failed — alternate location requires choice |
| 0.82 Å | expansion-015 | failed — alternate location requires choice |
| 0.83 Å | expansion-019 | failed — alternate location requires choice |
| 0.84 Å | expansion-011 | failed — alternate location + template matching |
| 0.85 Å | expansion-016 | failed — alternate location requires choice |
| 0.85 Å | expansion-020 | failed — alternate location + template matching |
| 0.89 Å | expansion-018 | failed — alternate location + template matching |
| 0.90 Å | expansion-010 | failed — alternate location requires choice |
| 0.92 Å | expansion-022 | failed — alternate location requires choice |
| 0.94 Å | expansion-021 | failed — alternate location requires choice |

**All ten of the explicitly sub-1.0 Å candidates in this registry failed
preparation, and all ten failed for an alternate-location reason.** This is
not a coincidence of chemistry: the same physical process that lets
crystallography resolve a structure to sub-angstrom detail is what makes
alternate side-chain conformations visible and modelable in the first
place. Ultra-high resolution and altloc-driven preparation failure are
mechanistically linked, not independent.

This is worth stating plainly for readers: **the criterion commonly used as
a shorthand for "high-quality structure" (resolution) is, in this
no-repair pipeline, anti-correlated with preparability.** A pipeline
selecting only for resolution would silently select against exactly the
structures a strict, no-repair policy can process. This is a real,
citable methodological observation about automated no-repair docking
pipelines generally, not a limitation specific to this audit's tooling.

## 4. Interpretation boundary

- The ten-case resolution cross-reference (Section 3) is based on
  resolution figures that happen to be recorded in free-text registration
  rationale, not a systematic resolution capture across all 30 candidates.
  It should be read as a striking corroborating observation on the subset
  where resolution was recorded, not a formal statistic claimed over the
  full registry.
- "15/16 failures involve altloc" (Section 1) is a complete count over all
  16 actual failures and is not subject to that caveat.
- None of this changes the audit's headline number (7/23 prepared, 30%);
  it explains *why* the other 16 failed, in enough mechanistic and
  quantitative detail that the raw failure count reads as evidence the
  policy is doing exactly what it says, not as evidence something broke.

## Machine-readable evidence

- `data/candidate_inventory_table.csv` — full 30-candidate outcome list
  (Table 9), including the `preparation_outcome` column this report
  aggregates.
- `reports/generated/strict-preparation/expansion-010_6FMC_chain-A.log` —
  the real log the Section 2 excerpt is quoted from.
- `data/candidates.csv` — `selection_rationale` field, source of the
  resolution figures in Section 3.
