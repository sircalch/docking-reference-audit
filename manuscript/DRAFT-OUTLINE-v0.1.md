# Manuscript outline v0.1 — target: Journal of Molecular Modeling

## Status

This is a working outline, not a submission draft. Every number here is
pulled from the versioned manifests in `data/` and the reports in `reports/`
as of commit `84d336d` (2026-08-13). Nothing here is invented to "fill space"
— where a section needs more content, that is flagged explicitly under
**Gaps to close before submission**, not padded.

## Working title (pick one)

1. *"How often does no-repair receptor preparation actually work? A
   transparent audit of Meeko-based strict preparation on high-resolution
   public PDB structures"*
2. *"A frozen, auditable protocol for reference-pose docking recovery:
   compatibility census and case results from 30 public PDB structures"*
3. *"Strict, no-repair receptor preparation for reference-pose redocking:
   a reproducible compatibility audit"*

Option 2 is probably the best fit for JMM's house style (states the method
and the deliverable, not a rhetorical question). Option 1 is more provocative
and could work as a Short Communication if JMM's editor prefers that framing.

## Article type

**Original Paper** (JMM does not have a strict "Technical Note" category in
its current author guidelines — verify at submission time). Target length:
short-to-medium (this is method/reproducibility content, not a large
screening campaign) — roughly 3500-5000 words plus figures, in line with
JMM's "Computational Methods" thread.

## Abstract (draft — real numbers only)

> Reference-pose redocking is commonly used to validate docking protocols,
> but the receptor-preparation step that precedes it is rarely audited on
> its own terms: preparation failures are typically discarded silently
> rather than reported. We built a frozen, no-repair receptor-preparation
> protocol (Meeko 0.7.1, AutoDock Vina 1.2.5) and applied it, without
> exception or retry, to 30 candidate protein-ligand complexes retrieved
> from the RCSB PDB (X-ray, ≤2.0 Å resolution, one auditable non-polymer
> ligand). Structural classification separated 12 structurally "clean"
> single-chain, single-ligand cases from 18 "contextual" cases requiring an
> explicit, case-specific chain/cofactor/water policy before any processing.
> Across 19 total preparation attempts — the 12 clean cases plus 5
> contextual cases carried through a declared, chemically justified
> component-retention policy — only 4 (21%) produced a receptor accepted by
> Meeko without repair, alternate-location selection, or residue deletion.
> Fourteen of the 15 rejections (93%) failed specifically on unresolved
> alternate side-chain conformers, a pattern that persisted even after
> deliberately sampling lower-resolution candidates. The 4 prepared
> receptors were carried through ligand preparation and identity-mapped,
> RMSD-verified reference-pose docking: two recovered the experimental pose
> to under 0.8 Å, one (with a retained physiological cofactor) to 1.1-1.5 Å,
> and one did not recover the pose at all (~5.6 Å across all nine poses),
> despite successful preparation. We report this negative result alongside
> the positive ones. The full candidate registry, every preparation attempt
> (successful and rejected), and all docking outputs are versioned and
> reproducible from a public code and data repository. [ORCID / affiliation
> / repository URL to be added at submission.]

*(≈250 words — trim to journal limit at final draft; verify JMM's exact
abstract word cap in the current author guidelines before submission.)*

## Keywords (draft)

molecular docking; receptor preparation; AutoDock Vina; Meeko; reproducibility;
reference-pose recovery; protein-ligand complexes; PDB; RMSD; computational
methods audit

## Section outline

### 1. Introduction
- The gap: docking benchmarks report accuracy on cases that already
  prepared successfully; the preparation failure rate itself is rarely
  quantified or discussed as a first-class result.
- What this paper is not: not a docking-accuracy benchmark, not a
  drug-design study, no biological-activity or affinity claim anywhere.
- What it is: a frozen, auditable, no-repair preparation protocol applied
  without exception to a declared candidate pool, with every outcome
  (including rejections) reported.
- Restate the guiding research question from `README.md`: what
  documentable conditions of provenance, structure, composition, and
  preparation let one decide whether a public complex is fit for a
  reference-pose redocking experiment.

