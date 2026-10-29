# Zenodo Release Procedure for CMPB Manuscript

## Status
- GitHub repository created: https://github.com/yashmahajan11234567/cmpb-medicine-substitution-scoring
- Release tag `v1.0.0` pushed
- Ready for Zenodo archival

## Required User Action (cannot be automated)

**You must complete these steps to obtain a real DOI:**

1. **Go to Zenodo GitHub Integration:**
   - Open https://zenodo.org/account/settings/github/
   - Log in with your GitHub account (yashmahajan11234567)

2. **Enable the Repository:**
   - Find `cmpb-medicine-substitution-scoring` in the repository list
   - Toggle the switch **ON** for this repository
   - This enables automatic archival on every GitHub release

3. **Trigger Archival:**
   - Since release `v1.0.0` already exists, Zenodo may not auto-archive it
   - **Option A:** Create a new release on GitHub (e.g., `v1.0.1`) — Zenodo will archive it
   - **Option B:** On Zenodo, go to "Upload" → "New Upload" → "Import from GitHub" → select the repo and tag `v1.0.0`

4. **Verify DOI:**
   - After archival, Zenodo will display a DOI (format: `10.5281/zenodo.XXXXXXX`)
   - Verify the DOI resolves at `https://doi.org/10.5281/zenodo.XXXXXXX`
   - Confirm the archived files match the GitHub release

5. **Update Manuscript:**
   - Once DOI is confirmed, update `main_cmpb_v13.tex` line ~443:
     ```latex
     The repository and persistent identifier are not yet available.
     ```
     to:
     ```latex
     Code and data available at https://github.com/yashmahajan11234567/cmpb-medicine-substitution-scoring (DOI: 10.5281/zenodo.XXXXXXX).
     ```
   - Rebuild `main_cmpb_v13_final.pdf` and verify

## Files Included in Release

All verified artifacts:
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

## Verification Before Submission

Run these to confirm everything works:
```bash
python code/test_caviglioli.py          # 196/196 pass
python reproduce_all.py                  # All tables/figures reproduced
```

## Blocker

**Only you can authorize the Zenodo-GitHub connection** — this requires your GitHub login on Zenodo. Once connected, the DOI will be real and verifiable. Until then, the manuscript's availability statement must remain "not yet available."