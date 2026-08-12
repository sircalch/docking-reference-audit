# Controlled expansion plan v0.1

## Rationale

The three-case clean structural-preparation subpilot established the audit and
reference-pose workflow. It is intentionally too small for a performance claim.
The next release should aim for **12 completed reference-pose cases**, while
retaining every strict-preparation failure and every non-eligible candidate.

## Two strata

1. **Clean stratum:** protein + declared small-molecule ligand, with no other
   non-polymeric component after the frozen inventory.
2. **Contextual stratum:** a declared ligand is present with ions, cofactors,
   modified residues, or multiple polymeric chains. Each case requires a
   predeclared retention/removal decision before preparation.

The two strata will be summarized separately. The contextual cases will never
be silently normalized into the clean stratum.

## Stopping rule

Stop candidate collection when either 12 completed reference-pose cases are
available or 30 candidates have been fully audited, whichever occurs first.
This prevents outcome-driven growth of the benchmark.

## Before a case can run

- record it in `data/candidates.csv`;
- retrieve original mmCIF and metadata with checksums;
- inventory chains, declared ligand and other components;
- record a case policy before receptor preparation;
- run the same strict preparation and retain its outcome;
- only dock a case whose receptor and ligand preparation succeed;
- verify every completed case with `verify_subpilot_evidence.py`.

## Reporting boundary

The expanded dataset may describe preparation compatibility and reference-pose
recovery under a specified workflow. It will not be described as a universal
benchmark of docking software, nor as evidence of ligand potency or biological
activity.
