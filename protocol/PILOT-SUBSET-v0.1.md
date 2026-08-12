# Frozen clean-case subpilot v0.1

## Decision

The first strict-preparation subpilot contains only cases with one proposed
ligand–receptor pair and no other non-polymeric components in the original
coordinate inventory:

| Case | PDB | Ligand | Proposed receptor chain | Status |
|---|---|---|---|---|
| pilot-001 | 1STP | BTN | A | accepted for strict-preparation feasibility test |
| pilot-004 | 1FPU | PRC | A | accepted for strict-preparation feasibility test |
| pilot-007 | 3D4Q | SM5 | A | accepted for strict-preparation feasibility test |

## Frozen policy

- Use the original RCSB mmCIF whose SHA-256 is recorded in
  `data/retrieval_manifest.csv`.
- Select the receptor chain and ligand instance recorded in
  `data/case_policy_proposals.csv`.
- Remove crystallographic water according to the predeclared water policy.
- Do not add atoms, repair residues, choose alternate conformers manually,
  remove unexpected components after an error or retry with altered settings.
- A preparation failure is recorded as a result, not corrected silently.

## Deferred expansion cases

`pilot-002`, `pilot-003`, `pilot-005`, `pilot-006` and `pilot-008` are retained
for a later amendment. Their coordinate inventories show additional components
or receptor context requiring an explicit scientific policy. They are not
included in the clean-case subpilot and are not considered failures.

## Boundary

This subpilot only evaluates whether a documented strict preparation can be
performed. It does not constitute docking performance, binding affinity or
biological validation.
