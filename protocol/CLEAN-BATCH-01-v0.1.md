# Clean execution batch 01 v0.1

## Purpose

This batch contains one newly registered case, 6FMC / DUE.  It is separate
from the original strict subpilot and therefore cannot alter its manifests,
scores, or report.

## Frozen policy

The original mmCIF inventory has one model, one polymer chain (`A`), one DUE
instance (`A:DUE:201`), and no additional non-polymeric component.  The frozen
receptor policy is therefore fully specified without a retention/removal
decision about metals, cofactors, glycans, or other ligands:

1. retain chain A;
2. remove all waters and the declared ligand after chain selection;
3. make no coordinate repair, alternate-location choice, template addition, or
   residue deletion;
4. retain either preparation failure or success as an observed outcome.

The corresponding machine-readable batch definition is
`data/clean_batch_01.csv`.  Any execution uses separate output directories and
separate manifests from the original subpilot.

## Registration provenance

6FMC was selected from an RCSB PDB Search API query restricted to X-ray
structures at resolution <= 2.0 Å and subsequently verified through the RCSB
Data API and the downloaded original-coordinate mmCIF.  The RCSB entry title
identifies it as a neuropilin-1 b1-domain complex with EG01377; the PDB chemical
component identifier used by this audit is DUE.

This policy does not establish a docking result.  Receptor and ligand
preparation, docking, and reference-pose RMSD are separate recorded steps.
