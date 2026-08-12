# Candidate discovery procedure v0.1

## Aim

This document fixes the discovery route used to identify *candidates*. It is
not an eligibility rule and does not produce a docking result. Eligibility is
determined later from the original-coordinate mmCIF inventory.

## Primary public source and query frame

Candidates are discovered from the RCSB PDB Search API with these entry-level
conditions:

1. experimental method is `X-RAY DIFFRACTION`;
2. reported combined resolution is <= 2.0 Å;
3. the entry reports exactly one distinct non-polymer entity, excluding
   solvent.

The returned IDs are ranked by reported resolution. Each selected ID is then
checked with the RCSB Data API before registration. Candidate discovery never
assumes that the one non-polymer entity is the intended ligand: salts,
solvents, metabolites, cofactors, ions, and unsuitable components are rejected
at that stage and recorded if registered.

## Selection within the discovery frame

For a new clean-execution batch, inspect entries in ascending result order and
register the first previously unaudited organic small-molecule protein complex
whose component is not an obvious solvent, simple ion, common crystallization
additive, or prosthetic group. The mmCIF inventory is then authoritative for
the clean/contextual classification.

If a candidate is contextual or fails strict preparation, retain its result and
continue in the predeclared ascending order. Do not replace it merely because
its outcome is inconvenient.

## Exclusions at discovery

The following are not intended reference ligands under this procedure:

- water, simple inorganic ions, and monoatomic metals;
- common buffer or crystallization components (for example sulfate, phosphate,
  glycerol, ethanol, DMSO, PEG-like additives, and nitrate);
- covalent prosthetic groups and porphyrins;
- nucleotides or ordinary metabolic substrates, unless a later protocol
  explicitly broadens the research question.

## Audit trail

Every registered candidate stores its RCSB entry URL, registration timestamp,
downloaded mmCIF checksum, frozen structural inventory, and deterministic
policy proposal. The query semantics and supported comparison operators are
documented by RCSB PDB's Search API.
