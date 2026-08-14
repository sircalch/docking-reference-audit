# Manuscript outline v0.1 — target: Journal of Molecular Modeling

## Status

This is a working outline, not a submission draft. Every number here is
pulled from the versioned manifests in `data/` and the reports in `reports/`
as of commit `84d336d` (2026-08-13). Nothing here is invented to "fill space"
— where a section needs more content, that is flagged explicitly under
**Gaps to close before submission**, not padded.

## Authors (confirmed 2026-08-14)

Same three authors and order as the companion 102-target DUD-E manuscript
("A provenance-aware workflow for strict receptor-preparation audits and
reference-pose recovery in molecular docking", currently under review at
JMM, not yet published):

1. **Andrés Monreal Hernández** (corresponding) — Universidad Estatal de
   Sonora, Hermosillo, Sonora, Mexico. ORCID: 0009-0009-1207-8597.
   andres.monreal@ues.mx
2. **Sara Lizbeth Franco Amaya** — Doctorado en Nanotecnología,
   Universidad de Sonora, Hermosillo, Sonora, Mexico. ORCID:
   0009-0005-0272-0241
3. **Carlos Ivanhoe Martínez Osorio** — Doctorado en Ciencia de Materiales,
   Universidad de Sonora, Hermosillo, Sonora, Mexico. ORCID:
   0009-0003-7872-4965

## Relationship to the companion 102-target manuscript

The companion manuscript (same three authors) audits 102 DUD-E
target/PDB pairs under a related but distinct protocol (Meeko strict
preparation across three source-and-reader conditions: original DUD-E PDB,
official RCSB mmCIF, official RCSB legacy PDB) and reports two
reference-pose cases, BRAF/3D4Q/SM5 and KIF11/3CJO/K30, docked with Vina
1.2.7 (exhaustiveness 16, seed 20260809). **This manuscript's registry is
different** (30 candidates from a frozen RCSB clean-discovery ranking, not
DUD-E) **but shares two PDB identifiers as reference cases** (3D4Q, 3CJO)
under different protocol parameters (Vina 1.2.5, exhaustiveness 8, seed
20260812) and reports different RMSD values for them, since the
preparation/docking runs are independent. This must be handled explicitly,
not silently:

