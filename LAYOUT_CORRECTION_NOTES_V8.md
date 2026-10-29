# Layout Correction Report — CMPB Manuscript V8

**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Report date:** 2026-10-28

---

## 1. Root Cause of Front-Matter Split

**Root cause:** `elsarticle` with `twocolumn` document class option typesets the `frontmatter` environment in **two columns** by default. V7 used `\documentclass[12pt,twocolumn,a4paper]{elsarticle}` (still containing `twocolumn` — the V6→V7 copy never actually removed it). This caused page 1 to show title/authors in left column with abstract text flowing into right column.

**Additional defect:** V7 had `\section*{References}` immediately before `\bibliography{references}`. Since `elsarticle` + `plainnat` already inserts its own "References" section heading via `\bibliography{}`, this created a duplicate References heading.

---

## 2. Fix Applied — `main_cmpb_v8.tex`

**File:** `main_cmpb_v8.tex` (new file; `main_cmpb_v7.tex` preserved unchanged)

| Change | Location | Before (V7) | After (V8) | Reason |
|--------|----------|-------------|------------|--------|
| Document class | Line 1 | `\documentclass[12pt,twocolumn,a4paper]{elsarticle}` | `\documentclass[a4paper]{elsarticle}` | `elsarticle` without `twocolumn` typesets frontmatter in single column by default |
| Before frontmatter | Lines 18-21 | `\begin{document}\n\n{...` | `\begin{document}\n\n\onecolumn\n\n{...` | Explicit single-column mode for frontmatter (belt-and-suspenders with document class change) |
| Duplicate References heading | Line 427 | `\section*{References}\n\n\bibliographystyle...` | `\bibliographystyle{plainnat}\n\bibliography{references}` | `elsarticle`+`plainnat` already inserts References heading via `\bibliography{}`; explicit `\section*{References}` creates duplicate |

**Why this works:** `elsarticle` with `twocolumn` option typesets frontmatter in two columns regardless of explicit switches. Removing `twocolumn` from the document class option makes frontmatter single-column by default. `\onecolumn` before `\begin{frontmatter}` ensures single-column mode explicitly. `\twocolumn` after `\end{frontmatter}` switches to two-column body layout.

---

## 3. Build Results — Final

| Check | V7 (broken) | V8 (fixed) |
|-------|-------------|------------|
| Tectonic exit code | 0 | **0** |
| LaTeX errors | 0 | **0** |
| Undefined references | 0 | **0** |
| Page count | 13 | **13** |
| Page size | A4 | **A4** |
| Page 1 frontmatter | Abstract overlapping right column | **Clean single column, no overlap** |
| Duplicate References heading | YES | **NO** |

**Commands executed:**
- `/opt/homebrew/bin/tectonic main_cmpb_v8.tex` → exit 0 (pass 1)
- `/opt/homebrew/bin/tectonic main_cmpb_v8.tex` → exit 0 (pass 2)

**Environment:** `DYLD_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub` for Tectonic freetype workaround.

---

## 4. Page-by-Page Visual Inspection Results

All 13 pages of `main_cmpb_v8.pdf` rendered at 100 DPI via `pdftoppm` and inspected visually.

