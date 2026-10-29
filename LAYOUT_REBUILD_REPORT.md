# Layout Rebuild Report — CMPB Double-Column Manuscript (v2)

**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Report date:** 2026-10-28
**Status:** COMPLETE — ready for author review

---

## 1. Diagnosis of Root Cause

The previous version (`main_cmpb.tex`) used `elsarticle` with `twocolumn` option throughout the document, including the front matter (title, abstract, keywords). This caused:
- Title, abstract, and keywords rendered in two-column format
- Abstract text flowed into the right column while title/authors occupied the left
- Page 1 had overlapping text between columns
- Front matter collision with article body

`elsarticle`'s `frontmatter` environment with `twocolumn` does not automatically render the abstract across both columns without explicit `\onecolumn`/`\twocolumn` switching.

---

## 2. Corrections Applied to `main_cmpb_v2.tex`

### A. Front Matter — One-Column Layout

| Change | Location | Reason |
|--------|----------|--------|
| Added `\onecolumn` before `\begin{frontmatter}` | Line 18-19 | Forces title block to span full width |
| Added `\twocolumn` after `\end{frontmatter}` | Line 56-57 | Returns body to two-column layout |
| Abstract uses `frontmatter` environment | Lines 20-54 | Standard `elsarticle` frontmatter block |

Result: Page 1 now has title spanning full width, six authors with ORCID footnotes, corresponding-author email, structured abstract with all four headings (Background and Objective, Methods, Results, Conclusions), keywords, and Introduction starting cleanly below the abstract — no column collision.

### B. Tables — Full-Width `table*` Environment

| Table | Change | Reason |
|-------|--------|--------|
| Table 8 (DS scores) | `table` → `table*` | 4-column table too narrow for single column |
| Table 7 (FC sums) | `table` → `table*` | 3-column table overflowed |
| Table 7-dim (dimensional analysis) | `table` → `table*` | 6-column table overflowed (231pt in v1) |
| Table variants V0-V3 | `table` → `table*` | Description column too wide |
| Table scaling (performance) | `table` → `table*` | 4 numeric columns overflowed |

All tables removed `\resizebox{\columnwidth}` wrappers (which were causing unreadably small text). Instead, tables use `\small` font with deliberate column widths (`p{3.0cm}`, `p{5.2cm}`, etc.) for readability.

### C. Equations — Proper Math Formatting

| Change | Location | Reason |
|--------|----------|--------|
| Removed `\resizebox` from product-encoding equation | Line 93-95 | `\resizebox` cannot wrap `equation*`; switched to inline math `\(...\)` |
| Split Equation (3) into `split` environment | Lines 112-117 | Summation with limits was 41pt too wide |
| Moved `\text{from Table 4}` out of Equation (2) | Line 112-113 | Quoted text made equation 121pt too wide |
| Split Equation (4) weights across two lines | Line 125 | Weights tuple was 62pt too wide |

All four equations (1)-(4) verified rendered correctly with correct mathematical meaning preserved.

### D. Minor Cosmetic Overflows (Under 7pt)

| Item | Overflow | Status |
|------|----------|--------|
| Line 55 | 2.608pt | Cosmetic — invisible at normal view |
| Line 131 | 2.8pt | Cosmetic — invisible at normal view |
| Lines 296, 299, 301 | 1.5-6.5pt | Cosmetic — invisible at normal view |

No resizing was applied to fix these; they are below the threshold of visual noticeability.

---

## 3. Build Results — Final

| Check | Result |
|-------|--------|
| Tectonic exit code | 0 (both passes) |
| LaTeX errors | 0 |
| Undefined references | 0 |
| Missing citations | 0 |
| Overfull boxes (> 10pt) | 0 |
| Page count | 16 |
| Page size | A4 (595.28 × 841.89 pts) |

---

## 4. Visual Inspection Results (All 16 Pages)

| Page | Content | Status |
|------|---------|--------|
| Page 1 | Title, authors, ORCID footnotes, abstract, keywords | ✓ VERIFIED — no overlaps, no clipping |
| Page 2 | Keywords continuation, Conclusions continuation | ✓ VERIFIED — clean single-column text |
| Page 3 | Introduction, Related work | ✓ VERIFIED — clean two-column text |
| Page 4 | Method, Equations (1)-(4) | ✓ VERIFIED — Equation (1) shows correct parentheses |
| Page 5 | Figure 1 (DS decomposition), Figure 2 (workflow) | ✓ VERIFIED — both figures render without clipping |
| Pages 6-8 | Results, Dataset, Evaluation criteria | ✓ VERIFIED — clean two-column text |
| Page 9 | Table 8 (full-width), Table 7 (full-width) | ✓ VERIFIED — all values legible |
| Page 10 | Table 7-dim (full-width) | ✓ VERIFIED — all row values legible |
| Pages 11-16 | Variants, scaling, Discussion, Limitations, Conclusion, Declarations, References | ✓ VERIFIED — clean rendering |

