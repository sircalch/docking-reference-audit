# Strict receptor-preparation summary v0.1

## Scope

This descriptive summary combines the original three-case strict subpilot with
eleven subsequently registered, independently frozen clean batches. It reports
compatibility with one specific, no-repair Meeko 0.7.1 policy. It is not a
benchmark estimate and must not be generalized to proteins, docking programs,
or alternative preparation policies.

| Case | PDB | Batch | Strict outcome | Recorded reason where rejected |
| --- | --- | --- | --- | --- |
| pilot-001 | 1STP | original subpilot | prepared | — |
| pilot-004 | 1FPU | original subpilot | failed | `meeko_template_matching_failed` |
| pilot-007 | 3D4Q | original subpilot | prepared | — |
| expansion-010 | 6FMC | clean batch 01 | failed | `meeko_alternate_location_requires_choice` |
| expansion-011 | 7G0Z | clean batch 02 | failed | `meeko_alternate_location_and_template_matching_failed` |
| expansion-012 | 7AOT | clean batch 03 | failed | `meeko_alternate_location_and_template_matching_failed` |
| expansion-013 | 7TH6 | clean batch 04 | failed | `meeko_alternate_location_requires_choice` |
| expansion-014 | 6Q7D | clean batch 05 | failed | `meeko_alternate_location_requires_choice` |
| expansion-015 | 1NWZ | clean batch 06 | failed | `meeko_alternate_location_requires_choice` |
| expansion-016 | 1X8Q | clean batch 07 | failed | `meeko_alternate_location_requires_choice` |
| expansion-017 | 4X5P | clean batch 08 | failed | `meeko_alternate_location_requires_choice` |
| expansion-018 | 5HBS | clean batch 09 | failed | `meeko_alternate_location_and_template_matching_failed` |
| expansion-020 | 4XXG | clean batch 10 | failed | `meeko_alternate_location_and_template_matching_failed` |
| expansion-022 | 6TE2 | clean batch 11 | failed | `meeko_alternate_location_requires_choice` |

Across these fourteen strict attempts, two receptors prepared and twelve were
rejected. The two prepared original-subpilot receptors are the only cases that
proceeded to the already recorded reference-pose runs; no new docking run is
implied by this summary.

Eleven of the twelve rejections carry an alternate-location component. The
three most recent additions (5HBS, 4XXG, 6TE2) were again selected from the
same sub-1-angstrom stratum of the frozen clean-discovery ranking (0.89 A,
0.85 A, 0.922 A) and again all failed, two of them on the combined
alternate-location-and-template-matching class rather than the pure
alternate-location class seen most often before. This further supports the
descriptive pattern already noted: within this candidate pool, ultra-high
resolution does not translate into strict no-repair preparation success, and
the two attempts made this session to find lower-resolution comparators
(roughly 1.5-2.0 A) inside the frozen ranking did not succeed with reasonable
manual sampling effort. The full clean-eligible subset registered so far
(twelve clean cases against thirty registered candidates) has now been carried
through strict preparation to its 30-candidate registration cap; the sample
remains small and the observation stays descriptive of this fourteen-case
sample, not a general claim about resolution and preparation compatibility.

## Interpretation boundary

The high-resolution clean inventory class is a structural description, not a
guarantee that strict receptor preparation will be compatible. In particular,
alternate locations and template matching are encountered only after the
original coordinates have been selected without repair. The present protocol
keeps those outcomes rather than choosing conformers or deleting residues
post hoc.

## Machine-readable evidence

- `data/strict_preparation_manifest.csv` (original subpilot);
- `data/clean_batch_01_preparation_manifest.csv`;
- `data/clean_batch_02_preparation_manifest.csv`;
- `data/clean_batch_03_preparation_manifest.csv`;
- `data/clean_batch_04_preparation_manifest.csv`;
- `data/clean_batch_05_preparation_manifest.csv`;
- `data/clean_batch_06_preparation_manifest.csv`;
- `data/clean_batch_07_preparation_manifest.csv`;
- `data/clean_batch_08_preparation_manifest.csv`;
- `data/clean_batch_09_preparation_manifest.csv`;
- `data/clean_batch_10_preparation_manifest.csv`;
- `data/clean_batch_11_preparation_manifest.csv`.
