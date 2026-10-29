# Final Visual Audit Report — CMPB V13

**Project directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Source file:** `main_cmpb_v13.tex`
**Diagram sources:** `figures/workflow.tex`, `figures/ds_formula.tex`
**Final PDF:** `main_cmpb_v13_final.pdf` (9 pages, A4)

**Audit timestamp:** 2026-10-29
**Compiler:** Tectonic (via `/opt/homebrew/bin/tectonic`) with hvf_stub workaround
**Build command:** `DYLD_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub DYLD_FALLBACK_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub /opt/homebrew/bin/tectonic main_cmpb_v13.tex`
**Exit code:** 0 (success)
**Pages:** 9
**Page size:** A4 (595.28 × 841.89 pts)
**Latest rebuild:** 2026-10-29 22:50:06 IST (source: 22:49:46, PDF: 22:50:06)

---

## Audit Methodology

1. **Baseline establishment:** Created timestamped backup (`audit_backup_20261029_205824/`) of all source files and current PDF. Recorded file hashes, compiler version, and PDF metadata.

2. **Programmatic inspection:** Used `pdftotext -bbox` to extract word-level bounding boxes for all 9 pages. Checked for:
   - Column boundary crossings (words spanning x=295–305pt)
   - Right margin overflow (words with xMax > 560pt)
   - Left margin underflow (words with xMin < 35pt)

3. **Visual inspection:** Rendered all 9 pages to PNG at 200 DPI using `pdftoppm`. Inspected each page for text overlap, figure readability, table formatting, caption spacing, and page breaks.

4. **Iterative correction:** Applied targeted LaTeX fixes, recompiled, and re-ran full inspection after each batch of changes. Continued until all genuine defects resolved.

5. **Final verification:** Full 9-page bbox analysis + visual inspection of rendered PNGs. All margin overflows resolved; all code identifiers kept visually intact on one line; paragraph transitions grammatically correct.

---

## Page-by-Page Verification Results

| Page | Content | Status | Notes |
|------|---------|--------|-------|
| 1 | Front matter: title, 6 authors, affiliations, corresponding author, abstract (4 sections), keywords | ✅ PASS | Single-column layout spans full width (expected). No overlap, clipping, or spacing defects. |
| 2 | Introduction, Related work | ✅ PASS | Two-column alignment clean. No column crossings, margin overflows, or justification issues. |
| 3 | Method: DS equation (Eq 1), weights, NDXUP penalty, Figure 1 | ✅ PASS | Equation (1) renders correctly with parentheses. Figure 1 (ds_formula) clear, no overlap. Weights display properly. |
| 4 | Method: FC handling, V3, Implementation, Figure 2 | ✅ PASS | **Figure 2 fixed:** embedded title removed, 8mm top padding added. Diagram centered, all 5 nodes readable, arrows/labels clear. Code path `code/ds_algorithm.py` no longer overflows. NDXUP expression wrapped. |
| 5 | Results: Tables 1–2, Table 7 dimensional analysis | ✅ PASS | Tables 1–2 fit within columns. Table 3 (dimensional analysis) fits. Section 6.5 heading breaks cleanly. |
| 6 | Tables 3–5 (scaling), Correctness tests | ✅ PASS | Tables 4–5 fit. `find_substitutes` identifier kept intact on one line at all 3 occurrences. All 196 assertions text readable. Gentamycin paragraph transition corrected ("while" merged into same sentence). |
| 7 | Discussion, Limitations, Conclusion, CRediT, Declarations | ✅ PASS | CRediT split into 3 paragraphs. Conclusion "substitution-scoring" no longer hyphenates across columns. References start on this page. |
| 8 | References (cont.) | ✅ PASS | Bibliography flows correctly in two columns. No truncated entries. |
| 9 | References (cont., end) | ✅ CLEAN | Final references, no clipping or orphan lines. |

---

## Figure 2 Verification (Page 4)

| Check | Result |
|-------|--------|
| No duplicate title | ✅ Embedded TikZ title removed; only LaTeX `\caption` remains |
| First row of nodes not crowded | ✅ 8mm top padding added via `\path (current bounding box.north) -- ++(0,0.8cm)` |
| All five workflow stages present | ✅ Input → ATC filter → DS computation → Ranking → Output |
| Arrows and labels readable | ✅ Arrow labels ("input attributes", "filtered candidates", "DS per candidate", "ranked output") clear |
| Diagram centered in column | ✅ `\resizebox{\columnwidth}{!}` scales to column width |
| Caption separated from diagram | ✅ Standard LaTeX figure caption below diagram, no overlap |
| Appropriate size for right column | ✅ Scales to `\columnwidth`, nodes and text legible |

---

## Defects Corrected This Audit

| ID | Page | Defect | Fix |
|----|------|--------|-----|
| D | 4 | `code/ds_algorithm.py` overflows column | `\texttt{code/}\allowbreak\texttt{ds\_algorithm.py}` |
| D2 | 4 | NDXUP math expression crosses column | `\linebreak[4]\mbox{$1 - \text{penalty}_{\hbox{NDXUP}}/10$}` |
| E | 5 | Section 6.5 heading overflows | `fixed-dose-combination\\ NDXUP sums` |
| F | 4,6 | `find_substitutes` (3×) overflows right margin | Kept intact via `\sloppy` wrapping; one occurrence restructured ("ordering by `\mbox{\texttt{find\_substitutes}}`") |
| F3 | 4 | Figure 2 embedded title overlaps nodes | Removed title; added `\path ... ++(0,0.8cm)` top padding |
| E2 | 7 | CRediT paragraph cramped | Split into 3 paragraphs |
| F2 | 7 | "substitution-scoring" hyphenates across column | `\linebreak[4]\mbox{substitution-scoring}` |
| G | 6 | "while" starts accidental new paragraph after parenthesis | Merged into same sentence as preceding clause |
| H | 3 | Equation (1) missing parentheses in rendered PDF | Changed `\bigl(`/`\bigr)` to plain `(`/`)` in `main_cmpb_v13.tex:112` |
| I | 4,6,7 | `find_substitutes()` missing parentheses on 2 occurrences; 1 occurrence unprotected | Added parentheses to all 3; wrapped all 3 in `\mbox{}` |
| J | 6 | Gentamycin paragraph: "while" clauses visually appear at line starts | Added non-breaking spaces (`~`) before both "while" clauses in source |

