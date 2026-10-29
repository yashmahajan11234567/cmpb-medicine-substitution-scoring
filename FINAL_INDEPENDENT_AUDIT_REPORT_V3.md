# Final Independent Audit Report — CMPB Manuscript V3

**Audit date:** 2026-10-28
**Files examined:**
- `main_cmpb_v3.tex` (source)
- `main_cmpb_v3.pdf` (compiled PDF)
- `FRONTMATTER_FIX_REPORT.md` (fix documentation)
- Authoritative source: `manuscript/main.tex` (project root)
- `FINAL_CORRECTION_REPORT.md` (project root)

---

## 1. Page-by-Page Visual Inspection (All 11 Pages)

All 11 pages of `main_cmpb_v3.pdf` were rendered at 100 DPI via `pdftoppm` and inspected visually.

| Page | Content | Status | Observations |
|------|---------|--------|--------------|
| 1 | Title, 6 authors with ORCID footnotes, affiliation, corresponding email, structured abstract (Background and Objective, Methods, Results, Conclusions), keywords, Section 1 start | PASS | Complete front matter on page 1. Title spans full width. All 6 authors listed once, in correct order. ORCID footnotes attached to each author. Corresponding email: yash.mahajan23@pccoepune.org. Affiliation: Pimpri Chinchwad College of Engineering, Pune. Abstract sections all present: Background and Objective, Methods (with DS equation), Results (26/32, 32/32, 1.2152, 3/5, 4/5, 196 assertions), Conclusions. Keywords present. Introduction starts cleanly below abstract. No overlapping text between columns. No text clipping at margins. |
| 2 | Section 1 (Introduction continued), Section 2 (Related work), Section 3 (Method start) | PASS | Clean two-column layout. No overlapping text. No text overflow beyond margins. Citations render as [3], [4], etc. |
| 3 | Section 3.1 (Product encoding), Equations (1)-(4), Figure 1 (DS decomposition), Section 3.2 | PASS | Equation (1) renders as `DS = 100 − (penaltyNDXUP + penaltySTs)` with parentheses around both penalty terms. Equations (2)-(4) render correctly. Product encoding equation `ATC | BDF | AME | ISI | RCA | TRN | NDXUP` visible. Figure 1 renders without clipping. Caption legible. |
| 4 | Section 3.3-3.4 (V3), Figure 2 (workflow), Section 4 (Implementation) | PASS | Figure 2 renders without clipping. Caption legible. Section 4 bulleted list readable. No layout issues. |
| 5 | Section 5 (Experimental design): Dataset, Evaluation criteria, Reproducibility | PASS | Clean two-column text. No overlaps. Citations resolve correctly. |
| 6 | Table 1 (Table 8 DS scores), Table 2 (Table 7 NDXUP sums), Section 6.6-6.7 | PASS | Full-width tables within margins. Table 1: V0-strict-baseline 26/32, V1 32/32. Table 2: Unit-aware 3/5, Literal 4/5, Any convention 5/5. All values legible. Section 6.6 Variants, 6.7 Performance scaling visible. |
| 7 | Table 3 (Table 7-dim dimensional analysis), Section 6.8 Correctness tests | PASS | Full-width dimensional analysis table. All 5 rows (A-E) legible with literal/unit-normalized calculations, published values, "Dim. valid?" column. Section 6.8 visible. |
| 8 | Section 7 (Discussion), Section 8 (Limitations), Section 9 (Conclusion) | PASS | Clean two-column text. All subsections readable. No overlapping text. Section 9 Conclusion visible. |
| 9 | Section 10 (Declarations): Ethics, Funding, Competing interests, CRediT, AI disclosure, Data/code availability | PASS | All declarations readable. Data/code availability states repository not yet available. No public repository claimed. |
| 10 | References [1]-[8] | PASS | References readable, complete, consistently formatted. No clipping. No missing references (?). |
| 11 | References [9]-[25], last page | PASS | References [9]-[25] complete and readable. Page ends cleanly with page number 11 at bottom. No truncated content. |

**Visual inspection result: ALL 11 PAGES PASS.** No overlapping text, no clipping, no missing glyphs, no orphaned captions, no empty pages, no awkward float-only pages, no excessive whitespace.

---

## 2. Scientific Fidelity Verification

Compared `main_cmpb_v3.tex` against `FINAL_CORRECTION_REPORT.md` and authoritative source `manuscript/main.tex`.

