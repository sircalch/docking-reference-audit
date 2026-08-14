# Independent reproducibility verification v0.1

## Scope

The abstract and every report in this repository claim the audit is fully
reproducible from versioned scripts and manifests. This report is the first
time that claim was actually tested rather than asserted: every stage of
the pipeline was re-run independently and compared against the already
committed results. No prior report in this repository had done this.

## What was tested and how

**1. Structural classification, extraction, and strict preparation — all
19 clean/subpilot batches and 9 contextual batches (all 23 preparation
attempts).** Re-ran `classify_structural_eligibility.py`,
`extract_strict_receptors.py`, and `run_strict_meeko_preparation.py` for
every batch from the already-retrieved raw mmCIF files. Compared every
resulting manifest against the committed version field-by-field for the
columns that carry scientific meaning: `input_sha256`, `status`,
`normalized_error_class`, `exit_code`.

**Result: zero substantive differences across all 20 preparation manifests
and the eligibility register.** The only differences found were output
directory paths (a small number of early batches historically used
per-batch subdirectories rather than the shared default path — a naming
inconsistency, not a reproducibility failure) and `completed_at_utc`
timestamps, neither of which carries scientific content. Every prepared/
failed outcome and every `normalized_error_class` reproduced exactly.

**2. Reference-pose RMSD calculation — all 6 verified cases plus the 1
unverified case.** Re-ran `calculate_reference_pose_rmsd.py` for the
original two-case subpilot and all five contextual batches with docking
results (04-08), from the already-downloaded raw structures, ligand SDFs,
and Vina outputs. Diffed the full output CSV (all columns: mode, affinity,
RMSD, `mapping_status`, `mapping_note`) against the committed file.

**Result: byte-identical output for all 6 batches, 63 pose rows total**,
including contextual_batch_07 (pilot-003/1IEP), whose `mapping_status =
not_verified` and exact pose-count-mismatch error message reproduced
exactly — the audit's one known technical failure is itself fully
reproducible, not a one-off fluke.

**3. Live re-verification against the public source (not just internal
consistency).** Re-downloaded three representative structures directly from
RCSB (`https://files.rcsb.org/download/{PDB}.cif`) — 1STP (a clean,
sub-1-kDa case), 3PTB (the negative-recovery case), and 1IEP (the
technically-unverifiable case) — and compared SHA-256 checksums against
`data/retrieval_manifest.csv`, recorded roughly two years earlier in
audit-session time (`retrieved_at_utc: 2026-08-12`).

**Result: all three checksums matched exactly.** The public RCSB structures
this audit depends on have not changed, and the recorded checksums remain a
valid, currently-verifiable fingerprint of the exact input data used.

**4. Full docking determinism — one complete Vina re-run.** Re-ran
`run_wsl_vina_subpilot.py` for the original two-case subpilot (1STP, 3D4Q)
end to end (WSL, AutoDock Vina 1.2.5, fixed seed 20260812, one CPU,
exhaustiveness 8) into a separate scratch output directory, and compared
the SHA-256 checksum of the entire output PDBQT file (all nine poses) against
the committed run manifest.

**Result: the output PDBQT files are byte-identical**, not just
score-equivalent — every atom coordinate in every one of the 9 poses for
both cases reproduced exactly under the fixed seed.

## Interpretation

Every stage of this audit's pipeline — structural classification, receptor
extraction, strict preparation, ligand docking, and RMSD verification — was
independently confirmed deterministic and reproducible from the versioned
inputs in this repository, without relying on any cached intermediate
result. This does not mean the pipeline is free of bugs elsewhere (a
deterministic bug reproduces just as exactly as correct behavior); it means
the specific "reproducible from this repository" claim made throughout this
project's reports is verified, not merely asserted.

## What this did not test

- Reproduction was not attempted from a fully empty checkout with no
  `raw/structures/` or `derived/` content at all — the RCSB re-download
  check (item 3) tests the live-source dependency directly and separately
  from the rest of the pipeline, which is a more targeted test of the same
  underlying risk (an external resource becoming unavailable or changing)
  without requiring every one of the 30 structures to be re-fetched.
- Preparation and docking were not re-run inside a machine with a different
  OS, Meeko/Vina build, or WSL configuration than the one this audit has
  used throughout; cross-environment reproducibility (a different analyst's
  machine) remains untested.

## Machine-readable evidence

This check was procedural (re-running existing scripts and diffing outputs
in place) rather than producing new persisted data files; no new CSV is
added to `data/`. The verification commands are recorded above and can be
re-run directly against this repository's existing scripts and manifests.
