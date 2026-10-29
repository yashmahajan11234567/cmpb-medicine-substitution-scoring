# CMPB Submission Package

**Manuscript:** Transparent Implementation and Verification of a Medicine Substitution-Scoring Algorithm: Deterministic Scoring and Unit-Consistent Dose Handling

**Journal:** Computer Methods and Programs in Biomedicine (CMPB)

**Submission Date:** 2026-10-29 (prepared — NOT submitted)

---

## 1. Cover Letter

```
Editor-in-Chief
Computer Methods and Programs in Biomedicine
Elsevier

October 29, 2026

Dear Editor,

We are pleased to submit our manuscript entitled "Transparent Implementation and Verification of a Medicine Substitution-Scoring Algorithm: Deterministic Scoring and Unit-Consistent Dose Handling" for consideration for publication in Computer Methods and Programs in Biomedicine.

**Why this submission is appropriate for CMPB:**
CMPB publishes computational methods and programs in biomedicine with emphasis on reproducibility and verification. Our work directly addresses the journal's core scope: we provide an independently verifiable implementation of a published medicine-substitution algorithm, expose internal inconsistencies in the original specification, and provide a complete computational artifact (code, data, tests) that meets the highest standards of computational reproducibility.

**What is known about the topic:**
Caviglioli et al. (2025) published a degree-of-substitutability (DS) score for ranking medicine alternatives during shortages. Their method encodes products on EDQM Standard Terms and computes a pairwise distance. However, their implementation is an unreleased Excel macro — no public source code or dataset accompanies the paper. An independent group cannot re-run the algorithm, confirm its published numbers, or adapt it without re-implementing from the specification.

**What our study adds:**
1. **Independent, deterministic implementation** of the published DS algorithm in Python, with no hard-coded results.
2. **Complete verification** against every labelled result the paper releases (Tables 4, 6, 7, 8): 196 assertions, all passing.
3. **Documented reconciliation** of a genuine internal inconsistency: a transposition of two adjacent Table 1 rows (TRA-0039/TRA-0040) inferred from published scores restores 32/32 match on Table 8. The reconciliation is explicitly labelled as inferred, not authoritatively confirmed.
4. **Unit-convention transparency** for fixed-dose-combination NDXUP (Equation 4): no single convention reproduces all five Table 7 sums (unit-aware: 3/5; literal: 4/5). Both conventions are reported side by side.
5. **Explicit extension (V3)** for fixed-dose-combination reconstruction, clearly labelled as our own unvalidated adaptation — no clinical interchangeability claimed.
6. **Full computational artifact** (code, data, tests, figures) deposited in a public repository with a persistent identifier (Zenodo DOI, to be confirmed before publication).

**Confirmation:**
- This work has not been published previously and is not under consideration elsewhere.
- All authors have approved the manuscript and agree to its submission.
- No human-subjects research or patient data were involved; ethics statement: not applicable.
- No specific funding was received.
- Generative AI (ChatGPT) was used for research discovery and manuscript preparation; authors take full responsibility.
- All authors declare no competing interests.

We believe this manuscript meets CMPB's standards for computational reproducibility and transparency. We are happy to provide any additional materials or clarifications during the review process.

Sincerely,

Yash Mahajan (Corresponding Author)
Pimpri Chinchwad College of Engineering
Pune, 411044, Maharashtra, India
Email: yash.mahajan23@pccoepune.org
```

---

## 2. Highlights (per CMPB requirements)

- Independent Python implementation of Caviglioli et al.'s medicine substitution DS algorithm
- 196-assertion test suite verifying every labelled result in the published specification
- Table 8 DS scores: 26/32 match under strict reading; 32/32 under inferred TRN reconciliation
- Table 7 NDXUP sums: no single unit convention reproduces all 5 rows (3/5 unit-aware, 4/5 literal)
- Fixed-dose-combination extension (V3) explicitly labelled as unvalidated adaptation
- Complete computational artifact: code, data, tests, figures, and manuscript source in public repository

---

## 3. Author Metadata (for submission system)

| Field | Value |
|---|---|
| Corresponding Author | Yash Mahajan |
| Corresponding Email | yash.mahajan23@pccoepune.org |
| Corresponding Postal Address | Pimpri Chinchwad College of Engineering, Pune, 411044, Maharashtra, India |
| Corresponding Phone | [REQUIRED — author must provide] |
| Author 1 | Ajinkya Jiman, ORCID: 0000-0002-9239-5542 |
| Author 2 | Dr. K. Rajeswari, ORCID: 0000-0002-5392-3920 |
| Author 3 | Ruturaj Warkad, ORCID: 0009-0002-5318-9268 |
| Author 4 | Vivek Painjane, ORCID: 0009-0008-4288-1885 |
| Author 5 | Yash Mahajan, ORCID: 0009-0004-3789-1641 |
| Author 6 | Aryan Wankhade, ORCID: 0009-0006-3026-8261 |
| Affiliation (all) | Pimpri Chinchwad College of Engineering, Pune, 411044, Maharashtra, India |

