# Strict receptor-preparation summary v0.1

## Scope

This descriptive summary combines the original three-case strict subpilot,
eleven subsequently registered clean batches, and two contextual batches
processed under an explicit, per-case predeclared policy. It reports
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
| expansion-009 | 9CY0 | contextual batch 01 | failed | `meeko_alternate_location_requires_choice` |
| expansion-021 | 2BT9 | contextual batch 02 | failed | `meeko_alternate_location_requires_choice` |

Across these sixteen strict attempts, two receptors prepared and fourteen were
rejected. The two prepared original-subpilot receptors are the only cases that
proceeded to the already recorded reference-pose runs; no new docking run is
implied by this summary.

Thirteen of the fourteen rejections carry an alternate-location component. The
three additions from the final clean-registration round (5HBS, 4XXG, 6TE2)
were again selected from the same sub-1-angstrom stratum of the frozen
clean-discovery ranking (0.89 A, 0.85 A, 0.922 A) and again all failed, two of
them on the combined alternate-location-and-template-matching class rather
than the pure alternate-location class seen most often before. Two attempts
made earlier to find lower-resolution comparators (roughly 1.5-2.0 A) inside
the frozen ranking did not succeed with reasonable manual sampling effort.

With the clean stratum of the 30-candidate registry fully processed (twelve
of twelve), this round opened the contextual stratum: expansion-009 (9CY0)
and expansion-021 (2BT9), both structurally complex only by having multiple
polymer chains and multiple declared ligand instances with no other
non-polymeric component, were assigned an auditable receptor-chain and
ligand-instance policy computed by `scripts/propose_case_policies.py`
(minimum original-coordinate ligand-to-polymer atom distance) and carried
through the same frozen no-repair extraction and preparation pipeline used
for every clean case. Both failed on the pure alternate-location class. This
extends, rather than contradicts, the pattern already observed: opening the
contextual route did not raise the strict-preparation success rate in these
two additional attempts. One contextual case, expansion-019 (9HOO), remains
unprocessed: its extra non-polymer component (CSS) would require the
extraction script to remove a declared component beyond the fixed
ligand-and-water policy, which is a script change not yet made and is
recorded here as an open item rather than silently skipped.

The observation stays descriptive of this sixteen-case sample and is not a
general claim about resolution, chain multiplicity, or preparation
compatibility.

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
- `data/clean_batch_11_preparation_manifest.csv`;
- `data/contextual_batch_01_preparation_manifest.csv`;
- `data/contextual_batch_02_preparation_manifest.csv`.
