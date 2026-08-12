# Contextual expansion batch 01 v0.1

## Scope

This register adds eight public protein--small-molecule structure candidates
to the controlled expansion plan.  It records metadata, original-coordinate
mmCIF retrieval, checksums, structural inventory, and a deterministic *draft*
selection proposal.  It does **not** approve a receptor representation, run
preparation, or produce docking results for any listed case.

The additions are intentionally classified as contextual because at least one
of the following was observed in the frozen structural inventory: multiple
polymeric chains, additional ligands/cofactors, metal ions, or carbohydrate
components.  They must remain separate from the clean stratum.

## Registered cases

| Case | PDB / declared ligand | Context that requires an explicit decision |
| --- | --- | --- |
| expansion-001 | 1B9V / RA2 | Ca and NAG components |
| expansion-002 | 1CDE / DZF | Four chains and GAR components |
| expansion-003 | 1E66 / HUX | NAG components |
| expansion-004 | 1H22 / E10 | NAG components |
| expansion-005 | 1KZK / JE2 | Two chains, chloride and EDO components |
| expansion-006 | 1MZC / BNE | Two chains, FPP, sugars, and Zn |
| expansion-007 | 1N1M / A3M | Two chains, glycans, and Hg |
| expansion-008 | 1R55 / 097 | Metal ions, glycans, and chloride |

## Reproducibility records

The machine-readable evidence is deliberately kept in the following files:

- `data/candidates.csv`: candidate registration and source entry endpoint;
- `data/retrieval_manifest.csv`: source URL, retrieval timestamp, byte count,
  and SHA-256 for each original mmCIF;
- `data/structure_inventory.csv`: frozen counts of models, polymer chains,
  ligand instances, and other non-polymeric components;
- `data/eligibility_register.csv`: mechanical clean/contextual classification
  from the frozen inventory; it is not an execution result;
- `data/case_policy_proposals.csv`: deterministic ligand/receptor proximity
  proposal, marked `proposal_pending_researcher_review`.

## Required review before any execution

For each individual case, record a written policy that specifies: (1) the
polymer chain or chains retained; (2) whether every listed non-target component
is retained or removed and why; (3) the water policy; and (4) the criterion
used to determine eligibility.  In particular, metal ions, cofactors, and
glycans must not be discarded merely to obtain a successful preparation.

Only after this record is frozen may the existing strict extraction,
preparation, ligand preparation, box derivation, Vina, and reference-RMSD
steps be applied.  A failure remains an observed outcome and is not grounds
for changing the policy retrospectively.

## Status at registration

All eight cases are `ready_for_policy_review`; none is an eligible completed
reference-pose case.  The original three-case strict subpilot and its 18
retained poses are unaffected by this registration batch.
