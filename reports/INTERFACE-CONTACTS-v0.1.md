# Receptor-ligand interface contacts (top-scoring pose) v0.1

## Scope

This report adds a real, coordinate-derived per-case interaction analysis to
the seven completed docking runs: for each case's top-scoring (mode 1) Vina
pose, the receptor residues within 4.5 Å (any heavy-atom pair) and a
heavy-atom-only hydrogen-bond candidate list (N/O···N/O ≤ 3.5 Å, no explicit
hydrogens, no donor-acceptor angle check — a LigPlot/PLIP-style
approximation, not a validated H-bond network). It is descriptive structural
context, not a binding-affinity or biological-activity claim.

## Method and provenance

Computed by `scripts/compute_interface_contacts.py`, a standalone Python
reimplementation of the exact algorithm and thresholds already used and
validated in the scAMH platform's
`src/features/interface-contacts/interfaceContacts.ts` (residue-contact
cutoff 4.5 Å, H-bond heuristic 3.5 Å N/O···N/O). The two implementations are
independent — this repository has no code dependency on that platform — but
intentionally share the same thresholds and convention so results are
directly comparable to what the scAMH docking-audit project screen shows.
Inputs: the same strict-prepared receptor PDB and Vina output PDBQT already
used throughout this audit; only the first (`mode 1`) MODEL block of each
PDBQT is analyzed.

## Results

| Case | PDB | Ligand | Residue contacts (≤4.5 Å) | H-bond candidates (≤3.5 Å) | Closest contact |
| --- | --- | --- | ---: | ---: | --- |
| pilot-001 | 1STP | BTN | 17 | 7 | Ser45 (2.264 Å) |
| pilot-007 | 3D4Q | SM5 | 17 | 3 | Glu501 (2.047 Å) |
| expansion-001 | 1B9V | RA2 | 17 | 7 | Arg374 (2.039 Å) |
| pilot-008 | 3CJO | K30 | 16 | 1 | Gly117 (2.997 Å) |
| pilot-002 | 1HVR | XK2 | 15 | 3 | Asp29 (2.616 Å) |
| pilot-006 | 3PTB | BEN | 17 | 5 | Gly219 (2.118 Å) |
| pilot-003 | 1IEP | STI | 23 | 6 | Thr315 (2.240 Å) |

## Two contacts worth noting explicitly

- **pilot-003 (1IEP, imatinib)**: the closest receptor contact to the
  top-scoring docked pose is **Thr315**, the well-known Abl kinase
  "gatekeeper" residue whose mutation to isoleucine (T315I) is the classic
  clinical imatinib-resistance mutation. This is chemically consistent with
  imatinib's known binding mode and is an independent, coordinate-level
  sanity check on the docked geometry for a case whose reference-pose RMSD
  could not itself be verified (pose-count mismatch, see
  `reports/CONTEXTUAL-BATCH-06-08-RESULTS-v0.1.md`).
- **pilot-006 (3PTB, benzamidine)**: despite this case's poor reference-pose
  RMSD (~5.6 Å, reported as a negative result), the top-scoring pose's
  closest receptor contacts (Gly219, Ser190, Asp189) are trypsin's classical
  S1 specificity-pocket residues, Asp189 in particular being the textbook
  determinant of trypsin's substrate specificity. The docked pose therefore
  landed in a chemically plausible region of the correct pocket even though
  its precise orientation did not match the experimental structure closely
  enough to count as recovery under the RMSD threshold — a more specific
  characterization of that failure mode than "wrong site" would suggest.

## Interpretation boundary

Contact and hydrogen-bond counts describe geometry of one specific pose
(Vina's top-scoring mode) under one specific docking protocol; they are not
a validated interaction fingerprint, do not imply binding affinity or
biological relevance, and were not cross-checked against literature-reported
binding modes beyond the two residues noted above, which are cited only
because they are unambiguous, well-established facts about these specific
targets (Abl T315I gatekeeper; trypsin Asp189 S1 pocket), not as a
systematic literature validation of every contact.

## Machine-readable evidence

- `data/interface_contacts_top_pose.csv` — 122 rows, all 7 cases;
- `data/hydrogen_bonds_top_pose.csv` — 32 rows, all 7 cases;
- `scripts/compute_interface_contacts.py` — reproduces both files from the
  same receptor/pose files already versioned in `derived/`.
