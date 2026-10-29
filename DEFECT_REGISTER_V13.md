# Defect Register — CMPB V13 Layout Correction Pass

**Project:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Source:** `main_cmpb_v13.tex`
**Baseline PDF:** `main_cmpb_v13.pdf` (9 pages, A4)
**Final PDF:** `main_cmpb_v13_final.pdf`

---

## Issue Register & Resolution

| ID | Page | Issue Description | Location in Source | Fix Applied | Verified |
|----|------|-------------------|-------------------|-------------|----------|
| A | 2 | Awkward wrapping around "fixed-dose-combination extension" in contribution paragraph | Line 74 | No fix needed — bbox analysis showed CLEAN on page 2 | ✅ Verified CLEAN |
| B | 2 | Right-column alignment defects | — | No fix needed — bbox analysis showed CLEAN on page 2 | ✅ Verified CLEAN |
| C | 3 | "EDQM" overflow/spill near column boundary | Line 107 | No fix needed — bbox shows EDQM at xMax=301.8pt (left column, not crossing) | ✅ Verified CLEAN |
| D | 4 | Inline code path `code/ds_algorithm.py` overflows column boundary | Line 197 | Changed to `\texttt{code/}\allowbreak\texttt{ds\_algorithm.py}` | ✅ Verified CLEAN |
| D2 | 4 | NDXUP expression `$1 - \text{penalty}_{\text{NDXUP}}/10$` crosses column boundary | Line 185 | Wrapped in `\linebreak[4]\mbox{$1 - \text{penalty}_{\hbox{NDXUP}}/10$}` | ✅ Verified CLEAN |
| E | 5 | Section 6.5 heading "Table 7: fixed-dose-combination NDXUP sums" extends beyond right column | Line 287 | Added forced line break: `fixed-dose-combination\\ NDXUP sums` | ✅ Verified CLEAN |
| F | 6 | `find_substitutes` identifier formatting/overflow (3 occurrences) | Lines 204, 210, 385 | All changed to `\texttt{find\_sub}\allowbreak\texttt{stitutes}` with `\texttt{}` formatting | ✅ Verified CLEAN |
| F3 | 4 | Figure 2 embedded title overlaps diagram | `figures/workflow.tex` lines 28-30 | Removed embedded title; added `\path (current bounding box.north) -- ++(0,0.8cm)` for caption clearance | ✅ Verified CLEAN |
| E2 | 7 | CRediT author-contribution text cramped/overlap in right column | Line 438 | Split into three paragraphs with explicit line breaks | ✅ Verified CLEAN |
| F2 | 7 | Conclusion text "substitution-scoring" hyphenated across column boundary | Line 421 | Changed to `\linebreak[4]\mbox{substitution-scoring}` | ✅ Verified CLEAN |

---

## General Visual Audit Results (All 9 Pages)

| Page | Status | Notes |
|------|--------|-------|
| 1 | Front matter (single-column) | Title, authors, abstract, keywords span full width — expected crossings, not defects |
| 2 | ✅ CLEAN | Left/right columns properly separated |
| 3 | ✅ CLEAN | Section 3.1 EDQM text contained |
| 4 | ✅ CLEAN | Code path, NDXUP expression, Figure 2 fixed |
| 5 | ✅ CLEAN | Section 6.5 heading fits |
| 6 | ✅ CLEAN | `find_substitutes` and all code identifiers contained |
| 7 | ✅ CLEAN | CRediT section formatted; Conclusion text flows correctly |
| 8 | ✅ CLEAN | References flow properly |
| 9 | ✅ CLEAN | References continue, no clipping |

---

## Compilation Result

- **Command:** `DYLD_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub DYLD_FALLBACK_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub /opt/homebrew/bin/tectonic main_cmpb_v13.tex`
- **Exit code:** 0 (success)
- **Pages:** 9
- **Page size:** A4 (595.28 × 841.89 pts)
- **Warnings:** Only underfull hbox in bibliography (normal), no overfull hbox in main text

---

## Preservation Confirmation

- ✅ `main_cmpb_v12.tex` and all earlier versions unchanged
- ✅ Scientific content, equations, citations, references, author details preserved
- ✅ No global margin/font/column changes made
- ✅ No submission/publication/upload performed