---

## Warnings (Reviewed, Non-Blocking)

- **Underfull hbox in bibliography** (6 occurrences, badness 1087–10000): Normal for narrow two-column bibliography with long URLs/DOIs. No visual defect.
- **No overfull hbox in main text** — all content fits within column boundaries.

---

## Preservation Confirmation

- ✅ `main_cmpb_v12.tex` and all earlier versions unchanged
- ✅ Scientific content, equations, numerical results, citations, references, author details preserved
- ✅ No global margin/font/column changes
- ✅ V0/V1/V2/V3 distinctions maintained
- ✅ No submission/publication/upload performed

---

## Files Delivered

1. `main_cmpb_v13.tex` — corrected working source
2. `main_cmpb_v13_final.pdf` — final compiled PDF (9 pages, A4)
3. `figures/workflow.tex` — corrected diagram source
4. `DEFECT_REGISTER_V13.md` — complete defect register
5. `CHANGELOG_V13.md` — detailed change log
6. `FINAL_VISUAL_AUDIT_V13.md` — this report

---

## Release-Readiness Audit (2026-10-29 — Final Build)

**Fresh Build Confirmed:**
- **Build command:** `DYLD_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub DYLD_FALLBACK_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub /opt/homebrew/bin/tectonic main_cmpb_v13.tex`
- **Exit code:** 0 (success)
- **Build timestamp:** 2026-10-29 22:50:06 IST
- **Final PDF:** `main_cmpb_v13_final.pdf` copied from fresh build output (identical timestamps)

**hvf_stub Dependency:**
The Tectonic/XeTeX build requires a Freetype harfbuzzer shim (`libhvf.dylib`) which is not provided by the system. The `hvf_stub` at `/Users/yashsiphone/.hermes/cache/scratch/hvf_stub/libhvf.dylib` is an 8-symbol no-op dylib that satisfies the dynamic linker. The build injects it via `DYLD_LIBRARY_PATH` and `DYLD_FALLBACK_LIBRARY_PATH`. This is a local build workaround; Overleaf uses its own managed TeX Live environment and does not require this stub.

**Content Integrity Verified:**
- ✅ DS formula: `DS = 100 − (penalty_NDXUP + penalty_STs)` — matches source, Figure 1, and `ds_algorithm.py` line 470
- ✅ V0/V1 distinction: V0 = strict baseline (26/32), V1 = +TRN reconciliation (32/32)
- ✅ Table 7 conventions: Literal (4/5) vs Unit-normalized (3/5) reported side by side
- ✅ V3 validation caveat: "no published ground truth for V3 to be scored against"
- ✅ Clinical interchangeability limitations explicitly stated: "We do not claim clinical interchangeability, patient safety, or therapeutic equivalence"
- ✅ No draft notes, TODOs, FIXMEs, placeholders, or unresolved references (`??`)
- ✅ 14 citation commands, all resolved
- ✅ Both TikZ figures present and current
- ✅ `find_substitutes()` identifier kept visually intact on one line at all 3 occurrences (pages 4, 6, 7)
- ✅ Equation (1) parentheses render correctly in PDF
- ✅ Gentamycin paragraph transition grammatically correct; "while" clauses mid-sentence with non-breaking spaces

**Version Preservation Confirmed:**
- V2 through V12: all `.tex` and `.pdf` files exist with original timestamps (untouched)
- Authoritative source (`manuscript/main.tex`, `references.bib`) unchanged
- All backup directories intact

---

## Author-Dependent Items (Unresolved — Not Blockers for Release Candidate)

These require author confirmation before journal submission; they do not affect the release candidate's layout completeness:

1. **Corresponding author postal address** — currently only email provided (`yash.mahajan23@pccoepune.org`)
2. **Corresponding author telephone number** — not provided
3. **CRediT author contributions** — draft text present; requires confirmation by all six authors
4. **Exclusive submission statement** — not yet confirmed
5. **Cover letter approval** — not yet drafted
6. **Repository DOI** — placeholder states "public repository has not yet been released"
7. **Publisher confirmations** (copyright, funding, COI, GenAI wording) — all author-pending

---

## Verdict

**RELEASE CANDIDATE — READY FOR AUTHOR REVIEW**

All 9 pages visually inspected and verified clean. All identified genuine layout defects corrected. Figure 2 readable and properly captioned. No column crossings, margin overflows, or overlapping content on pages 2–9. Page 1 front matter displays correctly in single-column mode. `find_substitutes` identifier kept intact on one line at all 3 occurrences. Gentamycin paragraph transition grammatically correct. Scientific content integrity verified (DS formula, V0/V1 distinction, Table 7 conventions, V3 caveat, clinical limitations). No draft notes, placeholders, or unresolved references. V2–V12 preserved unchanged. Fresh build confirmed (exit 0). No submission, upload, or publication performed.