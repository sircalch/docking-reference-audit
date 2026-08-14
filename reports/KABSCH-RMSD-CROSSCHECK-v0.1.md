# Independent Kabsch-Horn RMSD cross-check v0.1

## Scope

Every reference-pose RMSD reported in this audit is computed by
`scripts/calculate_reference_pose_rmsd.py` using RDKit's
`rdMolAlign.GetBestRMS`. That function is the sole source of every RMSD
number in every report in this repository. This report independently
verifies those numbers with a second, separately implemented algorithm on
the same atomic coordinates, as a reproducibility check — not as a new
result.

## Method

`scripts/verify_rmsd_kabsch.py` reconstructs, for each of the 6 cases with a
verified RMSD, the same identity-mapped atom correspondence RDKit already
established (RCSB CCD atom order → RCSB ideal SDF topology → original mmCIF
coordinates, the same bridge `calculate_reference_pose_rmsd.py` verifies
before trusting any RMSD), then computes the optimal rigid-superposition
RMSD with the classical Kabsch algorithm (Kabsch, 1976), implemented here in
plain NumPy (SVD form) with no call into RDKit's own alignment code. Where a
ligand has molecular symmetry admitting more than one valid atom
correspondence (locally symmetric rings or terminal groups), every
correspondence RDKit's `GetSubstructMatches` returns is tried and the
minimum-RMSD one is kept — the same exhaustive-symmetry search
`GetBestRMS` itself performs, done independently here rather than assumed.

An earlier version of this check used only the first substructure match
returned rather than searching all of them, and disagreed with the reported
value for expansion-001/1B9V by 1.07 Å — not a disagreement between the two
algorithms, but an artifact of an incomplete symmetry search in the
cross-check itself. Fixed before this result was accepted; recorded here for
transparency rather than silently corrected.

## Results

| Case | PDB | Reported RMSD (Å) | Kabsch cross-check (Å) | Δ (Å) |
| --- | --- | ---: | ---: | ---: |
| pilot-001 | 1STP | 0.689 | 0.689 | 0.000 |
| pilot-007 | 3D4Q | 0.769 | 0.769 | 0.000 |
| expansion-001 | 1B9V | 0.930 | 0.930 | 0.000 |
| pilot-008 | 3CJO | 1.504 | 1.504 | 0.000 |
| pilot-002 | 1HVR | 2.493 | 2.493 | 0.000 |
| pilot-006 | 3PTB | 5.594 | 5.594 | 0.000 |

All six values agree with the originally reported RMSD to machine precision
(≤0.001 Å). Two independent implementations — RDKit's C++ `GetBestRMS` and a
from-scratch NumPy Kabsch-SVD implementation — converge on the same value
for every case, given the same identity-mapped atom correspondence.

## Interpretation boundary

This is a reproducibility cross-check of a well-defined mathematical
quantity (minimum-RMSD rigid superposition for a fixed, already-verified
atom correspondence), not independent evidence that the underlying pose or
atom-identity mapping itself is correct — that verification already happens
in `calculate_reference_pose_rmsd.py` (CCD/SDF element order, experimental
heavy-atom completeness, isomeric SMILES match, pose count) and is not
repeated here. Agreement between two implementations of the same optimum
does not prove either is free of unrelated bugs; it does rule out an entire
class of implementation-specific error (a coding mistake unique to one of
the two codebases) for the specific numbers checked here.

pilot-003 (1IEP) is excluded from this check because its RMSD was never
verified in the first place (PDBQT pose-count mismatch; see
`reports/CONTEXTUAL-BATCH-06-08-RESULTS-v0.1.md`) — there is nothing to
cross-check.

## Machine-readable evidence

- `data/kabsch_rmsd_crosscheck.csv`;
- `scripts/verify_rmsd_kabsch.py` — reproduces the table above from the same
  receptor/pose/reference files already versioned in this repository.
