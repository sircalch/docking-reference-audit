# Clean execution batch 03 — strict preparation result v0.1

## Outcome

For 7AOT / RTQ, the predeclared extraction of chain A from the original mmCIF
completed successfully. Strict Meeko 0.7.1 preparation exited with code 1 and
was retained as `meeko_alternate_location_and_template_matching_failed`.

The command log identifies alternate locations in 11 residues and template
matching failures for A:65, A:73, and A:74. No alternate conformer was chosen,
no residue was removed, and `--allow_bad_res` was not enabled. The case is
therefore not eligible for ligand preparation, docking, or reference-pose RMSD
under protocol v0.1.

## Evidence

- extraction: `data/clean_batch_03_receptor_extraction_manifest.csv`;
- preparation: `data/clean_batch_03_preparation_manifest.csv`;
- command log: `reports/generated/clean-batch-03/strict-preparation/`;
- original mmCIF checksum: `data/retrieval_manifest.csv`.
