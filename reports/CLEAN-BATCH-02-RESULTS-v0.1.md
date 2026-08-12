# Clean execution batch 02 — strict preparation result v0.1

## Scope

This is an independent one-case strict execution batch for 7G0Z / WMB.  It
does not modify the original subpilot or clean batch 01.

## Outcome

The receptor was extracted from the original-coordinate mmCIF after retaining
chain A and removing ligands and waters, as predeclared.  Strict Meeko 0.7.1
preparation then exited with code 1.  The normalized result is
`meeko_alternate_location_and_template_matching_failed`.

The retained log reports alternate locations in 32 residues and template
matching failure for residue A:131.  Meeko suggested selecting alternate
locations and enabling `--allow_bad_res`; neither action was taken because each
would alter the frozen strict policy.  The case is consequently ineligible for
subsequent ligand preparation, docking, and reference-pose RMSD under v0.1.

## Evidence

- extraction: `data/clean_batch_02_receptor_extraction_manifest.csv`;
- preparation: `data/clean_batch_02_preparation_manifest.csv`;
- command log: `reports/generated/clean-batch-02/strict-preparation/`;
- original file SHA-256: `data/retrieval_manifest.csv`.
