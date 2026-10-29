#!/usr/bin/env python3
"""Correctness tests for the Caviglioli et al. (2025) reproduction.

Run:  python code/test_caviglioli.py

Every assertion is checkable against the published paper:

  * the printed worked example (Section 3.2 / Table 5 area),
  * the Table 4 penalty ladder,
  * the Table 6 fictitious-ATC rule,
  * the Table 7 NDXUP sums (Equation 4),
  * the Table 8 DS scores and the published ranking order,
  * internal consistency of the scoring function.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reproduce_published as rp  # noqa: E402
from ds_algorithm import (DS_EQUIVALENT, FC_UNIT_AWARE, FC_UNIT_LITERAL,  # noqa: E402
                           MAX_NDXUP_PENALTY, MAX_ST_PENALTY, MODE_PUB_COMPAT,
                           MODE_STRICT, ST_MAX_DIFF, ST_RP, ST_WEIGHTS,
                           ds_components, ds_score, fictitious_fc_atc,
                           fc_ndxup, fc_ndxup_units, find_substitutes, nrd,
                           penalty_ndxup, rp_of, validation_indicators)

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(condition), detail))


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------
# 1. Weights and constants
# ---------------------------------------------------------------------------
def test_constants() -> None:
    check("weights sum to 1",
          close(sum(ST_WEIGHTS.values()), 1.0),
          f"sum={sum(ST_WEIGHTS.values())}")
    check("published weights BDF/AME/ISI/RCA/TRN",
          ST_WEIGHTS["BDF"] == 0.46 and ST_WEIGHTS["AME"] == 0.18
          and ST_WEIGHTS["ISI"] == 0.20 and ST_WEIGHTS["RCA"] == 0.09
          and ST_WEIGHTS["TRN"] == 0.07,
          str(ST_WEIGHTS))
    check("maximum penalties are 10 and 80",
          MAX_NDXUP_PENALTY == 10.0 and MAX_ST_PENALTY == 80.0)
    check("equivalent threshold is 100", DS_EQUIVALENT == 100.0)
    for st, scale in ST_RP.items():
        mx = max(scale.values())
        mn = min(scale.values())
        check(f"{st} max difference matches the scale span",
              close(ST_MAX_DIFF[st], mx - mn),
              f"declared={ST_MAX_DIFF[st]} span={mx - mn}")


# ---------------------------------------------------------------------------
# 2. Table 4 penalty ladder
# ---------------------------------------------------------------------------
def test_penalty_ladder() -> None:
    res = rp.check_penalty_ladder()
    check("Table 4 penalty ladder reproduces all branches",
          res["n_matching"] == res["n"],
          f"{res['n_matching']}/{res['n']}")
    # direct spot checks of the printed ladder
    check("equal NDXUP -> no penalty", penalty_ndxup(1.0, 1.0) == 0.0)
    check("half NDXUP -> penalty 2", penalty_ndxup(1.0, 0.5) == 2.0)
    check("double NDXUP -> penalty 4", penalty_ndxup(1.0, 2.0) == 4.0)
    check("between 1x and 2x -> penalty 8", penalty_ndxup(1.0, 1.5) == 8.0)
    check("below half -> penalty 10", penalty_ndxup(1.0, 0.2) == 10.0)
    check("above double -> penalty 10", penalty_ndxup(1.0, 5.0) == 10.0)
    # the printed Table 4 ladder, branch by branch
    ladder = {
        1.0: 0.0,    # equal
        0.5: 2.0,    # 0.5 * NDXUP_lak
        2.0: 4.0,    # 2 * NDXUP_lak
        0.75: 6.0,   # 0.5x < sub < 1x
        1.5: 8.0,    # 1x < sub < 2x
        0.2: 10.0,   # sub < 0.5x
        5.0: 10.0,   # sub > 2x
    }
    for sub, expected in ladder.items():
        check(f"penalty ladder: NDXUP_sub={sub} -> {expected}",
              penalty_ndxup(1.0, sub) == expected,
              f"{penalty_ndxup(1.0, sub)}")
    check("the ladder is symmetric in the 0.5x / 2x branches",
          penalty_ndxup(1.0, 0.5) == 2.0 and penalty_ndxup(1.0, 2.0) == 4.0)


# ---------------------------------------------------------------------------
# 3. Published worked example (Section 3.2)
# ---------------------------------------------------------------------------
def test_worked_example() -> None:
    res = rp.check_worked_example()
    check("worked example NRD reproduces 41.30",
          close(res["nrd_reproduced"], 41.30, 0.01),
          f"{res['nrd_reproduced']}")
    check("worked example weighted contribution reproduces 18.998",
          close(res["weighed_reproduced"], 18.998, 0.005),
          f"{res['weighed_reproduced']}")


# ---------------------------------------------------------------------------
# 4. NRD definition
# ---------------------------------------------------------------------------
def test_nrd() -> None:
    # identical positions -> 0
    check("NRD of identical positions is 0", close(nrd("BDF", 1.0, 1.0), 0.0))
    # full span -> 100
    for st in ST_RP:
        lo = min(ST_RP[st].values())
        hi = max(ST_RP[st].values())
        check(f"NRD across the full {st} span is 100",
              close(nrd(st, lo, hi), 100.0, 1e-6))
    # symmetry
    check("NRD is symmetric",
          close(nrd("AME", 2.0, 7.0), nrd("AME", 7.0, 2.0)))


# ---------------------------------------------------------------------------
# 5. Table 6 fictitious ATC codes
# ---------------------------------------------------------------------------
def test_fictitious_codes() -> None:
    res = rp.check_table6()
    check("Table 6 fictitious-ATC rule satisfied for every row",
          res["n_rule_satisfied"] == res["n"],
          f"{res['n_rule_satisfied']}/{res['n']}")
    # the rule itself: keep the 4th level, pick an unused 5th level in 99..80
    check("fictitious code keeps the 4th-level stem",
          fictitious_fc_atc("N05AX").startswith("N05AX"),
          fictitious_fc_atc("N05AX"))
    check("fictitious code picks the highest free 5th level (99)",
          fictitious_fc_atc("N05AX") == "N05AX99",
          fictitious_fc_atc("N05AX"))
    check("fictitious code skips a taken 5th level",
          fictitious_fc_atc("N05AX", taken=[99]) == "N05AX98",
          fictitious_fc_atc("N05AX", taken=[99]))
    check("fictitious code falls back to a letter+digit when 99..80 are taken",
          fictitious_fc_atc("N05AX", taken=list(range(80, 100))) == "N05AXA0",
          fictitious_fc_atc("N05AX", taken=list(range(80, 100))))
    check("every generated 5th level is inside the printed 99..80 range",
          all(80 <= int(fictitious_fc_atc("N05AX", taken=list(range(80, t)))[5:])
              <= 99 for t in range(80, 100)))
    check("fictitious codes are unique for distinct taken sets",
          fictitious_fc_atc("N05AX", taken=[99])
          != fictitious_fc_atc("N05AX", taken=[99, 98]))


# ---------------------------------------------------------------------------
# 6. Equation 4 and Table 7
# ---------------------------------------------------------------------------
def test_equation4() -> None:
    check("Equation 4 sums the per-API ratios",
          close(fc_ndxup([(10.0, 10.0), (10.0, 10.0)]), 2.0))
    check("Equation 4 is unit-agnostic when the numbers match",
          close(fc_ndxup([(0.5, 1.0), (0.25, 1.0)]), 0.75))
    # unit conventions
    comp = [(30.0, "mg", 1.0, "g"), (30.0, "mg", 2.0, "g")]
    check("unit-aware NDXUP converts mg against g",
          close(fc_ndxup_units(comp, FC_UNIT_AWARE), 0.045),
          f"{fc_ndxup_units(comp, FC_UNIT_AWARE)}")
    check("literal NDXUP divides the printed numbers",
          close(fc_ndxup_units(comp, FC_UNIT_LITERAL), 45.0),
          f"{fc_ndxup_units(comp, FC_UNIT_LITERAL)}")
    # a tablet DDD cannot be mass-converted
    tab = [(0.15, "mg", 1.0, "tab"), (0.03, "mg", 25.0, "mcg")]
    check("unit-aware leaves a tablet DDD as printed",
          close(fc_ndxup_units(tab, FC_UNIT_AWARE), 0.15 + 1.2, 1e-9),
          f"{fc_ndxup_units(tab, FC_UNIT_AWARE)}")
    check("literal reproduces the published desogestrel row",
          close(fc_ndxup_units(tab, FC_UNIT_LITERAL), 0.1512, 1e-9),
          f"{fc_ndxup_units(tab, FC_UNIT_LITERAL)}")

    res = rp.reproduce_table7()
    check("Table 7 unit-aware reproduces 3 of 5 rows",
          res["unit_aware"]["n_matching"] == 3,
          str(res["unit_aware"]["n_matching"]))
    check("Table 7 literal reproduces 4 of 5 rows",
          res["literal"]["n_matching"] == 4,
          str(res["literal"]["n_matching"]))
    check("every Table 7 row is reproducible by some convention",
          res["n_reproducible_by_some_convention"] == res["n_total"] == 5)


# ---------------------------------------------------------------------------
# 7. Table 8 DS scores
# ---------------------------------------------------------------------------
def test_table8() -> None:
    strict = rp.reproduce_table8(MODE_STRICT)
    compat = rp.reproduce_table8(MODE_PUB_COMPAT)

    check("strict mode reproduces 26 of 32 published DS scores",
          strict["n_matching"] == 26,
          str(strict["n_matching"]))
    check("strict mode mismatches are exactly the six parenteral rows",
          [r["aic"] for r in strict["rows"] if not r["match"]] ==
          ["028752172", "028752184", "028752196", "049100011",
           "049100047", "049100074"],
          str([r["aic"] for r in strict["rows"] if not r["match"]]))
    check("all six strict mismatches are parenteral injections",
          all("IM" in r["description"] for r in strict["rows"] if not r["match"]),
          str([r["description"] for r in strict["rows"] if not r["match"]]))

    check("publication-compatible mode reproduces all 32 published DS scores",
          compat["n_matching"] == 32,
          str(compat["n_matching"]))
    check("publication-compatible mode max error within rounding",
          compat["max_abs_error"] <= 0.05,
          f"{compat['max_abs_error']}")
    for row in compat["rows"]:
        check(f"Table 8 AIC {row['aic']} matches the published DS",
              row["match"], f"{row['reproduced_ds']} vs {row['published_ds']}")


# ---------------------------------------------------------------------------
# 8. Ranking order
# ---------------------------------------------------------------------------
def test_ranking() -> None:
    for mode in (MODE_STRICT, MODE_PUB_COMPAT):
        res = rp.reproduce_ranking(mode)
        check(f"ranking order matches the published order ({mode.name})",
              res["identical"], str(res["reproduced_order"]))


# ---------------------------------------------------------------------------
# 9. Scoring-mode semantics
# ---------------------------------------------------------------------------
def test_modes() -> None:
    check("strict mode leaves the printed TRN positions untouched",
          rp_of("TRN", "0039", MODE_STRICT) == ST_RP["TRN"]["0039"])
    check("publication-compatible mode swaps the 0039/0040 TRN positions",
          rp_of("TRN", "0039", MODE_PUB_COMPAT) == 5.0
          and rp_of("TRN", "0040", MODE_PUB_COMPAT) == 7.0)
    check("publication-compatible mode leaves the other scales untouched",
          rp_of("BDF", "0069", MODE_PUB_COMPAT) == ST_RP["BDF"]["0069"])
    check("the mode does not change the TRN scale span",
          close(ST_MAX_DIFF["TRN"], max(ST_RP["TRN"].values())
                - min(ST_RP["TRN"].values())))

    catalogue = rp.build_table8_catalogue()
    query = catalogue[0]
    a = ds_score(query, catalogue[1])
    b = ds_components(query, catalogue[1])["ds"]
    check("ds_score agrees with ds_components", close(a, b))


# ---------------------------------------------------------------------------
# 10. DS score bounds and internal consistency
# ---------------------------------------------------------------------------
def test_ds_bounds() -> None:
    catalogue = rp.build_table8_catalogue()
    query = catalogue[0]
    for cand in catalogue[1:]:
        ds = ds_score(query, cand)
        check(f"DS of {cand.aic} is within [0, 100]",
              0.0 <= ds <= 100.0, f"{ds}")
        comp = ds_components(query, cand)
        total = comp["penalty_ndxup"] + comp["penalty_st_total"]
        check(f"DS of {cand.aic} matches its component breakdown",
              close(ds, 100.0 - total, 1e-9), f"{ds} vs {100.0 - total}")
        check(f"weighted ST contributions of {cand.aic} sum to the ST part",
              close(sum(comp["weighted_nrd"].values()) / 100.0 * MAX_ST_PENALTY,
                    comp["penalty_st_total"], 1e-9))


# ---------------------------------------------------------------------------
# 11. find_substitutes behaviour
# ---------------------------------------------------------------------------
def test_find_substitutes() -> None:
    catalogue = rp.build_table8_catalogue()
    query = catalogue[0]
    results = find_substitutes(query, catalogue, MODE_PUB_COMPAT)
    check("find_substitutes returns every candidate", len(results) == len(catalogue) - 1)
    scores = [r.ds for r in results]
    check("find_substitutes sorts by descending DS",
          all(a >= b for a, b in zip(scores, scores[1:])), str(scores[:5]))
    check("the query itself is excluded",
          all(r.sub.aic != query.aic for r in results))


# ---------------------------------------------------------------------------
# 12. Validation indicators
# ---------------------------------------------------------------------------
def test_validation_indicators() -> None:
    catalogue = rp.build_table8_catalogue()
    query = catalogue[0]
    results = find_substitutes(query, catalogue, MODE_PUB_COMPAT)
    ind = validation_indicators([(query, results)])
    check("validation indicators are produced", bool(ind))
    check("validation indicators count every alternative",
          ind["n_alternatives"] == len(results), str(ind["n_alternatives"]))
    check("validation indicator bands partition the alternatives",
          close(ind["pct_ds_100"] + ind["pct_ds_90_99"] + ind["pct_ds_80_89"]
                + ind["pct_ds_lt_80"], 100.0, 1e-6))
    check("validation indicators report the same-BDF share",
          0.0 <= ind["pct_same_bdf"] <= 100.0)


def main() -> int:
    for fn in (test_constants, test_penalty_ladder, test_worked_example,
               test_nrd, test_fictitious_codes, test_equation4, test_table8,
               test_ranking, test_modes, test_ds_bounds,
               test_find_substitutes, test_validation_indicators):
        fn()
    failed = [(n, d) for n, ok, d in CHECKS if not ok]
    print(f"Caviglioli correctness suite: {len(CHECKS) - len(failed)}/{len(CHECKS)} "
          f"assertions passed")
    for name, detail in failed:
        print(f"  FAIL: {name} {detail}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