### 2. Methods
- **2.1 Candidate registration and inclusion criteria** — X-ray, ≤2.0 Å,
  exactly one auditable non-polymer ligand entity verified via the RCSB
  Data API (not entry-level summary counts alone — cite the two false
  positives caught this way, see Limitations). Registry capped at 30
  candidates by a pre-declared expansion plan.
- **2.2 Structural classification** — clean (single model, single chain,
  single ligand instance, no other non-polymer component) vs. contextual
  (everything else); automated via `scripts/classify_structural_eligibility.py`.
- **2.3 Frozen no-repair preparation policy** — chain/ligand-instance
  selection by minimum original-coordinate ligand-to-polymer atom distance;
  water and declared ligand always removed; Meeko 0.7.1 run with no
  alternate-location choice, no repair, no `--allow_bad_res`, no residue
  deletion.
- **2.4 The retained-component extension** — how and why five contextual
  cases were processed under an explicit, chemically justified
  component-retention policy instead of blanket stripping (cite the two
  concrete justifications used: KSP/Eg5 nucleotide cofactor in 3CJO,
  trypsin's structural Ca²⁺ site in 3PTB; and the one case, 9HOO, where the
  "extra component" turned out to be a covalently modified in-chain residue
  rather than a ligand at all).
- **2.5 Docking and reference-pose RMSD** — AutoDock Vina 1.2.5 via WSL,
  fixed seed, one CPU, exhaustiveness 8, box derived from experimental
  ligand coordinates; identity-mapped heavy-atom RMSD verified via
  CCD-to-SDF atom order, heavy-atom identity, isomeric SMILES, and pose
  count before being trusted (distinguish explicitly from Vina's own
  pose-to-best-pose RMSD, which is not a reference-pose metric). State
  explicitly that RMSD is computed with RDKit's `rdMolAlign.GetBestRMS`,
  which (a) resolves the correct atom correspondence between the
  RCSB-ideal-SDF-derived reference molecule and the PDBQT-derived docked
  molecule via symmetry-aware substructure matching — necessary because the
  two are built by independent pipelines with different atom orderings, not
  optimized/checked against each other — and (b) additionally performs a
  best-fit rigid superposition on top of that correspondence. This was
  checked directly during this audit (naive same-index RMSD without correct
  atom correspondence gives nonsensical values, 5-8 Å, even for the
  best-recovered cases; using the correct substructure-matched
  correspondence without any further alignment gives values close to but
  systematically ≥ `GetBestRMS`'s reported value, by roughly 0.03-0.6 Å
  across the cases checked) — the rigid-alignment component is a modest,
  bounded correction, not a source of misleading "forgiveness" of genuine
  positional error, but this should be disclosed plainly rather than left
  implicit, since a reviewer familiar with redocking metrics may otherwise
  assume raw, unaligned RMSD.
- **2.6 Reproducibility statement** — every script, manifest, and output
  is versioned; commands to regenerate all figures and tables from the
  repository are given explicitly.

### 3. Results
- **3.1 Registry outcome** — 30/30 candidates retrieved and checksummed;
  12 clean / 18 contextual / 0 review-required.
- **3.2 Strict preparation census** — table of all 19 attempts (12 clean +
  5 contextual with declared policy); 4 prepared / 15 failed; failure-class
  breakdown (`meeko_alternate_location_requires_choice` ×10,
  `meeko_alternate_location_and_template_matching_failed` ×4,
  `meeko_template_matching_failed` ×1).
- **3.3 The resolution observation** — within the subset of clean cases
  with recorded resolution (8 cases, all 0.8-0.99 Å), all 8 failed, all on
  an alternate-location-related class; explicitly frame as descriptive of
  this sample, not a general claim.
- **3.4 Four completed reference-pose cases** — table + per-case narrative:
  1STP/BTN (0.689 Å), 3D4Q/SM5 (0.769 Å), 3CJO/K30 with retained ADP-Mg
  (1.504 Å top-score / 1.154 Å best), 3PTB/BEN with retained Ca²⁺ (~5.6 Å,
  no recovery). State plainly that preparation success and pose-recovery
  success are shown here to be separate outcomes.
- **3.5 The 9HOO relabeling** — a short subsection on the false "extra
  component" flag turning out to be a covalently modified in-chain residue,
  as a worked example of why entry-level non-polymer counts should not be
  trusted without atom-level inspection.