| Page | Content | Status | Key observations |
|------|---------|--------|------------------|
| 1 | Title, 6 authors with ORCIDs, affiliation, corresponding email, structured abstract (4 headings start here) | PASS | Page 1 is clean, single column, no overlap. Title spans full width. All 6 authors listed once in correct order with ORCIDs below affiliation. Corresponding email: yash.mahajan23@pccoepune.org. Affiliation: Pimpri Chinchwad College of Engineering, Pune, 411044, Maharashtra, India. Abstract: Background and Objective, Methods, Results, Conclusions heading visible — Conclusions paragraph continues to page 2. No overlapping text between columns. No text clipping at margins. |
| 2 | Conclusions continuation, Keywords | PASS | Conclusions paragraph completes at top of page 2. Keywords present below abstract. Remainder of page blank (front matter complete). No overlap. |
| 3 | Section 1 Introduction, Section 2 Related work | PASS | Section 1 Introduction starts at top of page 3. Clean two-column body layout. No overlapping text. |
| 4 | Section 3 Method, Equations (1)-(4), Figure 1 | PASS | Equation (1) shows `DS = 100 − (penaltyNDXUP + penaltySTs)` with parentheses. Figure 1 renders without clipping. |
| 5 | Section 3.2-3.4, Figure 2 workflow | PASS | Figure 2 renders without clipping. Caption legible. |
| 6 | Section 6 Results, Table 1 (DS scores) | PASS | Table renders without overflow. All values legible. |
| 7 | Table 2 (Table 7 sums), Section 6.5-6.7 | PASS | Full-width table. All values legible. |
| 8 | Table 3 Dimension Analysis, Table 4 Variants | PASS | Full-width tables. All 5 rows A-E legible. Table 4 legible. No overflow. |
| 9 | Table 5 Scaling, Section 7 Discussion | PASS | Full-width table. All values legible. |
| 10 | Section 8 Limitations, Section 9 Conclusion | PASS | Clean two-column text. |
| 11 | Section 10 Declarations | PASS | All declarations readable. |
| 12 | References [1]-[17] | PASS | Exactly ONE References heading. References readable. |
| 13 | References [18]-[25], last page | PASS | References complete through [25]. Page ends cleanly. Page number "13" at bottom. |

**Visual inspection result: Page 1 verified clean and non-overlapping (mandatory acceptance condition met).** Abstract continues from page 1 to page 2 — this is acceptable per user guidance: "If the journal-compatible structure requires the abstract to continue onto page 2, allow that rather than forcing a broken first page." No overlapping text anywhere in the document. No clipping, no missing glyphs, no orphaned captions, no duplicate References heading.

---

## 5. Scientific Preservation Verification

| Element | Status | Details |
|---------|--------|---------|
| Equation (1): `DS = 100 − (penalty_NDXUP + penalty_STs)` | VERIFIED | Both penalties subtracted inside parentheses, page 4 |
| V0: 26/32 Table 8 matches | VERIFIED | Page 6 Table 1 |
| V1: 32/32 with proposed TRN reconciliation | VERIFIED | Page 6 Table 1 |
| TRN reconciliation proposed/inferred | VERIFIED | Labelled "proposed reconciliation" and "inferred from published scores" |
| Table 7: unit-normalized 3/5, literal 4/5 | VERIFIED | Page 7 Table 2 |
| No match claimed dimensionally valid | VERIFIED | Page 8 Table 3 labels Row B "No (tab count)", Row C "No (g not converted)", Row E "No (g not converted)" |
| V3: preliminary and unvalidated | VERIFIED | Sections 3.4, 7.3 |
| No clinical interchangeability claim | VERIFIED | Sections 7.3, 8.4 |
| No public repository/DOI claimed | VERIFIED | Section 10.6 |
| 196 assertions | VERIFIED | Abstract, Section 6.8 |
| All six authors in correct order | VERIFIED | Page 1 |
| All six ORCIDs | VERIFIED | Page 1 |

**Scientific preservation result: VERIFIED.** No scientific content altered between V7 and V8 — only front-matter LaTeX configuration and duplicate References heading removed.

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

### Summary

V8 fixes two defects from V7:
1. **Front-matter column split:** Removed `twocolumn` from document class option and added explicit `\onecolumn` before `\begin{frontmatter}`. Page 1 now renders in clean single column with no overlap between title/authors and abstract text.
2. **Duplicate References heading:** Removed `\section*{References}` since `elsarticle`+`plainnat` already inserts its own References heading via `\bibliography{}`.

Page 1 verification: Title, all 6 authors with ORCIDs, affiliation, corresponding email, abstract (all 4 headings visible), all on page 1 in single column with no overlap. Conclusions paragraph continues to page 2 (acceptable per user guidance). Keywords appear on page 2. Introduction starts on page 3.

**Not submitted. Not uploaded. No DOI minted. No external action taken.**
**Authoritative source files: UNCHANGED**
**Existing backups: UNTOUCHED**
**V2, V3, V4, V5, V6, V7 files: PRESERVED UNCHANGED**
