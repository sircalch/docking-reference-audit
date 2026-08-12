# Strict receptor-preparation summary v0.1

## Scope

This descriptive summary combines the original three-case strict subpilot with
five subsequently registered, independently frozen clean batches. It reports
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

Across these eight strict attempts, two receptors prepared and six were
rejected. The two prepared original-subpilot receptors are the only cases that
proceeded to the already recorded reference-pose runs; no new docking run is
implied by this summary.

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
- `data/clean_batch_05_preparation_manifest.csv`.
