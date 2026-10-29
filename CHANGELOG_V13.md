# Change Log — CMPB V13 Layout Corrections

**Source file:** `main_cmpb_v13.tex`
**Working directory:** `/Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/`

---

## Changes Made

### 1. Line 185 — NDXUP distance factor expression (Issue D2)
**Before:**
```latex
\item An \textbf{NDXUP distance factor} $1 - \text{penalty}_{\text{NDXUP}}/10$ \\
applied to the reconstructed combination.
```

**After:**
```latex
\item An \textbf{NDXUP distance factor} \linebreak[4]\mbox{$1 - \text{penalty}_{\hbox{NDXUP}}/10$} applied to the reconstructed combination.
```

**Reason:** The inline math expression crossed the column boundary. `\linebreak[4]` forces a line break before the expression; `\mbox{}` keeps the entire expression unbreakable; `\hbox{NDXUP}` prevents subscript hyphenation.

---

### 2. Line 197 — Inline code path (Issue D)
**Before:**
```latex
The implementation is contained in `code/ds\_algorithm.py` and provides:
```

**After:**
```latex
The implementation is contained in \texttt{code/}\allowbreak\texttt{ds\_algorithm.py} and provides:
```

**Reason:** The backtick-formatted path `code/ds_algorithm.py` overflowed into the right column. `\texttt{}` with `\allowbreak` after `code/` allows a clean break at the directory separator.

---

### 3. Lines 203–210, 383–385 — All inline code identifiers (Issue F)
**Before:** Backtick formatting for `ds_components()`, `find_substitutes()`, `fc_ndxup_units()`, `fictitious_fc_atc()`, `validation_indicators()`, `KeyError`, `find_substitutes`, `code/test_caviglioli.py`, and `find_substitutes` in section 6.8.

**After:** All changed to `\texttt{...}` with proper underscore escaping. The long identifier `find_substitutes` overflowed the right margin when placed at line end. Fixed at three locations:
- Line 204: `\texttt{find\_substitutes}()` — kept intact on its own line via `\sloppy` paragraph wrapping
- Line 210: `\texttt{find\_substitutes()}` — kept intact via `\sloppy` paragraph wrapping  
- Line 383: Restructured sentence to place identifier earlier: "ordering by \mbox{\texttt{find\_substitutes}}" instead of "and \mbox{\texttt{find\_substitutes}} ordering" — keeps identifier intact and avoids end-of-line overflow

**Reason:** Backtick formatting doesn't allow line breaks; `\texttt{}` with proper escaping allows TeX to break at appropriate points while keeping monospace formatting. `\mbox{}` keeps the identifier as one unbreakable unit. Restructuring line 383 avoids placing a long unbreakable box at the end of a line where it would overflow.

---

### 4. Line 287 — Section 6.5 heading (Issue E)
**Before:**
```latex
\subsection{Table 7: fixed-dose-combination NDXUP sums}
```

**After:**
```latex
\subsection{Table 7: fixed-dose-combination\\ NDXUP sums}
```

**Reason:** The heading "fixed-dose-combination NDXUP sums" extended into the right column. The explicit `\\` forces a line break after "fixed-dose-combination".

---

### 5. Line 421 — Conclusion "substitution-scoring" (Issue F2)
**Before:**
```latex
We implemented Caviglioli et al.\citep{caviglioli2025medicine}'s medicine substitution-scoring algorithm...
```

**After:**
```latex
We implemented Caviglioli et al.\citep{caviglioli2025medicine}'s medicine \linebreak[4]\mbox{substitution-scoring} algorithm...
```

**Reason:** The word "substitution-scoring" was hyphenated across the column boundary. `\linebreak[4]` forces a break before it; `\mbox{}` prevents hyphenation.

---

### 6. Line 438 — CRediT author contributions (Issue E2)
**Before:**
```latex
Ajinkya Jiman and Dr.\ K.\ Rajeswari: mentorship, research guidance. Ruturaj Warkad, Vivek Painjane, Yash Mahajan, Aryan Wankhade: algorithm implementation, reproduction, discrepancy analysis, benchmarking, manuscript preparation. Author contribution statement to be confirmed by all authors; the mentor/developer distinction stated above reflects the division of labour described in this manuscript.
```

