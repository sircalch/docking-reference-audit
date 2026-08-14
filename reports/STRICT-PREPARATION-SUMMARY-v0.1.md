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
| pilot-006 | 3PTB | contextual batch 05 | prepared | — |
| pilot-002 | 1HVR | contextual batch 06 | prepared | — |
| pilot-003 | 1IEP | contextual batch 07 | prepared | — |
| expansion-001 | 1B9V | contextual batch 08 | prepared | — |
| expansion-005 | 1KZK | contextual batch 09 | failed | `meeko_alternate_location_and_template_matching_failed` |

Across these twenty-three strict attempts, seven receptors prepared and
sixteen were rejected. The two original-subpilot receptors (pilot-001,
pilot-007) proceeded to the already recorded reference-pose runs; pilot-008,
pilot-006, pilot-002, pilot-003, and expansion-001 are five further
completed docking runs from the two most recent contextual rounds — see
below.

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

A fifth contextual case, pilot-006 (3PTB, bovine trypsin with the benzamidine
inhibitor BEN), used the same retained-component mechanism for a second,
independently justified cofactor: CA, trypsin's well-characterized structural
calcium-binding site (Bode and Schwager, 1975), distinct from the S1
catalytic pocket where benzamidine binds. Strict preparation **succeeded**
(the fourth prepared receptor in the audit) and docking completed, but the
docked poses did not recover the experimental position: all nine poses
returned RMSD ≈5.6 A regardless of score, versus the sub-2 A recovery seen in
every other completed case. This is reported as a genuine negative
pose-recovery result — a successful strict preparation does not guarantee an
accurate docked pose under this frozen protocol. See
`reports/CONTEXTUAL-BATCH-05-RESULTS-v0.1.md`.

A further round processed three more contextual cases with the same
retained-component discipline, plus a fourth that failed preparation.
pilot-002 (1HVR, HIV protease with the cyclic-urea inhibitor XK2) retained
CSO, a covalently modified in-chain residue (Ile66-Cys67-Gly68 backbone,
annotated hydroxylation) — the same false-"extra component" pattern already
seen in 9HOO. pilot-003 (1IEP, c-Abl kinase with imatinib/STI) needed no
retention: its extra component, CL, is a genuinely separate crystallization
ion, stripped under the default policy. expansion-001 (1B9V, influenza
neuraminidase with the inhibitor RA2) retained CA — neuraminidase's
well-documented structural calcium site — while stripping NAG, verified
directly to carry no covalent bond to the polymer chain and therefore not
glycosylation. **All three prepared successfully.** The fourth,
expansion-005 (1KZK, HIV protease with JE2147), failed on the combined
alternate-location-and-template-matching class, extending rather than
breaking the dominant failure pattern.

Opening the contextual route has now produced five net new prepared
receptors (pilot-008, pilot-006, pilot-002, pilot-003, expansion-001)
alongside four further preparation failures (9CY0, 2BT9, 9HOO, 1KZK) that
extend, rather than contradict, the pattern already observed for the clean
stratum: the overall strict-preparation success rate is now 7 of 23 (30%),
still dominated by alternate-location incompatibility (15 of 16 failures),
and the earlier "extra non-polymer component" flags on 9HOO and 1HVR were
both found to be labeling artifacts of HETATM records rather than genuine
free ligands. Of the five new prepared receptors, docking outcomes span a
full range: expansion-001/1B9V and pilot-008/3CJO recovered the experimental
pose closely (0.591-1.504 Å depending on pose), pilot-002/1HVR recovered it
weakly (1.664-2.493 Å), pilot-006/3PTB did not recover it at all (~5.6 Å),
and pilot-003/1IEP's docking completed but could not be RMSD-verified at all
due to a pose-count mismatch between Vina's log and its output file (4
parsed poses against 9 logged scores) — reported as an unresolved technical
outcome rather than silently discarded. See
`reports/CONTEXTUAL-BATCH-06-08-RESULTS-v0.1.md` for the full detail.

The observation stays descriptive of this twenty-three-case sample and is
not a general claim about resolution, chain multiplicity, cofactor
retention, or preparation compatibility.

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
  `reports/CONTEXTUAL-BATCH-04-RESULTS-v0.1.md` for the full docking result);
- `data/contextual_batch_05_preparation_manifest.csv` (see also
  `reports/CONTEXTUAL-BATCH-05-RESULTS-v0.1.md` for the full docking result,
  including the negative pose-recovery outcome);
- `data/contextual_batch_{06,07,08,09}_preparation_manifest.csv` (see also
  `reports/CONTEXTUAL-BATCH-06-08-RESULTS-v0.1.md` for the full docking
  results, including the weak-recovery and unverifiable outcomes).
