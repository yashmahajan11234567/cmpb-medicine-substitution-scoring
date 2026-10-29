# Layout Failure Diagnosis — CMPB Manuscript V4

**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Report date:** 2026-10-28

---

## 1. Root Cause of V3 Failure

**Diagnosed root cause:** The `elsarticle` document class with `twocolumn` option typesets the `frontmatter` environment (title, authors, abstract, keywords) in **two columns**. This was not apparent during initial testing because V3 used `\documentclass[twocolumn,a4paper]{elsarticle}` without any column-switching commands around `\begin{frontmatter}`.

**Consequence on V3 page 1:** The title block, author list, affiliations, ORCID footnotes, and abstract were all typeset across two columns. Page 1 showed:
- Left column: title, first 3-4 authors, partial abstract text (Background and Objective, Methods, partial Results)
- Right column: remaining authors, partial abstract text (Results continuation, Conclusions), Keywords

This caused text interleaving when extracted via `pdftotext`, overlapping visual elements, and an unreadable first page.

**Why removing `\onecolumn`/`\twocolumn` was insufficient:** Simply omitting explicit column switches does not make `elsarticle` render frontmatter in single column. The `elsarticle` class with `twocolumn` option typesets frontmatter content in two columns by default, regardless of whether `\onecolumn`/`\twocolumn` are explicitly used.

**Why V2 appeared to work:** `main_cmpb.tex` (V2 source) did NOT contain `\onecolumn`/`\twocolumn` around frontmatter either, yet appeared to produce single-column frontmatter in earlier visual inspection. This was misleading — V2 page 1 actually had the same two-column frontmatter problem, but the earlier visual inspection did not catch it because the title/authors happened to fit in the left column and the abstract text flowed into the right column without obviously overlapping at the top of the page.

---

## 2. Root Cause Analysis Summary

| Issue | V2 | V3 | V4 (fixed) |
|-------|----|----|------------|
| `\documentclass` class option | `twocolumn,a4paper` | `twocolumn,a4paper` | `twocolumn,a4paper` |
| `\onecolumn` before frontmatter | Absent | Absent | Present |
| `\twocolumn` after frontmatter | Absent | Absent | Present |
| Page 1 frontmatter | Two columns (broken) | Two columns (broken) | Single column (correct) |
| Abstract split across pages | Yes (1-2) | Yes (1-2) | Yes (1-2) — expected for long abstract |

---

## 3. Class-Supported Solution Selected

**Solution:** Use `elsarticle` with `twocolumn,a4paper` document class options, and explicitly wrap the frontmatter with `\onecolumn` before `\begin{frontmatter}` and `\twocolumn` after `\end{frontmatter}`.

**Rationale:** The `elsarticle` class documentation does not guarantee single-column frontmatter when `twocolumn` is specified. The `frontmatter` environment does not automatically switch column mode. Explicit `\onecolumn`/`\twocolumn` switching is the standard, supported LaTeX approach for mixed single-column front matter and two-column body content.

**Trade-offs:**
- The abstract spans pages 1-2 because it is long (4 structured paragraphs). This is normal and acceptable for journal submissions — many journals accept abstracts that span pages.
- The body (Introduction onwards) renders in clean two-column format starting on page 3.
- All tables render as full-width `table*` environments.
- All equations render in single-column math mode within the two-column body.

---

## 4. Source Changes Made

**File:** `main_cmpb_v4.tex` (new file; `main_cmpb_v3.tex` preserved unchanged)

| Location | Before (V3) | After (V4) |
|----------|-------------|------------|
| Line 18-19 | `\begin{document}\n\n\\begin{frontmatter}` | `\begin{document}\n\n\\onecolumn\n\n\\begin{frontmatter}` |
| Line 54-55 | `\end{frontmatter}\n\n\\section{Introduction}` | `\end{frontmatter}\n\n\\twocolumn\n\n\\section{Introduction}` |

All other content (equations, tables, figures, scientific text, references, author details) is identical to V3.

---

## 5. Layout Trade-Offs

| Trade-off | Decision |
|-----------|----------|
| Single-column frontmatter vs two-column frontmatter | Single-column frontmatter chosen because two-column frontmatter causes unreadable overlap |
| Abstract spanning pages 1-2 vs fitting on page 1 | Abstract spans pages 1-2 because it is long (4 structured paragraphs). This is acceptable for initial submission |
| Double-column body vs single-column body | Double-column body retained because CMPB Guide permits single-column initial submission, and two-column is the journal's published format |
| Full-width tables vs column-width tables | Full-width `table*` tables used for all tables because single-column width is too narrow for tables with 4-6 columns |

---

## 6. Author Decisions Still Required

| Blocker | Details |
|---------|---------|
| Corresponding author postal address | Required by CMPB Guide; not supplied by authors |
| Corresponding author telephone | Required by CMPB Guide; not supplied by authors |
| CRediT author contributions confirmation | All six authors must confirm |
| Exclusive submission statement | Needs author confirmation |
| Cover letter approval | Needs author review |

---

**Status: `PASS — LAYOUT VERIFIED`** — V4 page 1 has complete front matter in single column, all subsequent pages render cleanly in two-column body format. Not submitted, not uploaded, no DOI minted. Authoritative source files and existing backups unchanged. V2 and V3 files preserved.