### 4. Discussion
- Preparation failure is not the exception here, it is the majority
  outcome (79%) even before any biological question is asked — this is
  worth stating plainly as a caution for anyone building an automated
  docking pipeline on "clean-looking" high-resolution PDB entries.
- Alternate-location incompatibility as the dominant, specific, and
  addressable (with a different tool policy) failure mode — useful,
  actionable information for tool users, distinct from a vague "docking is
  hard" statement.
- The n=4 docking outcomes should not be read as an accuracy estimate; they
  are illustrative of the pipeline's end-to-end functioning and of the
  fact that preparation success does not guarantee pose recovery.
- Reproducibility as a first-class contribution: every claim in this paper
  can be regenerated from the public repository.

### 5. Limitations
- Small, resolution-skewed candidate pool (drawn disproportionately from
  sub-1-Å structures because that stratum dominates the discovery ranking
  used).
- n=4 completed docking cases is not sufficient for any accuracy or
  recovery-rate claim.
- Findings describe compatibility with one specific tool version (Meeko
  0.7.1) and one specific no-repair policy; not a statement about Meeko,
  Vina, or AutoDock-family tools in general.
- 13 of 18 contextual candidates remain unprocessed (no declared policy
  yet) — state this as future work, not as a gap in the reported results.

### 6. Data and code availability
- Public repository URL (add before submission).
- Every manifest, script, and generated figure referenced by exact path.
- Explicit reproduction commands (validation suite already used throughout
  this project: `py_compile`, `classify_structural_eligibility.py`,
  `render_audit_figures.py`, `verify_subpilot_evidence.py`).

## Figure and table plan

