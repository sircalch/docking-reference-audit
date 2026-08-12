# Clean execution batch 01 — strict preparation result v0.1

## Scope

This report records one separate, predeclared clean-structure execution batch.
It does not modify or reinterpret the original strict subpilot.

## Case and frozen policy

| Case | PDB | Ligand | Selected chain | Policy |
| --- | --- | --- | --- | --- |
| expansion-010 | 6FMC | DUE | A | retain chain A; remove waters and ligands; no repair or alternate-location selection |

## Outcome

The original-coordinate mmCIF was extracted successfully under that policy.
Strict Meeko 0.7.1 receptor preparation then exited with code 1 and was
recorded as `meeko_alternate_location_requires_choice`.

The preparation log reports alternate locations in 25 residues of chain A
(including A:272, A:277, A:288, and A:299).  Meeko requested an explicit
alternate-location choice or options that remove problematic residues.  Neither
was supplied: choosing conformers, enabling a default alternate location, or
using `--allow_bad_res` would violate this batch's frozen strict policy.

Accordingly, 6FMC is a retained strict-preparation failure and is not eligible
for ligand preparation, box derivation, Vina, or reference-pose RMSD in this
protocol version.

## Evidence

- receptor extraction: `data/clean_batch_01_receptor_extraction_manifest.csv`;
- strict preparation: `data/clean_batch_01_preparation_manifest.csv`;
- command output: `reports/generated/clean-batch-01/strict-preparation/`;
- source retrieval and SHA-256: `data/retrieval_manifest.csv`.