| Protected Element | Source Location | Verified? | Details |
|-------------------|----------------|-----------|---------|
| Equation (1): `DS = 100 − (penalty_NDXUP + penalty_STs)` | `main_cmpb_v3.tex` line 104; PDF page 3 | YES | Both penalty terms subtracted inside parentheses. Confirmed visually on page 3. |
| V0: 26/32 Table 8 DS matches | Source line 248; PDF page 6 Table 1 | YES | "V0-strict-baseline & 26 & 0.2290 & 1.2152" |
| V1: 32/32 Table 8 DS matches | Source line 249; PDF page 6 Table 1 | YES | "V1-publication-compatible & 32 & 0.0066 & 0.0293" |
| TRN reconciliation proposed/inferred | Source lines 147, 256; Discussion 365; Limitations 387 | YES | Explicitly labelled "proposed reconciliation" and "inferred from published scores"; "not been independently confirmed against an authoritative source" |
| Table 7: unit-normalized 3/5, literal 4/5 | Source lines 279-281; PDF page 6 Table 2 | YES | "Unit-aware & 3", "Literal & 4", "Any convention & 5" |
| Each row matches under ≥1 convention | Source line 282; PDF page 6 Table 2 | YES | "Every row reproducible by at least one" |
| No match claimed dimensionally valid | Source line 286; PDF page 7 Table 3 | YES | Table 3 labels Row B "No (tab count)", Row C "No (g not converted)", Row E "No (g not converted)" |
| V3: preliminary and unvalidated | Source lines 173-175, 314, 323 | YES | "preliminary adaptation", "unvalidated against published ground truth", "not evaluated against published ground truth" |
| No clinical interchangeability claim | Source lines 175, 377, 395 | YES | "No clinical interchangeability or therapeutic-equivalence claim is made" repeated |
| No public repository/DOI claimed | Source line 415 | YES | "The repository and persistent identifier are not yet available" |
| 196 assertions | Source lines 196, 357, 365, 393 | YES | "All 196 assertions pass" appears in abstract, methods, discussion, conclusion |
| All figures, tables, citations, references | Source lines 132-138, 198-204, 240-350, 417-420 | YES | All present and rendering correctly |

**Scientific fidelity result: VERIFIED.** All scientific claims match the authoritative source and correction report. No discrepancies found.

---

## 3. Document Structure and Reference Checks

| Check | Status | Details |
|-------|--------|---------|
| Section numbering | PASS | Sections 1-10 numbered correctly |
| Equation references | PASS | eq:ds, eq:ndxup, eq:st, eq:nrd, eq:fc all defined and referenced |
| Figure references | PASS | fig:ds-formula, fig:workflow defined and referenced |
| Table references | PASS | tab:table8, tab:table7, tab:table7-dim, tab:variants, tab:scaling all defined and referenced |
| Undefined citations | PASS | No `??` in rendered PDF; all `\citep` keys resolve |
| Duplicate paragraphs/captions | PASS | None found |
| Duplicate bibliography entries | PASS | None found |
| Missing figures/external assets | PASS | figures/ds_formula.tex and figures/workflow.tex present |
| Author order/names/affiliations | PASS | 6 authors, correct order, all affiliations Pimpri Chinchwad College of Engineering |
| ORCIDs preserved | PASS | All 6 ORCIDs as per-author footnotes |
| Corresponding author email | PASS | yash.mahajan23@pccoepune.org |
| No hidden placeholders as real info | PASS | Postal address and telephone not invented; CRediT statement flagged "to be confirmed by all authors" |
| No false public availability claim | PASS | "public repository has not yet been released" — truthful statement |

**Structure check result: VERIFIED.** No structural issues found.

---

## 4. Official CMPB Requirements Check

**Source:** Elsevier Guide for Authors, Computer Methods and Programs in Biomedicine (ISSN 0169-2607)
**URL:** https://www.sciencedirect.com/journal/computer-methods-and-programs-in-biomedicine/publish/guide-for-authors
**Access date:** 2026-10-28

| Requirement | Category | Status | Evidence |
|-------------|----------|--------|----------|
| Structured abstract headings: Background and Objective, Methods, Results, Conclusions | Mandatory | PASS | All 4 headings present (plural "Conclusions") |
| Abstract word limit ≤ 350 words | Mandatory | PASS | ~335 words |
| No citations in abstract | Mandatory | PASS | No `\citep` in abstract |
| Body word limit ≤ 3,500 words | Recommended | PASS | ~1,807 words |
| References ≤ 50 | Mandatory | PASS | 25 cited, 34 in .bib |
| Numbered sections | Mandatory | PASS | 9 numbered sections |
| Ethics statement | Mandatory | PASS | "Not applicable" |
| Funding statement | Mandatory | PASS | "No specific grant" |
| Competing interests | Mandatory | PASS | "No known competing interests" |
| Author contributions (CRediT) | Mandatory | PASS | Present, flagged for author confirmation |
| Generative AI disclosure | Mandatory | PASS | ChatGPT disclosed |
| Data and code availability | Mandatory | PASS | Truthful statement (project directory, not yet public) |
| Keywords | Mandatory | PASS | 7 keywords |
| Single corresponding author | Mandatory | PASS | Yash Mahajan |
| Editable .tex source | Mandatory | PASS | main_cmpb_v3.tex |
| Corresponding author full contact (postal, telephone) | Mandatory | NOT VERIFIED | Not supplied by authors; placeholders retained |
| Article highlights | Optional | PASS | 5 bullets, all ≤85 chars |
| Graphical abstract | Optional | NOT PRESENT | Not created (optional) |