- The companion manuscript is **under review, not yet published** — per
  JMM's own reference-list rule ("only includes works that are cited in
  the text and that have been published or accepted for publication"), it
  cannot be a numbered reference. It should be mentioned in-text as
  work by the same authors currently under review (e.g. "a related,
  independently parameterized audit of 102 DUD-E targets by the same
  authors is under review elsewhere"), not cited as `[N]`.
- The Introduction and/or Discussion should state plainly that 3D4Q and
  3CJO appear in both studies under different Vina configurations and
  seeds, and that the two RMSD values for each are not expected to match
  and should not be treated as a replication of each other — they are two
  independent runs under two independently frozen protocols.
- This is a disclosure/scope-clarity matter, not a duplicate-submission
  problem: the registries, inclusion criteria, and central finding (a
  30-candidate compatibility census with contextual-case cofactor
  retention vs. a 102-target three-condition source comparison) are
  substantively different studies.

## AI-use disclosure (required by JMM policy, drafted for Methods)

JMM requires LLM use to be documented in the Methods section. Confirmed
final wording (2026-08-14), kept brief and generic per the authors'
preference:

> "A large language model (LLM) was used as a computational aid during
> this study, under the authors' direction and review. The authors are
> responsible for the study design, interpretation, and final manuscript
> text."

Kept short and non-itemized rather than listing specific uses, per the
authors' request — but not reduced to a description narrower than what
was actually done (e.g. "data arrangement only"), since the public
repository (github.com/sircalch/docking-reference-audit) already carries
a `Co-Authored-By: Claude` trailer with detailed technical descriptions on
every commit touching scripts, analysis, or reports. A disclosure
inconsistent with that visible, public record would be a real submission
risk; a brief but accurate one is not.

## Statements and Declarations (confirmed 2026-08-14)

Placed after References, exact JMM-required heading "Statements and
Declarations":

**Funding**
> "The authors declare that no funds, grants, or other support were
> received during the preparation of this manuscript."

**Competing Interests**
> "The authors have no relevant financial or non-financial interests to
> disclose."

**Author Contributions** — still needs the specific per-author breakdown
(who did what) from the authors; JMM's own example statement is a
reasonable template ("All authors contributed to the study conception and
design...").

**Data Availability**
> "The datasets, protocol, and scripts generated and analysed during the
> current study are available in the docking-reference-audit repository,
> https://github.com/sircalch/docking-reference-audit."
Should be updated to the Zenodo DOI once a release is cut (see gap 5
below).

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

**Original Paper (Research)** — confirmed against JMM's live submission
guidelines (link.springer.com/journal/894/submission-guidelines, checked
2026-08-14). JMM's peer-reviewed article types are: Original Papers
(Research), Reviews, Short Comments, Software Reports, Brief Reports. No
formal "Technical Note" category exists; "Original Paper" is the correct
choice for this manuscript, not a placeholder guess. Target length:
short-to-medium (this is method/reproducibility content, not a large
screening campaign) — roughly 3500-5000 words plus figures, in line with
JMM's "Computational Methods" thread.

## Confirmed journal requirements (verified 2026-08-14, not guessed)

Checked directly at link.springer.com/journal/894/submission-guidelines.
Requirements that change what still needs to be done, in order of impact:

1. **Structured abstract, two mandatory subheadings.** JMM requires the
   abstract be split into **Context** (why the work was done, relevance,
   summary of results) and **Methods** (computational techniques and
   software used — for this manuscript: Meeko 0.7.1, AutoDock Vina 1.2.5,
   RDKit, NumPy Kabsch cross-check). 150-250 words total, no references, no
   undefined abbreviations. **The current draft abstract above is a single
   flowing paragraph and must be restructured into these two labeled parts
   before submission** — not just trimmed for length.
2. **LLM use must be disclosed in the Methods section.** JMM: "Use of an
   LLM should be properly documented in the Methods section... LLMs do not
   currently satisfy our authorship criteria." This manuscript's analysis
   pipeline, scripts, and prose were substantially produced with Claude
   (Anthropic). This needs an explicit, honest disclosure sentence in
   Methods — drafting it is now a required task, not optional polish. It
   does not make the user ineligible for authorship; it is a disclosure
   requirement, not a prohibition.
3. **A Data Availability Statement is mandatory, not optional**, for every
   original research article, with a link to a publicly archived dataset.
   This directly upgrades the standing "repository publication decision"
   from a nice-to-have to a hard submission blocker: **the repository (or
   at minimum the versioned `data/`/`reports/` manifests) needs a real,
   public, citable location before this can be submitted** — e.g. a GitHub
   release plus a Zenodo DOI (Zenodo is free, integrates with GitHub, and
   is a standard, discipline-neutral choice for this kind of computational
   audit). This is a new-and-separate authorization the user has not yet
   given (the project's standing constraint is "no publish/release/Zenodo
   without new explicit instruction") — do not act on this without asking.
4. **Numbered citations, square brackets, e.g. `[3]` or `[1-3, 7]`**,
   numbered reference list in citation order (not alphabetical), DOIs as
   full links where available. Standard journal-abbreviation style (ISSN
   LTWA) or full journal title if unsure.
5. **Structure confirmed**: Introduction (purpose + short literature
   review) → Methods (enough detail to repeat the work) → Results (concise,
   avoid very large tables) → Discussion (interpretation vs. other authors'
   work) → Summary (concise, does not repeat the Discussion) → **Statements
   and Declarations** (Funding, Competing Interests, Author Contributions,
   Data Availability — this exact heading, placed after References; missing
   it causes the submission to be "returned as incomplete").
6. **Format**: Word .docx (10-pt Times Roman, ≤3 heading levels) or LaTeX
   (Springer Nature template recommended). Figures: vector (EPS) or TIFF,
   minimum 300 dpi for halftones/600 dpi for combination art, sized to
   84 mm or 174 mm column width. Raw structure/data files (.pdb, .csv,
   .xlsx) are explicitly supported as Supplementary Information — this
   repository's manifests can likely be submitted close to as-is for that
   part, once a citable public location exists (see point 3).
7. **4-6 keywords required.**

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
| Fig. 7 (new) | 2D ligand-receptor interaction diagrams (LigPlot+/PLIP-style schematic), top-scoring pose, all 7 completed cases | `reports/generated/figures/interaction-diagrams/interaction-diagram-<case>-<PDB>.svg`, generated by `scripts/render_interaction_diagrams.py` | **done** — real, coordinate-derived contacts (same data as Table 4), schematic layout per LigPlot+/PLIP convention, green dashed = H-bond candidate, red = other contact, both labelled with real distances |
| Table 1 | Inclusion criteria and structural classification rule | text-only, write directly in manuscript | — |
| Table 2 | All 23 preparation attempts (case, PDB, batch, outcome, failure class) | already exists as the table in `reports/STRICT-PREPARATION-SUMMARY-v0.1.md` | reuse directly |
| Table 3 | 7 completed docking cases (case, PDB, ligand, top-score affinity, top-score RMSD, best RMSD, verified?) | already exists as the table in `reports/AUDIT-SYNTHESIS-v0.1.md` | reuse directly |
| Table 4 (new) | Receptor-ligand interface contacts and H-bond candidates for the top-scoring pose, all 7 completed cases | already exists as the table in `reports/INTERFACE-CONTACTS-v0.1.md`, data in `data/interface_contacts_top_pose.csv` / `data/hydrogen_bonds_top_pose.csv` | **done** — real, coordinate-derived (4.5 Å contact / 3.5 Å N-O H-bond heuristic), includes two chemically notable findings (1IEP's closest contact is the Abl kinase T315 gatekeeper residue; 3PTB's top pose sits in the correct S1 pocket residues despite failing the RMSD threshold) |
| Table 5 (new) | Independent Kabsch-Horn cross-check of every reported RMSD (6 cases) | already exists as the table in `reports/KABSCH-RMSD-CROSSCHECK-v0.1.md`, data in `data/kabsch_rmsd_crosscheck.csv` | **done** — a from-scratch NumPy implementation, independent of RDKit's `GetBestRMS`, agrees with every reported RMSD to machine precision (≤0.001 Å); strong reproducibility content for the Methods section |
| Table 6 (new) | Buried interface surface area (ΔSASA) for the top-scoring pose, all 7 completed cases | already exists as the table in `reports/SASA-BURIAL-v0.1.md`, data in `data/sasa_burial_top_pose.csv` | **done** — real, coordinate-derived Shrake-Rupley SASA; buried area tracks ligand size as expected (355.6-1137.3 Å²), and corroborates the 3PTB "right pocket, wrong orientation" characterization from Table 4 |
| Table 7 (new) | RMSD classified against standard success thresholds (≤1.0/≤2.0/≤3.0 Å), top-score and best pose, 6 verified cases | already exists as the table in `reports/INTERACTION-DIAGRAMS-AND-SUCCESS-THRESHOLDS-v0.1.md`, data in `data/success_thresholds.csv` | **done** — re-derived from the already-committed RMSD CSVs; 5/6 verified cases (83%) succeed at the conventional ≤2.0 Å threshold used in benchmarks such as CASF; 3PTB fails at every threshold, 1IEP excluded as not verified |

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
3. ~~No independent reproduction has been run.~~ **Done.**
   `reports/REPRODUCIBILITY-VERIFICATION-v0.1.md` independently re-ran
   classification, extraction, strict preparation (all 23 attempts), RMSD
   calculation (all 6 verified cases + the 1 unverified case), a live
   RCSB re-download and checksum match for 3 representative structures, and
   a full Vina re-run (bit-identical output PDBQT) — zero substantive
   differences anywhere. The abstract's reproducibility claim is now
   verified, not merely asserted. Not tested: reproduction on a different
   OS/Meeko/Vina build (cross-environment reproducibility remains open).
4. ~~Author list, affiliations, ORCID~~ **Done** — confirmed 2026-08-14, see
   "Authors" section above (same three authors and order as the companion
   102-target manuscript). ~~Funding statement and competing-interests
   statement.~~ **Done** — confirmed 2026-08-14 (no funding, no competing
   interests), see "Statements and Declarations" section above. Author
   Contributions still needs the per-author breakdown from the authors
   themselves before submission.
5. ~~Repository publication decision.~~ **Done** — created public at
   https://github.com/sircalch/docking-reference-audit (2026-08-14),
   containing `protocol/`, `data/`, `scripts/`, `reports/`, `manuscript/`;
   `raw/` and `derived/` intentionally excluded (gitignored, fully
   regenerable — confirmed by
   `reports/REPRODUCIBILITY-VERIFICATION-v0.1.md`). **Still open: Zenodo
   integration and a versioned GitHub Release for the permanent DOI** the
   Data Availability Statement should ultimately cite — this needs the
   user's own GitHub-authenticated login to Zenodo, and a deliberate
   decision on when to cut the first release (once the manuscript content
   is stable, not necessarily now).
6. ~~JMM's current author guidelines have not been checked.~~ **Done** — see
   "Confirmed journal requirements" above (structured abstract, LLM
   disclosure, Data Availability Statement, reference style, figure specs,
   Statements and Declarations section).
7. ~~Draft the LLM-use disclosure sentence for Methods.~~ **Done** —
   confirmed 2026-08-14, see "AI-use disclosure" section above.
8. **Restructure the draft abstract into Context/Methods subheadings**
   (currently one flowing paragraph) and trim to 150-250 words.
9. **Optional but valuable: 2-3 more contextual cases** processed under the
   same chemically-justified retained-component discipline, to grow both
   the preparation-attempt census and, if any succeed, the docking-outcome
   table beyond n=7.
