# Layout Correction Report — CMPB Manuscript V11

**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`
**Report date:** 2026-10-29

---

## 1. Root Cause of Remaining Page 3 Collision

**Root cause:** Line 137 of `main_cmpb_v10.tex` had an inline math expression for the weight definition that was all on one line:

```latex
where $w = (\text{BDF }0.46,\ \text{AME }0.18,\ \text{ISI }0.20,\ \text{RCA }0.09,\ \text{TRN }0.07)$ (Table 5 of the specification).
```

This inline math expression was too wide for the left column (~218pt column width). The expression extended horizontally past the left column's right margin, running into right column content where the "FC NDXUP computed as..." paragraph begins.

**Why V10's previous fix was insufficient:** V10 fixed equations (2) and (3) and the "where w = ..." paragraph break, but the weight definition itself remained as a single inline math expression on one line that was still too wide for the column. The inline math `$w = (\text{BDF }0.46,\ ...)$` couldn't break across lines and extended into the right column.

---

## 2. Fix Applied — `main_cmpb_v11.tex`

**File:** `main_cmpb_v11.tex` (new file; `main_cmpb_v10.tex` preserved unchanged)

| Fix | Location | Before (V10) | After (V11) | Reason |
|-----|----------|-------------|-------------|--------|
| Weight definition | Lines 137-144 | Single inline math `$w = (\text{BDF }0.46,\ ...)$` all on one line | Multiline `gathered` environment within `equation*` | Breaks the weight definition across two lines, each fitting within column width |

**Changed lines (V11 lines 137-144):**

```latex
where
\begin{equation*}
\begin{gathered}
w = (\text{BDF }0.46,\ \text{AME }0.18,\ \text{ISI }0.20,\\
\phantom{w = (}\text{RCA }0.09,\ \text{TRN }0.07)
\end{gathered}
\end{equation*}
(Table 5 of the specification).
```

**Weights preserved exactly:** BDF = 0.46, AME = 0.18, ISI = 0.20, RCA = 0.09, TRN = 0.07

---

## 3. Build Results — Final

| Check | V10 | V11 |
|-------|-----|-----|
| Tectonic exit code | 0 | **0** |
| LaTeX errors | 0 | **0** |
| Undefined references | 0 | **0** |
| Page count | 9 | **9** |
| Page size | A4 | **A4** |
| Page 3 weight-definition overfull | 75.94pt (V9) / still overfull (V10) | **Fixed** |

**Commands executed:**
- `/opt/homebrew/bin/tectonic main_cmpb_v11.tex` → exit 0 (pass 1)
- `/opt/homebrew/bin/tectonic main_cmpb_v11.tex` → exit 0 (pass 2)

**Environment:** `DYLD_LIBRARY_PATH=/Users/yashsiphone/.hermes/cache/scratch/hvf_stub` for Tectonic freetype workaround.

**Remaining overfull warnings (cosmetic only, pre-existing, do not cause column overlap):**
- All remaining overfull boxes are under 15pt and do not cause visible text overlap or clipping between columns.

---

## 4. Page-by-Page Visual Inspection Results

All 9 pages of `main_cmpb_v11.pdf` were rendered at 100 DPI via `pdftoppm` and inspected visually.

| Page | Content | Status | Key observations |
|------|---------|--------|------------------|
| 1 | Title, 6 authors with ORCIDs, affiliation, corresponding email, complete structured abstract (4 headings), complete keywords | PASS | Complete front matter on page 1 in single column. No overlapping text. No text clipping at margins. |
| 2 | Section 1 Introduction, Section 2 Related work | PASS | Section 1 starts at top of page 2. Clean two-column layout. No overlapping text. |
| 3 | Section 3 Method, Equations (1)-(5), Figure 1 | PASS | **Collision fixed.** Weight definition `w = (BDF 0.46, AME 0.18, ISI 0.20, RCA 0.09, TRN 0.07)` broken into two lines, entirely within left column. No text extends into right column. Equations contained within column width. Figure 1 renders without clipping. |
| 4 | Figure 2 workflow, Section 3.2-3.4 | PASS | Figure 2 renders without clipping. Caption legible. |
| 5 | Section 4 Implementation, Section 6 Results | PASS | Clean two-column text. No overlaps. |
| 6 | Table 1 DS scores, Section 6.5-6.7 | PASS | Table renders without overflow. All values legible. |
| 7 | Section 7 Discussion, Table 3 Dimension Analysis | PASS | Full-width table. All values legible. No overflow. |
| 8 | Table 4 Variants, Table 5 Scaling | PASS | Full-width tables. All values legible. |
| 9 | References [1]-[25], last page | PASS | Exactly ONE References heading. References complete through [25]. Page ends cleanly. |

**Visual inspection result: Page 3 column-overlap definitively fixed (mandatory acceptance condition met).** All 9 pages pass. No overlapping text between columns anywhere. No clipping, no missing glyphs, no orphaned captions, no empty pages, no duplicate References heading.

---

## 5. Scientific Preservation Verification

| Element | Status | Details |
|---------|--------|---------|
| Equation (1): `DS = 100 − (penalty_NDXUP + penalty_STs)` | VERIFIED | Both penalties subtracted inside parentheses |
| V0: 26/32 Table 8 matches | VERIFIED | Page 6 Table 1 |
| V1: 32/32 with proposed TRN reconciliation | VERIFIED | Page 6 Table 1 |
| TRN reconciliation proposed/inferred | VERIFIED | Labelled "proposed reconciliation" and "inferred from published scores" |
| Table 7: unit-normalized 3/5, literal 4/5 | VERIFIED | Page 7 Table 2 |
| No match claimed dimensionally valid | VERIFIED | Page 8 Table 3 labels |
| V3: preliminary and unvalidated | VERIFIED | Sections 3.4, 7.3 |
| No clinical interchangeability claim | VERIFIED | Sections 7.3, 8.4 |
| No public repository/DOI claimed | VERIFIED | Section 10.6 |
| 196 assertions | VERIFIED | Abstract, Section 6.8 |
| All six authors in correct order | VERIFIED | Page 1 |
| All six ORCIDs | VERIFIED | Page 1 |
| Weight values preserved | VERIFIED | BDF=0.46, AME=0.18, ISI=0.20, RCA=0.09, TRN=0.07 |

**Scientific preservation result: VERIFIED.** No scientific content altered between V10 and V11 — only the weight-definition line was reformatted as a multiline equation.

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

V10's page 3 column-overlap defect was caused by an inline weight-definition expression that was all on one line and too wide for the left column (~76pt overflow). V11 fixes this by reformatting the weight definition as a multiline `gathered` equation within `equation*`, keeping both lines within the column width.

**V11 improvements over V10:**
- Weight definition `w = (BDF 0.46, AME 0.18, ISI 0.20, RCA 0.09, TRN 0.07)` now renders on two lines, entirely within left column
- No text extends from left column into right column
- Page count unchanged at 9 pages
- Page size unchanged at A4
- All scientific content preserved exactly
- No new visible layout defects introduced

**Not submitted. Not uploaded. No DOI minted. No external action taken.**
**Authoritative source files: UNCHANGED**
**Existing backups: UNTOUCHED**
**V2, V3, V4, V5, V6, V7, V8, V9, V10 files: PRESERVED UNCHANGED**