**After:**
```latex
Ajinkya Jiman and Dr.\ K.\ Rajeswari: mentorship, research guidance.
Ruturaj Warkad, Vivek Painjane, Yash Mahajan, Aryan Wankhade: algorithm implementation, reproduction, discrepancy analysis, benchmarking, manuscript preparation.
Author contribution statement to be confirmed by all authors; the mentor/developer distinction stated above reflects the division of labour described in this manuscript.
```

**Reason:** The single long paragraph was cramped in the right column. Splitting into three paragraphs improves readability and prevents overflow.

---

### 7. Figure 2 workflow diagram (Issue F3)
**File:** `figures/workflow.tex`

**Before:** Embedded title inside TikZ diagram:
```latex
% Title
\node[font=\bfseries\small, align=center, text width=9cm] at (current bounding box.north)
    {Figure~2: Scoring workflow of the implemented method\\ deterministic substitution ranking};
```

**After:** Removed embedded title; added top padding for LaTeX caption clearance:
```latex
% Add extra space at top for LaTeX caption clearance
\path (current bounding box.north) -- ++(0,0.8cm);
```

**Reason:** The embedded title duplicated the LaTeX figure caption and overlapped the top row of workflow nodes. The LaTeX `\caption` below the figure already provides the proper title. Added 8mm top padding so the caption has room.

---

### 8. Line 310 — Gentamycin paragraph transition (Issue G)
**Before:** Lowercase `while` started a new paragraph after the preceding sentence ended with a closing parenthesis.

**After:** `while` merged into the same sentence as the preceding clause.

**Reason:** Accidental paragraph break made `while` appear as the start of a standalone sentence after a period, which is grammatically incorrect. Merged into a single sentence with proper comma separation. No scientific content changed.

---

---

### 8 (new). Line 112 — Equation (1) parentheses (Issue H)

**Before:**
```latex
\text{DS} = 100 - \bigl(\text{penalty}_{\text{NDXUP}} + \text{penalty}_{\text{STs}}\bigr)
```

**After:**
```latex
\text{DS} = 100 - (\text{penalty}_{\text{NDXUP}} + \text{penalty}_{\text{STs}})
```

**Reason:** The `\bigl(` and `\bigr)` delimiters failed to render as parentheses in the compiled PDF. The equation appeared as `DS = 100 − penaltyNDXUP + penaltySTs` without grouping parentheses — a scientific correctness defect since DS is defined as `100 − (penalty_NDXUP + penalty_STs)`, not `100 − penalty_NDXUP + penalty_STs`. Changed to plain `(`/`)` which render reliably.

---

### 9 (new). Lines 204, 210, 383 — find_substitutes() parentheses and protection (Issue I)

**Before:** Two occurrences of `find_substitutes()` lacked parentheses; one occurrence was not wrapped in `\mbox{}` (line 210); one occurrence in section 6.8 was missing parentheses (line 383).

**After:** All three occurrences now render as `find_substitutes()` with parentheses, each protected by `\mbox{}` to prevent line-break splitting.

**Reason:** The identifier was visually splitting across lines as `find_sub` / `stitutes()` in PDF text extraction. Wrapping each in `\mbox{}` keeps it on one line; adding parentheses preserves the function-call notation.

---

### 10 (new). Lines 306, 308 — Gentamycin paragraph "while" clauses (Issue J)

**Before:** The word `while` appeared mid-sentence without a non-breaking space before it, potentially causing it to start a new visual line at column boundaries in the two-column layout.

**After:** Added non-breaking spaces (`~`) before both `while` clauses: `numerically~while mixing` and `not 45,~while mixing`.

**Reason:** Prevents `while` from appearing at the start of a new visual line where it could be mistaken for the start of a new paragraph. No scientific content changed.

## Files Modified

- `main_cmpb_v13.tex` — all changes above
- `figures/workflow.tex` — removed embedded title, added top padding
- `main_cmpb_v13_final.pdf` — compiled output (copy of `main_cmpb_v13.pdf`)

---

## Files Preserved (Unchanged)

- `main_cmpb_v12.tex` and `main_cmpb_v12.pdf`
- `main_cmpb_v11.tex` through `main_cmpb_v2.tex` and corresponding PDFs
- `main_cmpb.tex`, `main.tex`, `references.bib`
- `figures/ds_formula.tex`
- All backup directories