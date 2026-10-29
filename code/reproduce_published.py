"""Reproduce the published results of Caviglioli et al. (2025).

Paper
-----
Caviglioli, G. et al. (2025). "Medicine Shortages: An Algorithm for
Evaluating the Substitution with Equivalent or Alternative Products."
Healthcare 13(10):1139. DOI 10.3390/healthcare13101139. PMCID PMC12111303.

What is reproduced
------------------
1. The published worked example: the normalised relative distance (NRD)
   between a *tablet* and a *syrup* for the Basic Dose Form (BDF) standard
   term, which the paper states is 41.30, and the corresponding weighed
   contribution 41.30 x 0.46 = 18.998.

2. The full Excel-macro output of Table 8: the query is the risperidone 2 mg
   film tablet (Italian MA number 037599230) and the published table lists 32
   candidate substitutes with their DS scores.  Every one of those 32 scores
   is recomputed here from the published scales, weights and penalty table.

3. Table 7: the NDXUP of five illustrative fixed-dose combinations computed
   with the paper's Equation (4).

4. Table 2/3: the ST codification of the risperidone MPs and the
   "combined code" string of the 3 mg film tablet.

Nothing is hard-coded: the catalogue below contains only the *published*
product attributes (AIC, description, ST codes, NDXUP) so that the algorithm
can be run over them; the scores are all produced by ``ds_algorithm``.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ds_algorithm import (DS_EQUIVALENT, FC_UNIT_AWARE, FC_UNIT_LITERAL,
                           MODE_PUB_COMPAT, MODE_STRICT,
                           MedicinalProduct, ScoringMode, ds_components,
                           ds_score, fictitious_fc_atc, fc_ndxup,
                           fc_ndxup_units, find_substitutes, nrd,
                           penalty_ndxup, rp_of, ST_MAX_DIFF, ST_WEIGHTS)

OUT = os.path.join(os.path.dirname(HERE), "outputs")


# --------------------------------------------------------------------------
# Published product data (paper Table 8 - attributes only, no scores)
# --------------------------------------------------------------------------

# The query MP: film tablet containing 2 mg of risperidone (MA 037599230).
# Table 3 shows its combined code: ATC N05AX08, BDF 0069, AME 0019,
# ISI 0031, RCA 0047, TRN 0042, NDXUP 0.6 for the 3 mg tablet and 0.4 for
# the 2 mg tablet (DDD oral risperidone = 5 mg).
QUERY_AIC = "037599230"

# (aic, description, bdf, isi, ame, rca, trn, ndxup)
TABLE8_PRODUCTS = [
    ("028752069", "RISPERDAL 60TAB 2MG ORANGE", "0069", "0031", "0019", "0047", "0042", 0.4),
    ("037092222", "RISPERIDONE TE 60FILM TAB 2MG", "0069", "0031", "0019", "0047", "0042", 0.4),
    ("040078293", "RISPERIDONE AURO 60TAB 2MG", "0069", "0031", "0019", "0047", "0042", 0.4),
    ("040616082", "RISPERIDONE MY 60FILM TAB 2MG", "0069", "0031", "0019", "0047", "0042", 0.4),
    ("028752057", "RISPERDAL 60TAB 1MG WHITE", "0069", "0031", "0019", "0047", "0042", 0.2),
    ("037092069", "RISPERIDONE TE 60FILM TAB 1MG", "0069", "0031", "0019", "0047", "0042", 0.2),
    ("037599065", "RISPERIDONE SAN 60FILM TAB 1MG", "0069", "0031", "0019", "0047", "0042", 0.2),
    ("040078192", "RISPERIDONE AURO 60TAB 1MG", "0069", "0031", "0019", "0047", "0042", 0.2),
    ("040616043", "RISPERIDONE MY 60FILM TAB 1MG", "0069", "0031", "0019", "0047", "0042", 0.2),
    ("028752083", "RISPERDAL 60TAB 4MG GREEN", "0069", "0031", "0019", "0047", "0042", 0.8),
    ("037092549", "RISPERIDONE TE 60FILM TAB 4MG", "0069", "0031", "0019", "0047", "0042", 0.8),
    ("037599572", "RISPERIDONE SAN 60FILM TAB 4MG", "0069", "0031", "0019", "0047", "0042", 0.8),
    ("040078495", "RISPERIDONE AURO 60TAB 4MG", "0069", "0031", "0019", "0047", "0042", 0.8),
    ("040616207", "RISPERIDONE MY 60FILM TAB 4MG", "0069", "0031", "0019", "0047", "0042", 0.8),
    ("028752071", "RISPERDAL 60TAB 3MG YELLOW", "0069", "0031", "0019", "0047", "0042", 0.6),
    ("037092386", "RISPERIDONE TE 60FILM TAB 3MG", "0069", "0031", "0019", "0047", "0042", 0.6),
    ("037599406", "RISPERIDONE SAN 60FILM TAB 3MG", "0069", "0031", "0019", "0047", "0042", 0.6),
    ("040078394", "RISPERIDONE AURO 60TAB 3MG", "0069", "0031", "0019", "0047", "0042", 0.6),
    ("040616120", "RISPERIDONE MY 60FILM TAB 3MG", "0069", "0031", "0019", "0047", "0042", 0.6),
    ("037835030", "RISPERDONE SAND OS DROPS 100ML", "0090", "0031", "0019", "0047", "0042", 0.2),
    ("038188037", "RISPERIDONE MY OS DROPS 100ML", "0090", "0031", "0019", "0047", "0042", 0.2),
    ("042441028", "RISPERIDONE AURO DROPS 100ML", "0090", "0031", "0019", "0047", "0042", 0.2),
    ("028752095", "RISPERDAL OS SOL 100ML 1MG/ML", "0083", "0031", "0019", "0047", "0042", 0.2),
    ("028752145", "RISPERDAL OS SOL 30ML 1MG/ML", "0083", "0031", "0019", "0047", "0042", 0.2),
    ("049966017", "OKEDI IM 1SYR 75MG RP", "0085", "0033", "0011", "0045", "0042", 13.9),
    ("049966029", "OKEDI IM 1SYR 100MG RP", "0085", "0033", "0011", "0045", "0042", 18.5),
    ("028752172", "RISPERDAL IM VL 25MG + 1SYR 2ML", "0085", "0033", "0011", "0045", "0039", 4.6),
    ("028752184", "RISPERDAL IM VL 37.5MG + 1SYR 2ML", "0085", "0033", "0011", "0045", "0039", 6.9),
    ("028752196", "RISPERDAL IM VL 50MG + 1SYR 2ML", "0085", "0033", "0011", "0045", "0039", 9.2),
    ("049100011", "RISPERIDONE TE IM 1VL 25MG + 2ML", "0085", "0033", "0011", "0045", "0039", 1.8),
    ("049100047", "RISPERIDONE TE IM VL 37.5MG + 2ML", "0085", "0033", "0011", "0045", "0039", 2.7),
    ("049100074", "RISPERIDONE TE IM 1VL 50MG + 2ML", "0085", "0033", "0011", "0045", "0039", 3.7),
]

# Published DS scores of Table 8, in the same order as TABLE8_PRODUCTS.
TABLE8_PUBLISHED_DS = [
    100.0, 100.0, 100.0, 100.0,
    98.0, 98.0, 98.0, 98.0, 98.0,
    96.0, 96.0, 96.0, 96.0, 96.0,
    92.0, 92.0, 92.0, 92.0, 92.0,
    84.4, 84.4, 84.4,
    83.2, 83.2,
    58.2, 58.2,
    55.7, 55.7, 55.7, 55.7, 55.7, 55.7,
]

ATC_RISPERIDONE = "N05AX08"


def build_table8_catalogue() -> List[MedicinalProduct]:
    """The catalogue the macro searched: the query plus the 32 candidates."""
    out = [
        MedicinalProduct(aic=QUERY_AIC,
                         description="RISPERIDONE MY 60FILM TAB 2MG (query, in shortage)",
                         atc=ATC_RISPERIDONE,
                         bdf="0069", ame="0019", isi="0031", rca="0047",
                         trn="0042", ndxup=0.4),
    ]
    for (aic, desc, bdf, isi, ame, rca, trn, ndxup) in TABLE8_PRODUCTS:
        out.append(MedicinalProduct(aic=aic, description=desc,
                                    atc=ATC_RISPERIDONE,
                                    bdf=bdf, ame=ame, isi=isi, rca=rca,
                                    trn=trn, ndxup=ndxup))
    return out


# --------------------------------------------------------------------------
# 1. The published worked example (Section 3, Equation 2)
# --------------------------------------------------------------------------


def check_worked_example() -> Dict:
    """Reproduce the paper's NRD example: tablet vs syrup for the BDF scale.

    The paper states NRD = 41.30 and the weighed contribution
    41.30 x 0.46 = 18.998.
    """
    rp_tablet = rp_of("BDF", "0069")
    rp_syrup = rp_of("BDF", "0086")
    value = nrd("BDF", rp_tablet, rp_syrup)
    weighed = value * ST_WEIGHTS["BDF"]
    return {
        "rp_tablet": rp_tablet,
        "rp_syrup": rp_syrup,
        "bdf_max_difference": ST_MAX_DIFF["BDF"],
        "nrd_reproduced": value,
        "nrd_published": 41.30,
        "nrd_abs_error": abs(value - 41.30),
        "weighed_reproduced": weighed,
        "weighed_published": 18.998,
        "weighed_abs_error": abs(weighed - 18.998),
        "matches": abs(value - 41.30) < 5e-3 and abs(weighed - 18.998) < 5e-3,
    }


# --------------------------------------------------------------------------
# 2. Table 8 reproduction
# --------------------------------------------------------------------------


def reproduce_table8(mode: ScoringMode = MODE_STRICT) -> Dict:
    """Recompute all 32 published DS scores under the given scoring mode."""
    catalogue = build_table8_catalogue()
    query = catalogue[0]
    results = find_substitutes(query, catalogue, mode)
    by_aic = {r.sub.aic: r for r in results}

    rows = []
    n_match = 0
    max_err = 0.0
    for (aic, desc, *_rest), published in zip(TABLE8_PRODUCTS,
                                             TABLE8_PUBLISHED_DS):
        r = by_aic.get(aic)
        if r is None:
            rows.append({"aic": aic, "description": desc,
                         "published_ds": published, "reproduced_ds": None,
                         "abs_error": None, "match": False,
                         "note": "candidate not returned by the algorithm"})
            continue
        err = abs(r.ds - published)
        max_err = max(max_err, err)
        # the paper prints one decimal place
        match = err < 0.05
        n_match += int(match)
        comp = ds_components(query, r.sub, mode)
        rows.append({
            "aic": aic,
            "description": desc,
            "ndxup": r.sub.ndxup,
            "published_ds": published,
            "reproduced_ds": round(r.ds, 4),
            "abs_error": round(err, 6),
            "match": match,
            "is_equivalent": r.is_equivalent,
            "penalty_ndxup": comp["penalty_ndxup"],
            "penalty_st_total": round(comp["penalty_st_total"], 4),
            "nrd": {k: round(v, 4) for k, v in comp["nrd"].items()},
        })
    return {
        "mode": mode.name,
        "mode_description": mode.description,
        "n_candidates": len(rows),
        "n_matching": n_match,
        "n_exact_within_0.05": n_match,
        "max_abs_error": round(max_err, 6),
        "all_match": n_match == len(rows),
        "rows": rows,
    }


def reproduce_ranking(mode: ScoringMode = MODE_STRICT) -> Dict:
    """Check that the reproduced ranking order matches the published order."""
    catalogue = build_table8_catalogue()
    query = catalogue[0]
    results = find_substitutes(query, catalogue, mode)
    published_order = [aic for (aic, *_r) in TABLE8_PRODUCTS]
    reproduced_order = [r.sub.aic for r in results]
    # published ties are broken by AIC in the table; compare as multisets of
    # positions restricted to the score groups
    return {
        "mode": mode.name,
        "published_order": published_order,
        "reproduced_order": reproduced_order,
        "identical": published_order == reproduced_order,
        "n": len(reproduced_order),
    }


# --------------------------------------------------------------------------
# 3. Table 7 - NDXUP of fixed-dose combinations (Equation 4)
# --------------------------------------------------------------------------


#: Table 7 exactly as printed.
#: Each FC carries two APIs with the DDD printed next to it.
#: ``components`` holds (dosage_value, dosage_unit, ddd_value, ddd_unit).
TABLE7_FCS = [
    {"api1": "Rosuvastatin zinc 10 mg", "ddd_api1": "10 mg",
     "api2": "Ezetimibe 10 mg", "ddd_api2": "10 mg",
     "published": 2.0,
     "components": [(10.0, "mg", 10.0, "mg"), (10.0, "mg", 10.0, "mg")]},
    {"api1": "Desogestrel 0.15 mg", "ddd_api1": "1 tab",
     "api2": "Ethinylestradiol 0.03 mg", "ddd_api2": "25 mcg",
     "published": 0.15,
     "components": [(0.15, "mg", 1.0, "tab"), (0.03, "mg", 25.0, "mcg")]},
    {"api1": "Scopolamine butylbromide 10 mg", "ddd_api1": "60 mg",
     "api2": "Paracetamol 800 mg", "ddd_api2": "3 g",
     "published": 0.43,
     "components": [(10.0, "mg", 60.0, "mg"), (800.0, "mg", 3.0, "g")]},
    {"api1": "Amitriptyline hydrochloride 12.5 mg", "ddd_api1": "75 mg",
     "api2": "Chlordiazepoxide 5 mg", "ddd_api2": "30 mg",
     "published": 0.33,
     "components": [(12.5, "mg", 75.0, "mg"), (5.0, "mg", 30.0, "mg")]},
    {"api1": "Gentamycin sulphate 30 mg", "ddd_api1": "1 g",
     "api2": "Betamethasone valerate 30 mg", "ddd_api2": "2 g",
     "published": 45.0,
     "components": [(30.0, "mg", 1.0, "g"), (30.0, "mg", 2.0, "g")]},
]


def reproduce_table7() -> Dict:
    """Recompute the NDXUP sums of the five illustrative fixed-dose combinations.

    The published table is not reproducible under a single unit convention:
    rows A and D are convention-independent, row C needs unit conversion and
    rows B and E need the literal (unit-ignoring) division.  Both
    conventions are therefore reported side by side, and a row counts as
    reproduced when *some* convention reproduces it.
    """
    out: Dict[str, Dict] = {}
    for convention in (FC_UNIT_AWARE, FC_UNIT_LITERAL):
        rows = []
        n_match = 0
        for fc in TABLE7_FCS:
            value = fc_ndxup_units(fc["components"], convention)
            published = fc["published"]
            err = abs(value - published)
            match = err < 0.005
            n_match += int(match)
            rows.append({
                "api1": fc["api1"], "ddd_api1": fc["ddd_api1"],
                "api2": fc["api2"], "ddd_api2": fc["ddd_api2"],
                "published_ndxup_sum": published,
                "reproduced_ndxup_sum": round(value, 6),
                "abs_error": round(err, 6),
                "match": match,
            })
        out[convention] = {
            "convention": convention,
            "n": len(rows),
            "n_matching": n_match,
            "all_match": n_match == len(rows),
            "rows": rows,
        }
    n_any = sum(
        1
        for i in range(len(TABLE7_FCS))
        if out[FC_UNIT_AWARE]["rows"][i]["match"]
        or out[FC_UNIT_LITERAL]["rows"][i]["match"]
    )
    out["n_total"] = len(TABLE7_FCS)
    out["n_reproducible_by_some_convention"] = n_any
    out["note"] = (
        "The published Table 7 mixes unit conventions: row C is only "
        "reproduced with unit conversion, rows B and E only without it. "
        "No single convention reproduces all five published sums."
    )
    return out


# --------------------------------------------------------------------------
# 4. Table 4 - the NDXUP penalty ladder
# --------------------------------------------------------------------------


def check_penalty_ladder() -> Dict:
    """Exercise every branch of the Table 4 penalty function."""
    lak = 0.4
    cases = [
        (0.4, 0.0),    # equal
        (0.2, 2.0),    # 0.5 * lak
        (0.8, 4.0),    # 2 * lak
        (0.3, 6.0),    # between 0.5*lak and lak
        (0.6, 8.0),    # between lak and 2*lak
        (0.1, 10.0),   # below 0.5*lak
        (0.9, 10.0),   # above 2*lak
    ]
    rows = []
    n_match = 0
    for sub, expected in cases:
        value = penalty_ndxup(lak, sub)
        match = abs(value - expected) < 1e-9
        n_match += int(match)
        rows.append({"ndxup_lak": lak, "ndxup_sub": sub,
                     "expected": expected, "reproduced": value, "match": match})
    return {"n": len(rows), "n_matching": n_match,
            "all_match": n_match == len(rows), "rows": rows}


# --------------------------------------------------------------------------
# 5. Table 6 - fictitious ATC codes for ambiguous fixed-dose combinations
# --------------------------------------------------------------------------


TABLE6_FCS = [
    ("043496037", "Rosuvastatin zinc 10 mg", "Ezetimibe 10 mg", "C10BA06", "C10BA96"),
    ("025253016", "Desogestrel 0.15 mg", "Ethinylestradiol 0.03 mg", "G03AA09", "G03AA09"),
    ("029454028", "Scopolamine butylbromide 10 mg", "Paracetamol 800 mg", "A03DB04", "A03DB95"),
    ("021462066", "Amitriptyline hydrochloride 12.5 mg", "Chlordiazepoxide 5 mg", "N06CA01", "N06CA95"),
    ("021736020", "Gentamycin sulphate 30 mg", "Betamethasone valerate 30 mg", "D07CC01", "D07CC96"),
]


def check_table6() -> Dict:
    """Check the fictitious-ATC-code rule against the paper's Table 6.

    The rule: keep the fourth level of the API with the main therapeutic
    effect and pick an unused fifth level from 99 down to 80.  The published
    codes are the ones the authors assigned in their database, so we verify
    the *rule* (the fifth level is in 99..80 and is unused) and report the
    published code for comparison.  For the desogestrel/ethinylestradiol FC
    the official code is already unambiguous and stays unchanged.
    """
    rows = []
    for aic, api1, api2, official, published in TABLE6_FCS:
        unambiguous = published == official
        if unambiguous:
            rule_ok = True
            generated = official
        else:
            generated = fictitious_fc_atc(official[:5], taken=[])
            rule_ok = (generated[:5] == official[:5]
                       and generated[5:].isdigit()
                       and 80 <= int(generated[5:]) <= 99)
        rows.append({
            "aic": aic, "api1": api1, "api2": api2,
            "official_atc": official, "published_new_atc": published,
            "rule_generated_atc": generated,
            "official_unchanged": unambiguous,
            "rule_satisfied": rule_ok,
            "published_matches_rule": (generated == published) if not unambiguous else True,
        })
    return {
        "n": len(rows),
        "n_rule_satisfied": sum(r["rule_satisfied"] for r in rows),
        "n_published_match_rule": sum(r["published_matches_rule"] for r in rows),
        "rows": rows,
    }


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    payload = {
        "paper": {
            "citation": "Caviglioli, G., Drava, G., Pivetta, L., Di Meco, C., "
                        "Livoti, E., Paoli, G., Baldassari, S., Ailuno, G., "
                        "Franchina, M. P., Bonsignore, A., Di Giorgio, D. & "
                        "Rebesco, B. (2025). Medicine Shortages: An Algorithm "
                        "for Evaluating the Substitution with Equivalent or "
                        "Alternative Products. Healthcare, 13(10), 1139.",
            "doi": "10.3390/healthcare13101139",
            "pmcid": "PMC12111303",
            "license": "CC BY 4.0",
            "source_url": "https://www.ebi.ac.uk/europepmc/webservices/rest/"
                          "PMC12111303/fullTextXML",
            "data_availability": "Farmadati Italia (proprietary, subscription "
                                 "required) and the AIFA shortage list (public). "
                                 "No public dataset or code repository was found.",
        },
        "worked_example": check_worked_example(),
        "strict": {
            "mode": MODE_STRICT.name,
            "mode_description": MODE_STRICT.description,
            "table8_reproduction": reproduce_table8(MODE_STRICT),
            "ranking_order": reproduce_ranking(MODE_STRICT),
        },
        "publication_compatible": {
            "mode": MODE_PUB_COMPAT.name,
            "mode_description": MODE_PUB_COMPAT.description,
            "table8_reproduction": reproduce_table8(MODE_PUB_COMPAT),
            "ranking_order": reproduce_ranking(MODE_PUB_COMPAT),
        },
        "table7_reproduction": reproduce_table7(),
        "penalty_ladder": check_penalty_ladder(),
        "table6_fictitious_codes": check_table6(),
    }
    path = os.path.join(OUT, "caviglioli_reproduction.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1)

    we = payload["worked_example"]
    t7 = payload["table7_reproduction"]
    pl = payload["penalty_ladder"]
    t6 = payload["table6_fictitious_codes"]

    print("=" * 74)
    print("Caviglioli et al. (2025) - reproduction")
    print("=" * 74)
    print(f"worked example NRD tablet-vs-syrup: {we['nrd_reproduced']:.4f} "
          f"(published {we['nrd_published']}) -> "
          f"{'MATCH' if we['matches'] else 'MISMATCH'}")
    print(f"weighed contribution: {we['weighed_reproduced']:.4f} "
          f"(published {we['weighed_published']})")
    for key in ("strict", "publication_compatible"):
        blk = payload[key]
        t8 = blk["table8_reproduction"]
        ro = blk["ranking_order"]
        print(f"[{key:22s}] Table 8 DS: {t8['n_matching']}/{t8['n_candidates']} "
              f"match within 0.05, max abs error {t8['max_abs_error']:.6f}; "
              f"ranking identical to published: {ro['identical']}")
    print(f"Table 7 FC NDXUP sums: unit_aware "
          f"{t7['unit_aware']['n_matching']}/{t7['unit_aware']['n']}, "
          f"literal {t7['literal']['n_matching']}/{t7['literal']['n']}, "
          f"some convention {t7['n_reproducible_by_some_convention']}"
          f"/{t7['n_total']}")
    print(f"Table 4 penalty ladder: {pl['n_matching']}/{pl['n']} branches match")
    print(f"Table 6 fictitious-ATC rule: {t6['n_rule_satisfied']}/{t6['n']} "
          f"rule satisfied, {t6['n_published_match_rule']}/{t6['n']} equal to "
          f"the published code")
    print(f"written: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