| # | Content | Source | Status |
| --- | --- | --- | --- |
| Fig. 1 | Structural inventory disposition (clean/contextual/review-required) | `reports/generated/figures/figure-01-structural-inventory` | **exists**, regenerate with current 23-attempt totals |
| Fig. 2 | Strict preparation outcomes (prepared/failed by class) | `figure-02-strict-preparation` | **exists**, regenerate |
| Fig. 3 | Reference-pose RMSD vs. Vina score, all verified completions | `figure-03-reference-pose-outcomes` | **exists**, regenerate — now aggregates all contextual batches via glob, filtered to `mapping_status == verified` (fixed a real bug this pass: the function crashed on unverified rows and its 4-color palette silently dropped points past the 4th case) |
| Fig. 4 | Evidence flow (candidates → retrieved → classified → prepared → docked) | `figure-04-evidence-flow` | **exists**, regenerate |
| Fig. 5 | 3D binding-site renders: docked top pose vs. experimental pose, receptor backbone context, for each of the 7 completed docking cases (1STP, 3D4Q, 3CJO, 3PTB, 1HVR, 1IEP, 1B9V) | `reports/generated/figures/binding-sites/binding-site-<case>-<PDB>.png`, generated by `scripts/render_binding_site_figures.py` | **done** — matplotlib 3D, not PyMOL (pymol-open-source's native module failed to load on this Windows environment; matplotlib was used instead, reusing coordinates already computed and identity-verified by `calculate_reference_pose_rmsd.py`). Caption should note that a single static 3D projection can visually understate or overstate depth separation — the RMSD number, not the image, is the quantitative claim. A second, publication-grade version of this figure now also exists interactively in the scAMH platform's "Docking Reference Audit" project (real 3Dmol.js cartoon receptor + colored stick poses) — see "Platform integration" below; a screenshot/capture from there could replace or supplement the matplotlib version if a more polished look is wanted before submission. |
| Fig. 6 (new, optional) | Workflow/protocol diagram (candidate registration → classification → preparation → docking → RMSD verification) | not yet produced | **gap — moderate value, mostly for reader orientation** |
| Table 1 | Inclusion criteria and structural classification rule | text-only, write directly in manuscript | — |
| Table 2 | All 23 preparation attempts (case, PDB, batch, outcome, failure class) | already exists as the table in `reports/STRICT-PREPARATION-SUMMARY-v0.1.md` | reuse directly |
| Table 3 | 7 completed docking cases (case, PDB, ligand, top-score affinity, top-score RMSD, best RMSD, verified?) | already exists as the table in `reports/AUDIT-SYNTHESIS-v0.1.md` | reuse directly |
| Table 4 (new) | Receptor-ligand interface contacts and H-bond candidates for the top-scoring pose, all 7 completed cases | already exists as the table in `reports/INTERFACE-CONTACTS-v0.1.md`, data in `data/interface_contacts_top_pose.csv` / `data/hydrogen_bonds_top_pose.csv` | **done** — real, coordinate-derived (4.5 Å contact / 3.5 Å N-O H-bond heuristic), includes two chemically notable findings (1IEP's closest contact is the Abl kinase T315 gatekeeper residue; 3PTB's top pose sits in the correct S1 pocket residues despite failing the RMSD threshold) |
| Table 5 (new) | Independent Kabsch-Horn cross-check of every reported RMSD (6 cases) | already exists as the table in `reports/KABSCH-RMSD-CROSSCHECK-v0.1.md`, data in `data/kabsch_rmsd_crosscheck.csv` | **done** — a from-scratch NumPy implementation, independent of RDKit's `GetBestRMS`, agrees with every reported RMSD to machine precision (≤0.001 Å); strong reproducibility content for the Methods section |
| Table 6 (new) | Buried interface surface area (ΔSASA) for the top-scoring pose, all 7 completed cases | already exists as the table in `reports/SASA-BURIAL-v0.1.md`, data in `data/sasa_burial_top_pose.csv` | **done** — real, coordinate-derived Shrake-Rupley SASA; buried area tracks ligand size as expected (355.6-1137.3 Å²), and corroborates the 3PTB "right pocket, wrong orientation" characterization from Table 4 |

## Platform integration

The docking-reference-audit is now also viewable as an independent project
inside the scAMH platform (`C:\visualizassss\proyecto-doctorado\visualizacion`,
project "Docking Reference Audit", route `docking_audit`), entirely separate
from that platform's doctoral project. It reuses the platform's existing,
already-built `ThreeDmolDockingViewer` component (real 3Dmol.js rendering,
not the matplotlib fallback used for Fig. 5) against the same real receptor
PDB and Vina PDBQT files from `derived/strict-receptors/` and
`derived/vina-runs/`, copied into that platform's
`public/data/docking-audit/`. This is a visualization/exploration surface,
not a data source — every number shown there is copied from, not computed
by, this repository's reports. Useful for interactively inspecting each of
the 7 cases and for producing a higher-quality figure capture than the
matplotlib renders if desired before submission.

## Gaps to close before submission

1. ~~Figure 5 (3D binding-site renders) does not exist yet.~~ **Done.**
   `scripts/render_binding_site_figures.py` produces one figure per completed
   docking case, all 7 rendered. Still open: these are matplotlib-based, not
   PyMOL cartoon+surface renders, which is what a JMM reviewer more typically
   expects from a structural docking figure. If time allows before
   submission, revisit PyMOL (the pymol-open-source pip wheel installed but
   its native `_cmd` module failed to load — `ImportError: DLL load failed`
   — likely a missing Windows OpenGL/runtime dependency, uninstalled again
   rather than leaving a broken dependency in place). A working PyMOL render
   would be a straightforward upgrade of the same figures without redoing
   the underlying data extraction.
2. **Regenerate figures 1-4 against the current 23-attempt state** — the
   files in `reports/generated/figures/` are not versioned (by design,
   `.gitignore`), so whoever writes the manuscript must re-run
   `python scripts/render_audit_figures.py` and pull fresh exports before
   drafting figure captions.
3. **No independent reproduction has been run from a clean checkout** —
   worth doing once before submission so the "reproducibility" claim in the
   abstract is itself verified, not asserted.
4. **Author list, affiliations, ORCID, funding/COI statement** — none of
   this is present in the repository and must come from the user, not be
   invented.
5. **Repository publication decision** — the manuscript's data-availability
   section needs a real, public URL. The project has explicit standing
   instructions to never create a GitHub remote or publish without new
   authorization — this must be revisited deliberately when ready to submit,
   not assumed.
6. **JMM's current author guidelines** (word/figure limits, reference style,
   submission categories) have not been checked against this outline — pull
   them directly from Springer before final formatting.
7. **Optional but valuable: 2-3 more contextual cases** processed under the
   same chemically-justified retained-component discipline, to grow both
   the preparation-attempt census and, if any succeed, the docking-outcome
   table beyond n=4.
