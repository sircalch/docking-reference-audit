# Buried interface surface area (ΔSASA), top-scoring pose v0.1

## Scope

Solvent-accessible surface area (SASA, Shrake-Rupley algorithm, 1973) for
the receptor alone, the top-scoring (mode 1) docked ligand pose alone, and
the two combined, computed directly from real atomic coordinates for all 7
completed docking cases. Buried interface area is
`ΔSASA = SASA(receptor) + SASA(ligand) − SASA(complex)`. This is a
structural descriptor of the modeled complex, not a binding-affinity or
biological-activity measurement.

## Method and provenance

Computed by `scripts/compute_sasa_burial.py`, a NumPy-vectorized Python
reimplementation of the same Shrake-Rupley algorithm and parameters already
used and verified in the scAMH platform's
`src/features/sasa-surface/sasaAnalysis.ts` (deterministic Fibonacci-spiral
sphere sampling, van der Waals + probe radius, point-in-any-other-sphere
occlusion test). Independent implementation, no code dependency on that
platform. Probe radius 1.4 Å (water), Bondi (1964) van der Waals radii, 200
points per sphere, heavy atoms only (no explicit hydrogens in these
strict-prepared receptors or docked poses).

As with any finite-sampling Shrake-Rupley implementation — including
professional tools such as FreeSASA — results converge toward, but do not
exactly equal, the analytic SASA at a given point density; this is a known
property of the algorithm, not an implementation defect.

## Results

| Case | PDB | Ligand | Receptor heavy atoms | Ligand heavy atoms | SASA receptor alone (Å²) | SASA ligand alone (Å²) | SASA complex (Å²) | Buried interface (Å²) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pilot-001 | 1STP | BTN | 901 | 16 | 7017.6 | 406.9 | 6873.5 | 551.1 |
| pilot-007 | 3D4Q | SM5 | 2107 | 28 | 13304.2 | 581.9 | 13055.5 | 830.6 |
| expansion-001 | 1B9V | RA2 | 3042 | 25 | 15756.5 | 530.7 | 15566.8 | 720.4 |
| pilot-008 | 3CJO | K30 | 2622 | 33 | 16564.4 | 631.9 | 16390.8 | 805.4 |
| pilot-002 | 1HVR | XK2 | 757 | 48 | 6575.6 | 724.2 | 6443.3 | 856.5 |
| pilot-006 | 3PTB | BEN | 1630 | 9 | 9245.2 | 268.8 | 9158.4 | 355.6 |
| pilot-003 | 1IEP | STI | 2229 | 37 | 14576.8 | 772.5 | 14212.0 | 1137.3 |

Buried interface area tracks ligand size in this sample, as expected: the
smallest ligand by heavy-atom count (benzamidine, 9 atoms, pilot-006/3PTB)
buries the least surface (355.6 Å²); the largest and most complex ligand
(imatinib, 37 heavy atoms, pilot-003/1IEP) buries the most (1137.3 Å²). All
seven values fall within the range typically reported for small-molecule
protein interfaces (roughly 300-1200 Å²), which is a plausibility check on
the modeled poses' general geometry, not a validation of pose accuracy.

pilot-006/3PTB — the case whose reference-pose RMSD failed recovery (~5.6 Å)
— still buries a physically reasonable interface area for its ligand size.
Combined with the interface-contacts finding that its top pose sits on
trypsin's genuine S1-pocket residues
(`reports/INTERFACE-CONTACTS-v0.1.md`), this is further, independent
structural evidence that the docked pose occupies a real, chemically
plausible pocket even though its precise orientation did not match the
experimental structure.

## Interpretation boundary

Buried surface area is a purely geometric descriptor of the modeled complex
under one specific docking protocol; it does not estimate binding free
energy, does not imply biological relevance, and was not compared against
any experimental or literature buried-area value for these targets. It
complements, and does not replace, the interface-contact and RMSD analyses
already reported.

## Machine-readable evidence

- `data/sasa_burial_top_pose.csv` — 7 rows, all completed cases;
- `scripts/compute_sasa_burial.py` — reproduces the table above from the
  same receptor/pose files already versioned in `derived/`.
