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
| expansion-019 | 9HOO | contextual batch 03 | failed | `meeko_alternate_location_requires_choice` |
| pilot-008 | 3CJO | contextual batch 04 | prepared | — |

Across these eighteen strict attempts, three receptors prepared and fifteen
were rejected. The two original-subpilot receptors (pilot-001, pilot-007)
proceeded to the already recorded reference-pose runs; the third prepared
receptor, pilot-008 (3CJO), is a new completed reference-pose case this
round — see below.

Fourteen of the fifteen rejections carry an alternate-location component. The
three additions from the final clean-registration round (5HBS, 4XXG, 6TE2)
were again selected from the same sub-1-angstrom stratum of the frozen
clean-discovery ranking (0.89 A, 0.85 A, 0.922 A) and again all failed, two of
them on the combined alternate-location-and-template-matching class rather
than the pure alternate-location class seen most often before. Two attempts
made earlier to find lower-resolution comparators (roughly 1.5-2.0 A) inside
the frozen ranking did not succeed with reasonable manual sampling effort.

With the clean stratum of the 30-candidate registry fully processed (twelve
of twelve), this round opened the contextual stratum. expansion-009 (9CY0)
and expansion-021 (2BT9), both structurally complex only by having multiple
polymer chains and multiple declared ligand instances with no other
non-polymeric component, were assigned an auditable receptor-chain and
ligand-instance policy computed by `scripts/propose_case_policies.py`
(minimum original-coordinate ligand-to-polymer atom distance) and carried
through the same frozen no-repair extraction and preparation pipeline used
for every clean case. Both failed on the pure alternate-location class.

expansion-019 (9HOO) was then investigated directly rather than left
unresolved: its flagged "other non-polymer component," CSS (S-mercaptocysteine,
chem-comp type L-peptide linking), was inspected in the deposited mmCIF and
found to be a covalently modified residue at auth_seq_id 304 within chain A
itself — `covale` bonds link Lys303-C to Cys304-N and Cys304-C to His305-N,
placing it inline in the polypeptide backbone, not a free ligand or cofactor.
`audit_structure_inventory.py` flags it as "other" only because it carries a
HETATM record, which is how mmCIF encodes any non-standard residue even when
covalently part of the chain. The declared policy for this case therefore
retains CSS as an intrinsic part of the receptor chain — removing it would be
an undeclared residue deletion, which protocol v0.1 prohibits — and removes
only water and the declared ligand (U5P), identical in spirit to every clean
case. No extraction-script change was needed: gemmi's entity-aware
`remove_ligands_and_waters()` already keeps CSS because it belongs to the
polymer entity, confirmed by inspecting the extracted PDB directly (11 atoms
retained at residue 304, zero U5P/HOH coordinate lines). expansion-019 still
failed strict preparation, again on the pure alternate-location class (96
flagged residues in this 0.83 A structure).

Finally, pilot-008 (3CJO, "KSP in complex with inhibitor 30") was processed
under a fourth kind of contextual policy: rather than stripping every
non-declared non-polymer component, the extraction script was extended
(`retained_components` column, `scripts/extract_strict_receptors.py`) to
retain named components on an explicit, chemically justified basis. 3CJO
has two other non-polymer components, ADP and MG, which are the
physiological KSP/Eg5 nucleotide cofactor bound at its own well-characterized
motor-domain site, distinct from the allosteric K30 inhibitor pocket. These
were retained rather than removed — stripping a resolved physiological
cofactor would alter pocket chemistry beyond a no-repair policy's intent —
and only water and the declared ligand K30 were removed. This was verified
empirically by inspecting the extracted receptor PDB (27 ADP atoms and the MG
ion retained, zero K30/HOH atoms). Strict preparation **succeeded**: the
third prepared receptor in the audit. Docking and reference-pose RMSD were
then completed for this case; see
`reports/CONTEXTUAL-BATCH-04-RESULTS-v0.1.md` and the updated
`reports/AUDIT-SYNTHESIS-v0.1.md` for the full result.

Opening the contextual route therefore produced one net new reference-pose
case (pilot-008) alongside three further failures (9CY0, 2BT9, 9HOO) that
extend, rather than contradict, the pattern already observed for the clean
stratum: the overall strict-preparation success rate remains low (3 of 18,
17%), still dominated by alternate-location incompatibility (14 of 15
failures), and the earlier "extra non-polymer component" flag on 9HOO was
found to be a labeling artifact of HETATM records rather than a genuine free
ligand.

The observation stays descriptive of this eighteen-case sample and is not a
general claim about resolution, chain multiplicity, cofactor retention, or
preparation compatibility.

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
- `data/contextual_batch_02_preparation_manifest.csv`;
- `data/contextual_batch_03_preparation_manifest.csv`;
- `data/contextual_batch_04_preparation_manifest.csv` (see also
  `reports/CONTEXTUAL-BATCH-04-RESULTS-v0.1.md` for the full docking result).
