# Zenodo Release Procedure for CMPB Manuscript — COMPLETED

## Status: ✅ ARCHIVED AND VERIFIED

- GitHub repository: https://github.com/yashmahajan11234567/cmpb-medicine-substitution-scoring
- GitHub release: `v1.0.1` (published October 29, 2026, 18:10:14 UTC)
- Zenodo record: https://zenodo.org/records/23774017
- **Verified DOI:** `10.5281/zenodo.23774017` (version-specific, not concept DOI)
- Manuscript availability statement: **UPDATED** in all 3 locations (abstract, conclusion, data/code availability)

---

## What Was Done (Manual Steps Completed)

1. **Enabled GitHub-Zenodo integration** at https://zenodo.org/account/settings/github/
2. **Created GitHub release `v1.0.1`** — Zenodo automatically archived it
3. **Verified DOI resolves** at https://doi.org/10.5281/zenodo.23774017
4. **Confirmed archived files match** the GitHub release `v1.0.1`
5. **Updated manuscript** `main_cmpb_v13.tex` at 3 locations with verified URL + DOI
6. **Rebuilt `main_cmpb_v13_final.pdf`** — verified 9 pages, all content intact

---

## DOI Details

| Property | Value |
|---|---|
| **DOI** | `10.5281/zenodo.23774017` |
| **Type** | Version-specific DOI (archives `v1.0.1` exactly) |
| **Concept DOI** | `10.5281/zenodo.23774016` (resolves to latest version) |
| **Zenodo URL** | https://zenodo.org/records/23774017 |
| **Title** | "Transparent Implementation and Verification of a Medicine Substitution-Scoring Algorithm: Deterministic Scoring and Unit-Consistent Dose Handling" |
| **Version** | v1.0.1 |
| **Published** | October 29, 2026 |

**Manuscript cites the version-specific DOI** (`10.5281/zenodo.23774017`), which correctly identifies the exact archived artifacts described in the paper.

---

## Files Included in Release `v1.0.1`

All verified artifacts (1.7 MB zip):
- `main_cmpb_v13.tex` / `main_cmpb_v13_final.pdf` (final manuscript)
- `main_cmpb_v12.tex` / `main_cmpb_v12.pdf` (protected baseline)
- `code/ds_algorithm.py` (core implementation)
- `code/reproduce_published.py` (table/figure reproduction)
- `code/discrepancy_analysis.py` (discrepancy analysis)
- `code/test_caviglioli.py` (196-assertion test suite)
- `data/published_tables.json` (Tables 4, 6, 7, 8 labelled data)
- `reproduce_all.py` (single-command verification)
- `figures/ds_formula.tex`, `figures/workflow.tex` (TikZ figures)
- `references.bib` (bibliography)
- `README.md`, `LICENSE`, `CITATION.cff`, `pyproject.toml`
- Audit documents: `FINAL_VISUAL_AUDIT_V13.md`, `CHANGELOG_V13.md`, `DEFECT_REGISTER_V13.md`

---

## Verification (Run Before Submission)

```bash
cd /Volumes/HP USB20FD/medigen-research/paper_caviglioli_2025/cmpb_format_work_2026-10-28/
python code/test_caviglioli.py          # 196/196 pass
python reproduce_all.py                  # All tables/figures reproduced
```

---

## No Further Action Required for Zenodo

The DOI is real, verified, and correctly cited in the manuscript. The manuscript does **not** need to be byte-for-byte identical to the archived source — the availability statement accurately describes what is available in the public repository and the versioned Zenodo archive.