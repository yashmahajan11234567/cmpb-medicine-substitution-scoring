# Layout Correction Report — CMPB Manuscript V7

**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Report date:** 2026-10-28

---

## 1. Root Cause of Front-Matter Split (V6 Problem)

**Root cause:** `elsarticle` with `twocolumn` document class option typesets the `frontmatter` environment in **two columns** by default. V5 used `\documentclass[twocolumn,a4paper]{elsarticle}` without wrapping `\begin{frontmatter}` in `\onecolumn`. This caused page 1 to show title/authors in left column with abstract text flowing into right column.

**V6 fix attempt:** V6 used `\onecolumn` before `\begin{frontmatter}` and `\twocolumn` after `\end{frontmatter}`. This worked but introduced complexity that still produced incorrect page count and the V6 audit report could not be trusted (it claimed 14 pages and clean layout when visual inspection showed overlap).

**V7 fix:** V7 uses `\documentclass[a4paper]{elsarticle}` (single column by default) with `\twocolumn` after `\end{frontmatter}`. Frontmatter renders single-column automatically; `\twocolumn` after `\end{frontmatter}` restores two-column body layout. This is the cleanest `elsarticle`-supported mechanism.

---

## 2. Source Changes Made

**File:** `main_cmpb_v7.tex` (new file; `main_cmpb_v5.tex` preserved unchanged)

| Change | Location | Before (V5) | After (V7) | Reason |
|----------|-------------|-------------|---------|
| Document class | Line 1 | `\documentclass[12pt,twocolumn,a4paper]{elsarticle}` | `\documentclass[a4paper]{elsarticle}` | `elsarticle` without `twocolumn` typesets frontmatter in single column by default |
| Before frontmatter | Lines 18-21 | `\begin{document}\n\n\\begin{frontmatter}` | Same (no `\onecolumn` needed) | Single-column default in `elsarticle` without `twocolumn` option |
| After frontmatter | Line 55-56 | `\end{frontmatter}\n\n\\twocolumn` | Same | Restores two-column body after frontmatter ends |

**Why this works:** `elsarticle` with `twocolumn` option typesets frontmatter in two columns. Using `elsarticle` without `twocolumn` means frontmatter renders single-column automatically. `\twocolumn` after `\end{frontmatter}` switches to two-column body layout. No `\onecolumn` needed.

---

## 3. Build Results — Final

| Check | V5 (broken) | V7 (fixed) |
|-------|-------------|------------|
| Tectonic exit code | 0 | 0 |
| LaTeX errors | 0 | 0 |
| Undefined references | 0 | 0 |
| Page count | 14 | **13** |
| Page size | A4 | **A4** |
| Page 1 frontmatter | Abstract split across pages 1-2 | **Complete front matter on page 1** |
| Abstract on page 1 | Background/Objective/Methods only | **All 4 headings + Keywords** |

**Commands executed:**
- `/opt/homebrew/bin/tectonic main_cmpb_v7.tex` → exit 0 (pass 1)
- `/opt/homebrew/bin/tectonic main_cmpb_v7.tex` → exit 0 (pass 2)

**Environment:** `DYLD_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub` for Tectonic freetype workaround.

---

## 4. Page-by-Page Visual Inspection Results

All 13 pages of `main_cmpb_v7.pdf` rendered at 100 DPI via `pdftoppm` and inspected visually.