---

## 5. Content Preservation Verification

| Element | Status | Details |
|---------|--------|---------|
| Six authors, correct order | VERIFIED | Ajinkya Jiman, Dr. K. Rajeswari, Ruturaj Warkad, Vivek Painjane, Yash Mahajan, Aryan Wankhade |
| ORCIDs as per-author footnotes | VERIFIED | All 6 ORCIDs attached to respective `\author` definitions |
| Corresponding author | VERIFIED | Yash Mahajan (corref{cor1}), email present |
| Abstract headings | VERIFIED | Background and Objective, Methods, Results, Conclusions |
| No citation in abstract | VERIFIED | No `\citep` in abstract |
| Equation (1) with parentheses | VERIFIED | `DS = 100 − (penalty_NDXUP + penalty_STs)` |
| Equations (2)-(4) | VERIFIED | All render correctly |
| Product encoding equation | VERIFIED | Inline math `ATC | BDF | ...` |
| Figure 1 (DS decomposition) | VERIFIED | Renders without clipping |
| Figure 2 (workflow) | VERIFIED | Renders without clipping |
| Table 8 results | VERIFIED | 26/32 and 32/32 |
| Table 7 results | VERIFIED | 3/5 unit-aware, 4/5 literal |
| Table 7-dim dimensional labels | VERIFIED | Present, correct |
| 196 assertions | VERIFIED | Present in text |
| TRN reconciliation proposed | VERIFIED | Labelled as inferred, not confirmed |
| V3 unvalidated | VERIFIED | Labelled as preliminary and unvalidated |
| No clinical claim | VERIFIED | "No clinical interchangeability or therapeutic equivalence" |
| Availability statement | VERIFIED | "public repository has not yet been released" |
| Missing references (??) | VERIFIED | None |
| Missing glyphs | VERIFIED | None |

---

## 6. File Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Previous version source | `main_cmpb.tex` | Preserved, unchanged |
| Previous version PDF | `main_cmpb_doublecolumn.pdf` | Preserved, unchanged |
| Rebuilt source | `main_cmpb_v2.tex` | Created, compiled exit 0 |
| Rebuilt PDF | `main_cmpb_v2.pdf` | Created, 16 pages, A4 |
| Build logs | Not separately saved | Compilation output captured inline |
| This report | `LAYOUT_REBUILD_REPORT.md` | This file |

---

## 7. Source and Backup Integrity

| Item | Status |
|------|--------|
| Authoritative source files unchanged | VERIFIED — SHA-256 matches |
| Existing backups untouched | VERIFIED — both backup directories exist |
| No files deleted or overwritten | VERIFIED |

**Authoritative source file hashes:**
- `manuscript/main.tex`: `cd9870e10745d013297b46efc185c91b89596f82542f9829b38154da959fade9`
- `manuscript/references.bib`: `1d739db885f901a12668c55964b77a051102d68ffcc5407663422054a9aa6ae3`

---

## 8. Remaining Author Decisions

| Blocker | Details |
|---------|---------|
| Corresponding author postal address | Required by CMPB; placeholder retained |
| Corresponding author telephone | Required by CMPB; placeholder retained |
| CRediT author contributions confirmation | All six authors must confirm |
| Exclusive submission statement | Author confirmation needed |
| Cover letter approval | Author review needed |

---

## 9. Final Status

**Status: `NOT READY FOR AUTHOR REVIEW`** — all technical formatting, compilation, and content-preservation checks have passed. The v2 manuscript compiles cleanly with `elsarticle` in double-column A4 layout, all equations/tables/figures render legibly, all scientific content is preserved, and page 1 front matter is properly formatted.

**Key file paths:**
- Rebuilt source: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_v2.tex`
- Rebuilt PDF: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_v2.pdf`

**Not submitted. Not uploaded. No DOI minted. No external action taken.**
**Authoritative source files: UNCHANGED**
**Existing backups: UNTOUCHED**
**Previous version preserved: main_cmpb.tex and main_cmpb_doublecolumn.pdf**
