# Protocol v0.1 — curated reference complexes for docking audits

## 1. Scope

This protocol defines a bounded, computational-only dataset of public experimental protein–small-molecule complexes for reference-pose recovery experiments. It is deliberately independent of any doctoral thesis project.

Initial target: **20–30 eligible cases** from RCSB PDB. The first release may contain fewer cases if the inclusion rules leave fewer valid candidates; the final sample size will not be enlarged by relaxing criteria after reviewing docking outcomes.

## 2. Unit of analysis

One case is one PDB entry plus one explicitly identified non-polymeric ligand component, receptor chain set, preparation record and reference-pose extraction. An entry can yield multiple candidate cases, but each is adjudicated separately.

## 3. Inclusion criteria

A candidate is eligible only when all conditions below can be recorded before docking:

1. Public RCSB PDB experimental entry with stable PDB identifier.
2. Protein receptor and a non-polymeric small-molecule ligand with a defined component ID.
3. Coordinate file available in mmCIF and/or legacy PDB at the retrieval date.
4. Experimental method, release date and resolution/quality fields available from the RCSB Data API where applicable.
5. A reference ligand pose can be extracted without guessing atom identity.
6. The selected receptor/ligand policy, retained cofactors and removed components are recorded.

## 4. Exclusion criteria

Exclude, retaining the reason, when any applies:

- ligand is a solvent, buffer, ion, crystallization additive or polymeric entity;
- alternate locations, missing atoms, ambiguous component identity or atom mapping prevent an auditable reference pose;
- the receptor contains an unresolved requirement that the declared preparation policy cannot handle;
- the required coordinates or primary metadata cannot be retrieved and checksummed;
- case only works after undocumented manual repair.

Failure of a preparation command is **not** an exclusion by itself. It is a recorded audit outcome.

## 5. Frozen procedure per case

1. Register the candidate in `data/candidates.csv` before processing.
2. Retrieve the original structure from its recorded RCSB URL; store retrieval timestamp and SHA-256 checksum.
3. Retrieve primary metadata and public validation-report URL.
4. Declare receptor chains, ligand component ID, retained cofactors, water policy and preparation profile.
5. Run strict preparation first: no manual repair, atom addition, alternate-location selection or post hoc deletion beyond the declared profile.
6. Record the outcome, normalized error class, program versions and command parameters.
7. If strict preparation succeeds, run bounded redocking only with the predeclared engine/configuration.
8. Extract all returned poses. Report top-score and identity-mapped, aligned heavy-atom RMSD separately; never select the best value without stating the selection rule.
9. Generate the case report and mark it included, excluded or pending review.

## 6. Outcomes

Primary descriptive outcomes:

- proportion of candidates with auditable provenance;
- proportion accepted by strict preparation;
- normalized preparation failure classes;
- fraction of prepared cases with an extractable reference pose;
- redocking recovery distribution for cases that complete under the frozen configuration.

No biological activity, binding affinity or clinical conclusion will be inferred from docking scores or RMSD.

## 7. Reproducibility record

Every processed case must have:

- PDB ID, ligand component ID and selected chains;
- source URL, retrieval time and SHA-256;
- input/output filenames and hashes;
- engine and package versions;
- full declared parameters or a versioned configuration reference;
- result status, reason and timestamps.

## 8. Candidate manifest schema

`data/candidates.csv` is the pre-analysis registry. Required fields:

```text
case_id,pdb_id,ligand_component_id,receptor_chains,candidate_source_url,
selection_rationale,registered_at_utc,status,exclusion_reason
```

Allowed initial statuses: `candidate`, `metadata_verified`, `strict_preparation`, `included`, `excluded`, `pending_review`.

## 9. Versioning and amendments

Any change to criteria, engine version or preparation profile requires a dated amendment explaining whether previously processed cases must be rerun. No candidate may be silently overwritten or removed.

## 10. Current limitations

This repository has no downloaded structures and no computed results at v0.1. It is not evidence of docking performance until a frozen candidate manifest, verifiable inputs and reproducible executions exist.