**Requirements not yet verified (author input needed):**
- Postal address and telephone number for corresponding author — CMPB Guide requires full contact details; email alone may not suffice. Placeholders retained. No address/telephone invented.
- CRediT author confirmation from all six authors.

---

## 5. Tests and Builds Actually Executed

| Test/Build | Command | Result |
|------------|---------|--------|
| `tectonic main_cmpb_v3.tex` pass 1 | `/opt/homebrew/bin/tectonic main_cmpb_v3.tex` | Exit 0 |
| `tectonic main_cmpb_v3.tex` pass 2 | `/opt/homebrew/bin/tectonic main_cmpb_v3.tex` | Exit 0 |
| LaTeX errors | Build output | 0 |
| Undefined references | Build output | 0 |
| Overfull boxes >10pt | Build output | 0 |
| PDF page count | `pdfinfo main_cmpb_v3.pdf` | 11 pages |
| PDF page size | `pdfinfo main_cmpb_v3.pdf` | A4 (595.28 × 841.89 pts) |

**Note:** The test suite (`python test_caviglioli.py`) was NOT rerun during this audit phase per the audit-only constraint. The 196/196 assertion count is taken from the authoritative source text in the manuscript itself, not from a fresh execution.

---

## 6. Confirmed Defects, Unresolved Issues, Author Decisions

### Defects Found (all corrected in V3):
1. **Page 1 column collision (V2)** — Front matter was rendering in two columns, causing abstract split. Fixed in V3 by using `elsarticle`'s native `frontmatter` environment with `twocolumn` document class (no manual `\onecolumn`/`\twocolumn`).
2. **Table overflows (V2)** — 5 tables overflowed single column. Fixed in V2 by converting to full-width `table*` environments; preserved in V3.
3. **Equation overflows (V2)** — Fixed in V2 with `split` environments; preserved in V3.
4. **ORCIDs not mapped to individual authors (V2)** — Fixed in V2 by adding `\footnote{ORCID: ...}` to each `\author`; preserved in V3.
5. **Invalid inline math `$_\\text{NDXUP}$` (V3 initial)** — Fixed by correcting to `$\\text{NDXUP}$`.

### Unresolved Issues (author decisions required):
| Issue | Details |
|-------|---------|
| Corresponding author postal address | Required by CMPB Guide; not supplied; placeholder retained |
| Corresponding author telephone | Required by CMPB Guide; not supplied; placeholder retained |
| CRediT author contributions | "to be confirmed by all authors" — needs confirmation |
| Exclusive submission statement | Needs author confirmation |
| Cover letter approval | Needs author review |

---

## 7. Final Status

**Status: `PASS — READY FOR AUTHOR REVIEW`**

### Summary of Findings

The rebuilt manuscript `main_cmpb_v3.tex` compiles cleanly with `tectonic` (exit 0, 0 LaTeX errors, 0 undefined references, 0 overfull boxes >10pt). All 11 pages of `main_cmpb_v3.pdf` were visually inspected and render correctly:

- **Page 1 front matter** (the issue from V2): Title, all 6 authors with ORCID footnotes, corresponding-author email, affiliation, structured abstract with all 4 headings (Background and Objective, Methods, Results, Conclusions), keywords — all on page 1 with no column collision. Introduction starts cleanly below.
- **All equations render correctly** with proper mathematical meaning (Equation (1): `DS = 100 − (penaltyNDXUP + penaltySTs)` with both penalties subtracted).
- **All figures render without clipping** (Figures 1 and 2).
- **All tables render legibly** as full-width tables within page margins (Tables 1/8, 2/7, 3/7-dim, 4/variants, 5/scaling).
- **References complete** through [25], ending cleanly on page 11.
- **All scientific claims verified** against the authoritative source and correction report.
- No clinical validation, therapeutic equivalence, or public repository claims made.
- No DOI minted, no public repository claimed.

The manuscript is **ready for author review** — all technical formatting, compilation, visual rendering, and scientific content checks have passed. It is **not submission-ready** until the author decisions listed in Section 6 are resolved.

**Not submitted. Not uploaded. No DOI minted. No external action taken.**

### Key File Paths
- Rebuilt source: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_v3.tex`
- Rebuilt PDF: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_v3.pdf` (11 pages, A4)
- Front-matter fix report: `FRONTMATTER_FIX_REPORT.md`
- This report: `FINAL_INDEPENDENT_AUDIT_REPORT_V3.md`

**Authoritative source files: UNCHANGED**
**Existing backups: UNTOUCHED**
**Previous versions preserved: main_cmpb.tex, main_cmpb_v2.tex, main_cmpb_v2.pdf**
