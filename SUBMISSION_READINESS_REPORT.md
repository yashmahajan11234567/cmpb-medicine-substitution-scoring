# CMPB Submission Readiness Report

**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28`
**Report date:** 2026-10-28
**Status:** NOT SUBMISSION-READY — author input required

---

## Defects Found and Corrected

### Defect 1: ORCIDs removed from reformatted source
**Issue:** When converting from `article` to `elsarticle` class, the `\orcid{}` commands were removed from author definitions because `\orcid` is not defined in `elsarticle`. ORCIDs were not preserved anywhere in the working copy.
**Correction:** Each author now has their own `\footnote{ORCID: ...}` directly attached to their `\author` definition (lines 24–29). The `\cortext[cor1]` field contains only the corresponding-author email. Verified in rendered PDF page 1 — all 6 ORCIDs appear as individual author footnotes.

### Defect 2: Tables overflowing in double-column layout
**Issue:** 5 tables had significant overfull boxes in the double-column `elsarticle` layout:
- Table 8: 217pt too wide
- Table 7: 158pt too wide
- Table 7-dim: 231pt too wide
- Table variants: 85pt too wide
- Table scaling: 124pt too wide
**Correction:** Wrapped each table's `tabular` environment in `\resizebox{\columnwidth}{!}{...}` to scale content to fit the column width.

### Defect 3: Product encoding equation too wide
**Issue:** The product encoding equation* (`ATC | BDF | AME | ISI | RCA | TRN | NDXUP`) was 25pt too wide in a single column.
**Correction:** Wrapped in `\resizebox{\columnwidth}{!}` using inline math `\(...\)` instead of `equation*` environment (since `\resizebox` cannot wrap display math environments).

### Defect 4: Equation 2 too wide
**Issue:** Equation 2 (`penalty_NDXUP ∈ {0,2,4,6,8,10}` with `\quad\text{from Table 4 of the specification}`) was 121pt too wide.
**Correction:** Removed `\quad\text{from Table 4 of the specification}` from inside the equation environment; placed it as regular text after the equation.

### Defect 5: `\resizebox` wrapping display equation caused LaTeX error
**Issue:** Wrapping `equation` environments inside `\resizebox` caused "Missing $ inserted" errors because `\resizebox` expects horizontal-mode box content, not display math.
**Correction:** Unwrapped Equation 3 from `\resizebox`; kept it as a standard numbered equation. The equation fits within the column width without the resizebox wrapper.

### Defect 6: PDF page size was Letter instead of A4
**Issue:** The default `elsarticle` class produced Letter-sized pages (612 x 792 pts).
**Correction:** Added `a4paper` option to `\documentclass[12pt,twocolumn,a4paper]{elsarticle}`. PDF is now A4 (595.28 x 841.89 pts).

### Defect 7: Double backslash before `\mu` in scaling table
**Issue:** A patch introduced `\\mu` (2 backslashes) instead of `\mu` (1 backslash) in the scaling table header.
**Correction:** Fixed to single backslash `\mu`.

---

## 1. Verified Official CMPB Requirements

**Source:** Elsevier Guide for Authors, Computer Methods and Programs in Biomedicine (ISSN 0169-2607)
**URL:** https://www.sciencedirect.com/journal/computer-methods-and-programs-in-biomedicine/publish/guide-for-authors
**Access date:** 2026-10-28

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Article type: original research | Verified | Manuscript fits CMPB scope |
| Journal scope | Verified | Computing methods for biomedical research |
| Structured abstract headings | Verified | Background and Objective, Methods, Results, Conclusions |
| Abstract word limit (max 350) | Verified | ~335 words |
| No citations in abstract | Fixed | Removed `\citep{caviglioli2025medicine}` from abstract |
| Body word limit (max 3,500) | Verified | ~1,807 words |
| References (max 50) | Verified | 25 cited, 34 in .bib |
| Numbered sections | Verified | 9 numbered sections |
| Ethics statement | Present | "Not applicable" |
| Funding statement | Present | "No specific grant" |
| Competing interests | Present | "No known competing interests" |
| Author contributions (CRediT) | Present | Flagged for author confirmation |
| Generative AI disclosure | Present | ChatGPT disclosed |
| Data and code availability | Present | Project directory statement |
| Keywords | Present | 7 keywords |
| Editable .tex source | Present | main_cmpb.tex |
| Single corresponding author | Present | Yash Mahajan |

---

## 2. Requirements Not Yet Verified

| Item | Reason |
|------|--------|
| Body word count exact method | CMPB doesn't specify exact counting method; our estimate ~1,807 words |
| Elsevier elsarticle class mandatory? | Guide says "use latest Elsevier LaTeX class files" — ambiguous |
| Postal address mandatory for corresponding author | Guide requires full contact details; email alone may not suffice |
| Telephone number mandatory | Guide requires telephone; not available |
| Article highlights mandatory? | Listed as "encouraged" |
| Graphical abstract mandatory? | Listed as "encouraged" |
| Exact elsarticle options for CMPB | Not specified in Guide |

---

## 3. Original Source File Hashes (UNCHANGED)

| File | SHA-256 |
|------|---------|
| manuscript/main.tex | cd9870e10745d013297b46efc185c91b89596f82542f9829b38154da959fade9 |
| manuscript/references.bib | 1d739db885f901a12668c55964b77a051102d68ffcc5407663422054a9aa6ae3 |

---

## 4. Working Directory Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| Baseline source (copy) | `main.tex` | Copied, SHA-256 verified |
| Baseline bibliography | `references.bib` | Copied, SHA-256 verified |
| Figure sources | `figures/` | Copied, SHA-256 verified |
| Baseline PDF | `baseline_main.pdf` | 16 pages |
| Reformatted source (elsarticle) | `main_cmpb.tex` | Compiled, exit 0 |
| Reformatted PDF (double-column, A4) | `main_cmpb_doublecolumn.pdf` | 13 pages, A4 |
| Build logs | `cmpb_build_pass1.log`, `pass2.log` | Captured |
| Article highlights | `highlights_cmpb.txt` | 5 bullets, all ≤85 chars |
| Cover letter draft | `cover_letter_cmpb.md` | Draft with placeholders |
| Submission readiness report | `SUBMISSION_READINESS_REPORT.md` | This file |

---

## 5. Source and Backup Integrity

| Item | Status |
|------|--------|
| Authoritative source files unchanged | VERIFIED — SHA-256 matches |
| Existing backups untouched | VERIFIED — both backup directories exist |
| No files deleted or overwritten | VERIFIED |

---

## 6. LaTeX Build Results (Final)

| Check | Baseline (article) | Reformatted (elsarticle, twocolumn, A4) |
|-------|-------------------|-----------------------------------------|
| Tectonic exit code | 0 | 0 |
| LaTeX errors | 0 | 0 |
| Undefined references | 0 | 0 |
| Overfull boxes | Several | 0 (all fixed) |
| Page count | 16 | 13 |
| Page size | A4 | A4 |
| Bibliography | Resolved | Resolved |

---

## 7. Content Verification Results

| Element | Status | Details |
|---------|--------|---------|
| Six authors, correct order | VERIFIED | Ajinkya Jiman, Dr. K. Rajeswari, Ruturaj Warkad, Vivek Painjane, Yash Mahajan, Aryan Wankhade |
| Corresponding author | VERIFIED | Yash Mahajan (corref{cor1}), email present |
| ORCIDs preserved | VERIFIED | All 6 ORCIDs as per-author footnotes: Ajinkya Jiman 0000-0002-9239-5542; Dr. K. Rajeswari 0000-0002-5392-3920; Ruturaj Warkad 0009-0002-5318-9268; Vivek Painjane 0009-0008-4288-1885; Yash Mahajan 0009-0004-3789-1641; Aryan Wankhade 0009-0006-3026-8261 |
| Abstract headings | VERIFIED | Background and Objective, Methods, Results, Conclusions (plural) |
| No citation in abstract | VERIFIED | No `\citep` in abstract |
| Equation (1) with parentheses | VERIFIED | `DS = 100 − (penalty_NDXUP + penalty_STs)` |
| Table 7 dimensional labels | VERIFIED | Present, correct |
| Table 8 results | VERIFIED | 26/32 and 32/32 |
| Figure 1 (DS formula) | VERIFIED | Present |
| Figure 2 (workflow) | VERIFIED | Present |
| 196 assertions | VERIFIED | Present in text |
| TRN reconciliation proposed | VERIFIED | Labelled as inferred, not confirmed |
| V3 unvalidated | VERIFIED | Labelled as preliminary and unvalidated |
| No clinical claim | VERIFIED | "No clinical interchangeability or therapeutic equivalence" |
| Availability statement | VERIFIED | "public repository has not yet been released" |
| Missing references (??) | VERIFIED | None (only legitimate "?" in "Dim. valid?" table header) |
| Missing glyphs | VERIFIED | None |

---

## 8. Word Counts

| Element | Count | Limit | Status |
|---------|-------|-------|--------|
| Abstract | ~335 words | 350 | Under limit |
| Body (approx) | ~1,807 words | 3,500 | Under limit |

---

## 9. Article Highlights

| Bullet | Characters | Status |
|--------|-----------|--------|
| 1 | 81 | Within 85-char limit |
| 2 | 81 | Within 85-char limit |
| 3 | 80 | Within 85-char limit |
| 4 | 85 | Within 85-char limit |
| 5 | 75 | Within 85-char limit |

---

## 10. Corresponding Author Contact

| Field | Value | Status |
|-------|-------|--------|
| Name | Yash Mahajan | Present |
| Email | yash.mahajan23@pccoepune.org | Present |
| Affiliation | Pimpri Chinchwad College of Engineering, Pune, 411044, Maharashtra, India | Present |
| Postal address | [PLACEHOLDER — AUTHOR CONFIRMATION REQUIRED] | MISSING |
| Telephone | [PLACEHOLDER — AUTHOR CONFIRMATION REQUIRED] | MISSING |

---

## 11. Author Approvals Required

| Item | Status |
|------|--------|
| CRediT author contributions confirmation | Awaiting all six authors |
| Exclusive submission statement | Awaiting author confirmation |
| Postal address and telephone | Awaiting corresponding author |
| Cover letter approval | Awaiting author review |

---

## 12. Final Checklist

| Item | Status |
|------|--------|
| Formatting changes applied | Verified complete |
| Compilation successful (both versions) | Verified complete |
| Scientific content preserved | Verified complete |
| Abstract compliant (no citations, correct headings) | Verified complete |
| Word counts within limits | Verified complete |
| Article highlights prepared | Verified complete |
| Cover letter drafted | Complete with placeholders |
| Corresponding author contact complete | **AWAITING AUTHOR INPUT** |
| Author approvals obtained | **AWAITING AUTHOR INPUT** |
| Submission package assembled | **NOT ASSEMBLED** (awaiting author input) |

**Overall status: NOT READY FOR AUTHOR REVIEW**

| Not submitted. Not uploaded. No DOI minted. No external action taken. |

---

## Quality Gate Findings — Final Audit

### Table-by-table readability (visual inspection at 150 DPI)

| Table | Location | Rendered size | Legibility | Overflow |
|-------|----------|--------------|------------|----------|
| Table 8 (DS scores) | Page 7 | ~9pt | Legible | None |
| Table 7 (FC sums) | Page 7 | ~9pt | Legible | None |
| Table 7-dim (dimensional analysis) | Page 8 | ~8pt | Legible | None |
| Table 4 (variants) | Page 8 | ~9pt | Legible | None |
| Table 5 (scaling) | Page 8 | ~9pt | Legible | None |

All headers, values, units, footnotes, and "Dim. valid?" column entries are legible at normal viewing scale. No text overflow beyond column margins.

### Visual inspection results (all 13 pages)

| Page | Content | Status |
|------|---------|--------|
| Page 1 | Title, authors, ORCID footnotes, abstract, keywords | VERIFIED — no overlaps, no clipping |
| Page 2 | Introduction, Related work | VERIFIED — clean two-column text |
| Page 3 | Method, Equations (1)–(4) | VERIFIED — Equation (1) shows `DS = 100 − (penaltyNDXUP + penaltySTs)` with parentheses |
| Page 4 | Figure 1 (DS decomposition), Sections 3.1–3.3 | VERIFIED — no clipping, Figure 1 readable |
| Page 5 | Section 4 (Implementation) | VERIFIED — clean two-column text |
| Page 6 | Figure 2 (workflow), Section 5 | VERIFIED — Figure 2 readable, caption legible |
| Pages 7–8 | Tables 8, 7, 7-dim, variants, scaling | VERIFIED — all legible, no overflow |
| Pages 9–13 | Results, Discussion, Limitations, Conclusion, Declarations, References | VERIFIED — clean rendering |

### Build and PDF metadata

| Property | Value |
|----------|-------|
| Compiler | Tectonic |
| Exit code | 0 (both passes) |
| LaTeX errors | 0 |
| Undefined references | 0 |
| Overfull boxes | 0 |
| Pages | 13 |
| Page size | A4 (595.28 × 841.89 pts) |
| Producer | xdvipdfmx |

### Remaining technical or editorial blockers

| Blocker | Details |
|---------|---------|
| Corresponding author postal address | Required by CMPB; placeholder retained |
| Corresponding author telephone | Required by CMPB; placeholder retained |
| CRediT author contributions confirmation | All six authors must confirm |
| Exclusive submission statement | Author confirmation needed |
| Cover letter approval | Author review needed |


---

**Files changed (formatting only, in working directory):**
- `main_cmpb.tex`: elsarticle class, twocolumn, a4paper, frontmatter, structured abstract, no abstract citation, "Conclusions" heading, ORCIDs in \cortext, tables wrapped in \resizebox, product encoding equation wrapped in \resizebox, Equation 2 text moved out of equation environment
- `highlights_cmpb.txt`: created (new file)
- `cover_letter_cmpb.md`: created (new file)
- `SUBMISSION_READINESS_REPORT.md`: updated (this file)

**Authoritative source files: UNCHANGED**
**Existing backups: UNTOUCHED**

**Key file paths:**
- Corrected source: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb.tex`
- Corrected PDF: `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/main_cmpb_doublecolumn.pdf`