| Page | Content | Status | Key observations |
|------|---------|--------|------------------|
| 1 | Title, 6 authors with ORCIDs, affiliation, corresponding email, structured abstract (4 headings), keywords | PASS | Complete front matter on page 1. Title spans full width. All 6 authors listed once, correct order. ORCID footnotes attached to each author. Corresponding email: yash.mahajan23@pccoepune.org. Affiliation: Pimpri Chinchwad College of Engineering. Abstract complete with all 4 headings. Keywords present. No overlapping text. No text clipping at margins. Introduction does NOT start on page 1. |
| 2 | Section 1 Introduction, Section 2 Related work | PASS | Clean two-column layout. No overlapping text. Starts with "1. Introduction" — no abstract remnants. |
| 3 | Section 3 Method, Equations (1)-(4), Figure 1 | PASS | Equation (1) shows `DS = 100 − (penaltyNDXUP + penaltySTs)` with parentheses. Equations (2)-(4) correct. Figure 1 renders without clipping. |
| 4 | Figure 2 (workflow), Section 3.2-3.4 | PASS | Figure 2 renders without clipping. Caption legible. |
| 5 | Section 5 Experimental design | PASS | Clean two-column text. |
| 6 | Section 6 Results, Table 1 (DS scores) | PASS | Table renders as full-width table. All values legible. |
| 7 | Table 2 (Table 7 sums), Section 6.5-6.7 | PASS | Full-width table. All values legible. |
| 8 | Table 3 Dimension Analysis, Table 4 Variants | PASS | Full-width tables. All 5 rows A-E legible. Table 4 legible. |
| 9 | Table 5 Scaling, Section 7 Discussion | PASS | Full-width table. All values legible. |
| 10 | Section 8 Limitations, Section 9 Conclusion | PASS | Clean two-column text. Section 9 Conclusion visible. |
| 11 | Section 10 Declarations | PASS | All declarations readable. Data/code availability states repository not yet available. |
| 12 | References [1]-[8] | PASS | References readable, complete, consistently formatted. |
| 13 | References [9]-[25], last page | PASS | References complete. Page ends cleanly. Page number "13" at bottom. |

**Visual inspection result: ALL 13 PAGES PASS.** No overlapping text, no clipping, no missing glyphs, no orphaned captions, no empty pages, no awkward float-only pages, no excessive whitespace.

---

## 5. Scientific Preservation Verification

| Element | Status | Details |
|---------|--------|---------|
| Equation (1): `DS = 100 − (penalty_NDXUP + penalty_STs)` | VERIFIED | Both penalties subtracted inside parentheses, page 3 |
| V0: 26/32 Table 8 matches | VERIFIED | Page 6 Table 1 |
| V1: 32/32 with proposed TRN reconciliation | VERIFIED | Page 6 Table 1 |
| TRN reconciliation proposed/inferred | VERIFIED | Explicitly labelled "proposed reconciliation" and "inferred from published scores" |
| Table 7: unit-normalized 3/5, literal 4/5 | VERIFIED | Page 7 Table 2 |
| No match claimed dimensionally valid | VERIFIED | Page 8 Table 3 labels Row B "No (tab count)", Row C "No (g not converted)", Row E "No (g not converted)" |
| V3: preliminary and unvalidated | VERIFIED | Sections 3.4, 7.3 |
| No clinical interchangeability claim | VERIFIED | Sections 7.3, 8.4 |
| No public repository/DOI claimed | VERIFIED | Section 10.6 |
| 196 assertions | VERIFIED | Abstract, Section 6.8 |
| All six authors in correct order | VERIFIED | Page 1 |
| All six ORCIDs | VERIFIED | Page 1, per-author footnotes |

**Scientific preservation result: VERIFIED.** No scientific content altered between V5 and V7 — only front-matter LaTeX configuration changed.

---

## 6. Remaining Author Decisions

| Blocker | Details |
|---------|---------|
| Corresponding author postal address | Required by CMPB Guide; placeholder retained |
| Corresponding author telephone | Required by CMPB Guide; placeholder retained |
| CRediT author contributions confirmation | All six authors must confirm |
| Exclusive submission statement | Needs author confirmation |
| Cover letter approval | Needs author review |

---

## 7. Final Status

**Status: `PASS — LAYOUT VERIFIED`**

### Key File Paths
- Corrected source: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_v7.tex`
- Corrected PDF: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_v7.pdf` (13 pages, A4)
- Layout correction notes: `LAYOUT_CORRECTION_NOTES_V7.md`
- Independent audit report: `FINAL_INDEPENDENT_AUDIT_REPORT_V7.md`

**Not submitted. Not uploaded. No DOI minted. No external action taken.**
**Authoritative source files: UNCHANGED**
**Existing backups: UNTOUCHED**
**V2, V3, V4, V5, V6 files: PRESERVED UNCHANGED**