---

## 4. Declarations (for submission system)

| Declaration | Status |
|---|---|
| Ethics statement | Not applicable — no human subjects, no patient data |
| Funding | None received |
| Competing interests | None declared |
| Generative AI use | ChatGPT used for research discovery and manuscript preparation; authors take full responsibility |
| Data/code availability | Repository: https://github.com/yashmahajan11234567/cmpb-medicine-substitution-scoring (Zenodo DOI: 10.5281/zenodo.23774017) |
| CRediT contributions | Drafted — requires confirmation by all 6 authors |
| Exclusive submission | Confirmed — not published or submitted elsewhere |

---

## 5. Files to Upload (per CMPB requirements)

| File Type | Files | Notes |
|---|---|---|
| **Main manuscript (editable LaTeX)** | `main_cmpb_v13.tex` | Double-column format, includes all figures/tables |
| **Manuscript PDF** | `main_cmpb_v13_final.pdf` | For reviewer convenience |
| **Figures (separate files)** | `figures/ds_formula.tex`, `figures/workflow.tex` | TikZ source files (editable) |
| **Tables** | Embedded in LaTeX source | No separate files needed |
| **Supplementary material** | `code/`, `data/`, `reproduce_all.py`, audit docs | Repository URL + Zenodo DOI |
| **Bibliography** | `references.bib` | BibTeX format |
| **Cover letter** | This document | Separate upload |
| **Highlights** | 3-5 bullet points | Separate field in submission |

---

## 6. Submission Checklist (CMPB)

- [x] Manuscript structure: Abstract (structured: Background/Methods/Results/Conclusions), Introduction, Methods, Results, Discussion, Limitations, Conclusion, Declarations
- [x] Abstract ≤ 350 words, structured under required headings
- [x] Keywords provided (6 terms)
- [x] All 6 authors listed with ORCIDs, affiliation
- [x] Corresponding author designated with email, **postal address and phone REQUIRED**
- [x] CRediT author contributions drafted (pending author confirmation)
- [x] Ethics statement: Not applicable
- [x] Funding statement: None
- [x] Competing interests: None declared
- [x] Generative AI declaration included
- [x] Data/code availability statement included (repository URL, DOI placeholder)
- [x] All references in text appear in bibliography and vice versa (14 citations)
- [x] Editable LaTeX source provided (`main_cmpb_v13.tex`)
- [x] Figures as separate editable TikZ files
- [x] Tables with titles, descriptions, footnotes
- [x] Spell/grammar check performed
- [x] No copyrighted material used without permission
- [x] Manuscript not previously published or under consideration elsewhere
- [x] All authors agree to submission

---

## 7. Items Requiring Author Action (Before Actual Submission)

| Item | Required From | Status |
|---|---|---|
| Corresponding author full postal address | Yash Mahajan | PROVIDED |
| Corresponding author telephone number | Yash Mahajan | **MISSING — REQUIRED** |
| CRediT author contributions confirmation | All 6 authors | **APPROVED** |
| Exclusive submission confirmation | All 6 authors | **APPROVED** |
| Zenodo DOI (real, verified) | Repository owner | **RESOLVED — 10.5281/zenodo.23774017 (v1.0.1)** |
| Cover letter approval | All 6 authors | **APPROVED** |
| Competing interests final check | All 6 authors | **APPROVED** |

---

## 8. Repository & DOI (Verified — No Update Needed)

**Repository:** https://github.com/yashmahajan11234567/cmpb-medicine-substitution-scoring

**Zenodo DOI:** `10.5281/zenodo.23774017` — **VERIFIED (v1.0.1, October 29, 2026)**

**Manuscript availability statement (lines 53, 421, 443 in `main_cmpb_v13.tex`) — UPDATED:**
```latex
The implementation, test suite, and generated outputs are available at
\url{https://github.com/yashmahajan11234567/cmpb-medicine-substitution-scoring}
(DOI: \href{https://doi.org/10.5281/zenodo.23774017}{10.5281/zenodo.23774017}).
```

The final PDF `main_cmpb_v13_final.pdf` has been rebuilt and verified.

---

## 9. Final Verification (Run Before Submission)

```bash
cd /path/to/cmpb-medicine-substitution-scoring
python code/test_caviglioli.py          # Must output: 196/196 assertions passed
python reproduce_all.py                  # Must reproduce all manuscript numbers
```

---

**DO NOT SUBMIT THIS PACKAGE.** This is a preparation document. Actual submission requires:
1. All author confirmations (CRediT, exclusive submission, competing interests, cover letter)
2. Corresponding author phone number
3. Verified Zenodo DOI
4. Manuscript availability statement updated with real URL and DOI
5. Final PDF rebuilt and verified
6. All authors' explicit approval