# CMPB Medicine Substitution-Scoring Algorithm

**Transparent Implementation and Verification of a Medicine Substitution-Scoring Algorithm: Deterministic Scoring and Unit-Consistent Dose Handling**

This repository contains the complete computational artifacts for the manuscript submitted to *Computer Methods and Programs in Biomedicine* (CMPB).

## Contents

| Directory/File | Description |
|---|---|
| `main_cmpb_v13.tex` | Final manuscript source (LaTeX, 9 pages A4) |
| `main_cmpb_v13_final.pdf` | Compiled manuscript PDF |
| `main_cmpb_v12.tex` / `.pdf` | Protected baseline (V12) |
| `code/ds_algorithm.py` | Core DS algorithm implementation |
| `code/reproduce_published.py` | Reproduction functions for Tables 4, 6, 7, 8 and ranking |
| `code/discrepancy_analysis.py` | Structural discrepancy analysis + TRN reconciliation search |
| `code/test_caviglioli.py` | 196-assertion correctness test suite |
| `data/published_tables.json` | All published labelled data (Tables 4, 6, 7, 8) |
| `reproduce_all.py` | Single-command reproduction entry point |
| `figures/ds_formula.tex` | Figure 1: DS decomposition (TikZ) |
| `figures/workflow.tex` | Figure 2: Scoring workflow (TikZ) |
| `references.bib` | Bibliography |
| `CHANGELOG_V13.md` | Detailed change log |
| `FINAL_VISUAL_AUDIT_V13.md` | Visual audit report |
| `DEFECT_REGISTER_V13.md` | Defect register |

## Quick Start

```bash
# Run all 196 correctness assertions
python code/test_caviglioli.py

# Reproduce all manuscript tables and figures
python reproduce_all.py
```

Expected output:
```
Caviglioli correctness suite: 196/196 assertions passed

TABLE 8: V0 (strict) 26/32 → V1 (reconciled) 32/32 match
TABLE 7: 5/5 reproducible by some convention (3/5 unit-aware, 4/5 literal)
Ranking: published order reproduced exactly
All 196 assertions pass
```

## Algorithm Summary

The Degree of Substitutability (DS) score:
```
DS = 100 − (penalty_NDXUP + penalty_STs)
```

Where:
- `penalty_NDXUP` ∈ {0,2,4,6,8,10} from Table 4
- `penalty_STs` = Σ NRD_st × w_st × 80/100 over 5 EDQM Standard Terms
- Weights: BDF 0.46, AME 0.18, ISI 0.20, RCA 0.09, TRN 0.07

## Scoring Modes

| Mode | Description | Table 8 Match |
|---|---|---|
| **V0-strict-baseline** | Specification exactly as printed | 26/32 |
| **V1-publication-compatible** | V0 + TRN row transposition (TRA-0039/0040) inferred from published scores | 32/32 |
| **V2-unit-literal-fc** | V1 + literal Equation 4 division | 32/32 (Table 8 unaffected) |
| **V3-medi-gen-fc-composite** | FC composite extension (unvalidated) | N/A |

## Table 7 Unit Conventions

No single convention reproduces all 5 published NDXUP sums:
- **Unit-aware** (convert to mg): 3/5 match (rows A, C, D)
- **Literal** (divide printed numbers): 4/5 match (rows A, B, D, E)
- **Any convention**: 5/5 (every row matches at least one)

## Requirements

- Python ≥ 3.10 (tested on 3.14)
- No external dependencies (stdlib only)

## License

MIT License — see [LICENSE](LICENSE) for details.

## Citation

```bibtex
@article{cmpb2025medsub,
  title={Transparent Implementation and Verification of a Medicine Substitution-Scoring Algorithm: Deterministic Scoring and Unit-Consistent Dose Handling},
  author={Jiman, Ajinkya and Rajeswari, K. and Warkad, Ruturaj and Painjane, Vivek and Mahajan, Yash and Wankhade, Aryan},
  journal={Computer Methods and Programs in Biomedicine},
  year={2025},
  note={Submitted}
}
```

## Data Provenance

All labelled data originates from Caviglioli et al. (2025) published tables:
- Table 4: NDXUP penalty ladder (public specification)
- Table 6: Fictitious ATC rule examples (5 rows)
- Table 7: FC NDXUP sums (5 rows)
- Table 8: 32 risperidone products with published DS scores

The proprietary Farmadati Italia + AIFA shortage list test set was not released and cannot be recomputed.

## Verification

All numbers in the manuscript are traceable to the JSON artifacts produced by the code. Run `python reproduce_all.py` to verify independently.