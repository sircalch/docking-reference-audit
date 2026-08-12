# Strict receptor-preparation summary v0.1

## Scope

This descriptive summary combines the original three-case strict subpilot with
eight subsequently registered, independently frozen clean batches. It reports
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

Across these eleven strict attempts, two receptors prepared and nine were
rejected. The two prepared original-subpilot receptors are the only cases that
proceeded to the already recorded reference-pose runs; no new docking run is
implied by this summary.

Eight of the nine rejections carry an alternate-location component. The three
most recent additions (1NWZ, 1X8Q, 4X5P) were all selected partly for their
high nominal resolution (0.82 A, 0.85 A, 0.997 A); all three still failed on
alternate locations. This is consistent with, not contrary to, high-resolution
data: sub-angstrom to near-angstrom refinements more often model alternate
side chain conformers explicitly, which is exactly what this frozen no-repair
policy declines to resolve automatically. An attempt to find a lower-resolution
comparator (roughly 1.5-2.0 A) within the frozen clean-discovery ranking did
not succeed with a reasonable manual sampling effort; the ranked pool sampled
so far skews toward sub-1-angstrom entries even deep into the ranking. Selecting
candidates by resolution alone should not be read as a way to raise the
strict-preparation success rate; the pattern so far points the other way. This
observation is descriptive of the present eleven-case sample and is not yet a
general claim.

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
- `data/clean_batch_08_preparation_manifest.csv`.
