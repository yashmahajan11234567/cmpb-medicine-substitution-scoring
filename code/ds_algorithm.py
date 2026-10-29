"""Caviglioli et al. (2025) substitution-scoring algorithm - reproduction.

Paper
-----
Caviglioli, G., Drava, G., Pivetta, L., Di Meco, C., Livoti, E., Paoli, G.,
Baldassari, S., Ailuno, G., Franchina, M. P., Bonsignore, A., Di Giorgio, D. &
Rebesco, B. (2025). "Medicine Shortages: An Algorithm for Evaluating the
Substitution with Equivalent or Alternative Products." Healthcare, 13(10),
1139. DOI 10.3390/healthcare13101139. PMCID PMC12111303. Licence CC BY 4.0.

What the paper's algorithm does
--------------------------------
Every marketed medicinal product (MP) is encoded by a string made of

    ATC code | BDF | AME | ISI | RCA | TRN | NDXUP

where

  * ATC          the 5-level Anatomical Therapeutic Chemical code identifying
                 the active pharmaceutical ingredient (API);
  * BDF/AME/ISI/RCA/TRN
                 five EDQM Standard Terms (ver. 1.2.0-28 January 2019), each
                 with a four-digit numeric code and a *relative position* (RP)
                 inside its own ordered scale (Table 1 of the paper);
  * NDXUP        the number of Defined Daily Doses per presentation unit.

A query MP ("lak", lacking/unavailable) is compared with every candidate MP
("sub") that shares its ATC code.  The *degree of substitutability* (DS) is

    DS = 100 - (penalty_NDXUP + penalty_STs)                              (1)

    penalty_NDXUP   from Table 4, at most 10 points
    penalty_STs     sum over the 5 STs of  NRD_n * wf_n / 100 * 80          (3)

where NRD_n is the *normalized relative distance* between the two RPs of that
ST, normalized to 100 (Equation 2):

    NRD = |RP_lak - RP_sub| / |max difference in absolute value| * 100

and wf_n are the weight factors of Table 5.  The maximum difference is a
function of the ST scale: it is the whole range of the RPs for that ST.

MPs whose *entire* code string matches the query are pharmaceutical
equivalents and score DS = 100.  Everything else with the same ATC is an
alternative, ranked by decreasing DS.

Fixed-dose combinations (FCs) get two extra provisions:

  * a fictitious ATC code (Table 6) when the official code is ambiguous - the
    fourth level is the API with the main therapeutic effect and the fifth
    level is a number in the 99..80 range (or a letter+number pair) so that
    each FC is unambiguous;
  * NDXUP for an FC is the sum of the component NDXUPs (Equation 4), because
    WHO defines no DDD for FCs:

        NDXUP_FC = Dosage_API1/DDD_API1 + Dosage_API2/DDD_API2

This module implements all of the above.  It contains no I/O and no
hard-coded results: everything is derived from the published scales, weights
and penalty table.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------
# EDQM Standard Terms scales (paper Table 1)
# Each entry is (ST-ID, term label, relative position (RP)).
# --------------------------------------------------------------------------

ST_SCALES: Dict[str, List[Tuple[str, str, float]]] = {
    "BDF": [
        ("0069", "Tablet", 1.0),
        ("0058", "Lozenge", 2.0),
        ("0051", "Capsule", 3.0),
        ("0050", "Cachet", 3.5),
        ("0060", "Pastille", 4.0),
        ("0054", "Gum", 5.0),
        ("0064", "Pillules", 6.0),
        ("0062", "Pellets", 7.0),
        ("0053", "Granules", 7.2),
        ("0066", "Powder", 8.0),
        ("0059", "Lyophilisate", 10.0),
        ("0052", "Film", 11.0),
        ("0114", "Herbal material (unprocessed)", 12.0),
        ("0070", "Tea", 13.0),
        ("0085", "Suspension", 15.0),
        ("0079", "Dispersion", 15.5),
        ("0080", "Emulsion", 16.0),
        ("0090", "Drops", 18.0),
        ("0082", "Liquid", 18.5),
        ("0084", "Solvent", 19.0),
        ("0083", "Solution", 19.5),
        ("0086", "Syrup", 20.0),
        ("0078", "Concentrate", 20.5),
        ("0094", "Spray (unspecified)", 22.0),
        ("0081", "Lacquer", 23.0),
        ("0077", "Collodion", 24.0),
        ("0093", "Shampoo", 25.0),
        ("0073", "Gel", 26.0),
        ("0072", "Foam", 26.5),
        ("0071", "Cream", 27.0),
        ("0074", "Ointment", 29.0),
        ("0076", "Poultice", 30.0),
        ("0075", "Paste", 31.0),
        ("0065", "Plaster", 33.0),
        ("0061", "Patch", 33.5),
        ("0056", "Impregnated material", 36.0),
        ("0067", "Stick", 36.5),
        ("0103", "Cement", 38.0),
        ("0068", "Suppository", 40.5),
        ("0063", "Pessary", 41.0),
        ("0088", "Insert", 42.0),
        ("0102", "Pouch", 42.5),
        ("0055", "Implant", 43.0),
        ("0089", "Additive (unspecified)", 44.0),
        ("0092", "Radiopharmaceutical", 45.0),
        ("0095", "System", 46.0),
        ("0087", "Medicinal gas", 47.0),
    ],
    "AME": [
        ("0019", "Swallowing", 1.0),
        ("0018", "Sucking", 2.0),
        ("0014", "Orodispersion", 3.0),
        ("0007", "Chewing", 4.0),
        ("0008", "Gargling", 5.0),
        ("0017", "Spraying", 6.0),
        ("0013", "Instillation", 7.0),
        ("0015", "Rinsing/washing", 8.0),
        ("0005", "Application", 9.0),
        ("0006", "Bathing", 10.0),
        ("0012", "Insertion", 11.0),
        ("0011", "Injection", 12.0),
        ("0009", "Infusion", 13.0),
        ("0113", "Implantation", 14.0),
        ("0010", "Inhalation", 15.0),
        ("0111", "Burning", 16.0),
        ("0112", "Dialysis", 17.0),
        ("0004", "Administration", 18.0),
        ("0020", "Not specified", 19.0),
    ],
    "ISI": [
        ("0031", "Oral", 1.0),
        ("0032", "Oromucosal", 2.0),
        ("0023", "Dental", 3.0),
        ("0106", "Gastric", 4.0),
        ("0107", "Gastroenteral", 5.0),
        ("0108", "Intestinal", 6.0),
        ("0035", "Rectal", 7.0),
        ("0036", "Vaginal", 8.0),
        ("0022", "Cutaneous/transdermal", 9.0),
        ("0021", "Auricular", 10.0),
        ("0029", "Nasal", 11.0),
        ("0030", "Ocular", 12.0),
        ("0110", "Oculonasal", 13.0),
        ("0034", "Pulmonary", 14.0),
        ("0033", "Parenteral", 15.0),
        ("0026", "Intramammary", 16.0),
        ("0105", "Endocervical", 17.0),
        ("0027", "Intrauterine", 18.0),
        ("0028", "Intravesical/urethral", 19.0),
        ("0109", "Intraperitoneal", 20.0),
        ("0024", "Environmental", 21.0),
        ("0025", "Extracorporeal", 22.0),
        ("0037", "Unknown/miscellaneous", 23.0),
    ],
    "RCA": [
        ("0047", "Conventional", 1.0),
        ("0045", "Prolonged", 3.0),
        ("0046", "Modified", 6.0),
        ("0044", "Delayed", 9.0),
        ("0048", "Unknown", 10.0),
    ],
    "TRN": [
        ("0042", "No transformation", 1.0),
        ("0038", "Dilution", 3.0),
        ("0040", "Dissolution", 5.0),
        ("0039", "Dispersion", 7.0),
        ("0041", "Mixing", 7.5),
        ("0043", "Unknown", 10.0),
    ],
}

ST_NAMES: Tuple[str, ...] = ("BDF", "AME", "ISI", "RCA", "TRN")

# Weight factors (paper Table 5).
ST_WEIGHTS: Dict[str, float] = {
    "BDF": 0.46,
    "AME": 0.18,
    "ISI": 0.20,
    "RCA": 0.09,
    "TRN": 0.07,
}

# ST-ID -> RP lookup, per ST.
ST_RP: Dict[str, Dict[str, float]] = {
    name: {sid: rp for sid, _label, rp in entries}
    for name, entries in ST_SCALES.items()
}

# The maximum difference in absolute value of each ST scale: the whole range
# of the RPs for that ST (max RP - min RP).  Equation (2) divides by it.
ST_MAX_DIFF: Dict[str, float] = {
    name: max(rp for _s, _l, rp in entries)
    - min(rp for _s, _l, rp in entries)
    for name, entries in ST_SCALES.items()
}

# --------------------------------------------------------------------------
# Scoring modes
# --------------------------------------------------------------------------
#
# The paper's printed Table 1 assigns the TRN relative positions
#
#     0042 No transformation  1      0040 Dissolution  5
#     0038 Dilution           3      0039 Dispersion   7
#                                  0041 Mixing        7.5
#                                  0043 Unknown      10
#
# i.e. the printed column places TRA-0040 *before* TRA-0039 even though the
# EDQM code order inside the transformation group is
# 0038 < 0039 < 0040 < 0041.  With the printed positions the six parenteral
# rows of Table 8 (which carry TRA = 0039) cannot be reproduced: they need
# |RP_lak - RP_sub| = 4 (TRA 0039 at RP 5), not 6 (RP 7).
#
# MODE_STRICT is the paper exactly as printed.  MODE_PUB_COMPAT applies the
# single transposition of the adjacent Table 1 rows TRA-0039 / TRA-0040,
# which restores the ascending EDQM code order and reproduces all 32
# published Table 8 DS scores.  The transposition is documented, not silently
# applied: both modes are reported side by side everywhere.

@dataclass(frozen=True)
class ScoringMode:
    """A named interpretation of the published scales."""

    name: str
    description: str
    trn_rp_overrides: Tuple[Tuple[str, float], ...] = ()

    @property
    def trn_overrides(self) -> Dict[str, float]:
        return dict(self.trn_rp_overrides)


MODE_STRICT = ScoringMode(
    name="strict",
    description=("Paper exactly as printed: Table 1 relative positions "
                 "(TRA-0039 Dispersion at RP 7, TRA-0040 Dissolution at RP 5)."),
)

MODE_PUB_COMPAT = ScoringMode(
    name="publication_compatible",
    description=("Publication-compatible mode: the single transposition of "
                 "the adjacent Table 1 rows TRA-0039 and TRA-0040 "
                 "(TRA-0039 Dispersion at RP 5, TRA-0040 Dissolution at RP 7). "
                 "Reproduces all 32 published Table 8 DS scores."),
    trn_rp_overrides=(("0039", 5.0), ("0040", 7.0)),
)

# Maximum deduction for the NDXUP class and for the ST class (paper Eq. 1).
MAX_NDXUP_PENALTY = 10.0
MAX_ST_PENALTY = 80.0

# The paper states that an MP with DS > 90 is a potential substitution
# candidate, and that DS = 100 marks a pharmaceutical equivalent.
DS_SUBSTITUTION_THRESHOLD = 90.0
DS_EQUIVALENT = 100.0


# --------------------------------------------------------------------------
# Product record
# --------------------------------------------------------------------------


@dataclass
class MedicinalProduct:
    """One marketed medicinal product."""

    aic: str                       # Italian MA number (AIC)
    description: str
    atc: str                       # 5-level ATC code (may be a fictitious FC code)
    bdf: str                       # EDQM ST-ID
    ame: str
    isi: str
    rca: str
    trn: str
    ndxup: float                   # number of DDDs per presentation unit
    api: Optional[str] = None      # optional API name (documentation only)
    ddd: Optional[float] = None     # optional DDD of the API (documentation only)

    # -- code string -------------------------------------------------------
    @property
    def code(self) -> str:
        """The full identification string used for exact-equivalence matching."""
        return (f"{self.atc}|{self.bdf}|{self.ame}|{self.isi}|{self.rca}"
                f"|{self.trn}|{self.ndxup:g}")

    @property
    def st_tuple(self) -> Tuple[str, str, str, str, str]:
        return (self.bdf, self.ame, self.isi, self.rca, self.trn)


# --------------------------------------------------------------------------
# NDXUP penalty (paper Table 4)
# --------------------------------------------------------------------------


def penalty_ndxup(ndxup_lak: float, ndxup_sub: float) -> float:
    """Penalty for a difference in the number of DDDs per presentation unit.

    Table 4 of the paper:

        NDXUP_lak == NDXUP_sub                     ->  0
        0.5 * NDXUP_lak == NDXUP_sub               ->  2
        2 * NDXUP_lak == NDXUP_sub                 ->  4
        0.5 * NDXUP_lak <  NDXUP_sub < NDXUP_lak   ->  6
        NDXUP_lak <  NDXUP_sub < 2 * NDXUP_lak     ->  8
        NDXUP_sub <  0.5 * NDXUP_lak              -> 10
        NDXUP_sub >  2 * NDXUP_lak                 -> 10
    """
    lak = float(ndxup_lak)
    sub = float(ndxup_sub)
    eps = 1e-9
    if abs(sub - lak) <= eps:
        return 0.0
    if abs(sub - 0.5 * lak) <= eps:
        return 2.0
    if abs(sub - 2.0 * lak) <= eps:
        return 4.0
    if 0.5 * lak < sub < lak:
        return 6.0
    if lak < sub < 2.0 * lak:
        return 8.0
    if sub < 0.5 * lak:
        return MAX_NDXUP_PENALTY
    if sub > 2.0 * lak:
        return MAX_NDXUP_PENALTY
    # Not covered by Table 4: the value sits exactly on a boundary that the
    # table leaves out (e.g. NDXUP_sub == 0.5*NDXUP_lak with NDXUP_lak == 0).
    return MAX_NDXUP_PENALTY


# --------------------------------------------------------------------------
# Normalized relative distance (paper Equation 2)
# --------------------------------------------------------------------------


def nrd(st: str, rp_lak: float, rp_sub: float) -> float:
    """Normalized relative distance between two RPs of the same ST scale.

        NRD = |RP_lak - RP_sub| / |max difference in absolute value| * 100
    """
    denom = ST_MAX_DIFF[st]
    if denom <= 0:
        return 0.0
    return abs(float(rp_lak) - float(rp_sub)) / denom * 100.0


def rp_of(st: str, st_id: str, mode: Optional[ScoringMode] = None) -> float:
    """Relative position of an ST-ID inside its scale.

    ``mode`` may override the printed position of individual ST-IDs (only
    the TRN scale is ever overridden, and only by MODE_PUB_COMPAT).
    """
    if mode is not None and st == "TRN":
        override = mode.trn_overrides.get(st_id)
        if override is not None:
            return override
    try:
        return ST_RP[st][st_id]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"unknown {st} ST-ID {st_id!r}") from exc


# --------------------------------------------------------------------------
# The DS score (paper Equations 1, 2, 3)
# --------------------------------------------------------------------------


def ds_components(lak: MedicinalProduct, sub: MedicinalProduct,
                  mode: Optional[ScoringMode] = None) -> Dict:
    """Full breakdown of the DS score for one (query, candidate) pair."""
    pen_ndxup = penalty_ndxup(lak.ndxup, sub.ndxup)
    per_st: Dict[str, float] = {}
    nrd_values: Dict[str, float] = {}
    weighted: Dict[str, float] = {}
    total_st = 0.0
    for st, sid_lak, sid_sub in zip(ST_NAMES, lak.st_tuple, sub.st_tuple):
        r_lak = rp_of(st, sid_lak, mode)
        r_sub = rp_of(st, sid_sub, mode)
        d = nrd(st, r_lak, r_sub)
        nrd_values[st] = d
        w = ST_WEIGHTS[st]
        weighted[st] = d * w
        per_st[st] = weighted[st] / 100.0 * MAX_ST_PENALTY
        total_st += per_st[st]
    ds = DS_EQUIVALENT - (pen_ndxup + total_st)
    return {
        "ds": ds,
        "penalty_ndxup": pen_ndxup,
        "penalty_st_total": total_st,
        "penalty_st_per_st": per_st,
        "nrd": nrd_values,
        "weighted_nrd": weighted,
        "is_equivalent": lak.code == sub.code,
    }


def ds_score(lak: MedicinalProduct, sub: MedicinalProduct) -> float:
    """Degree of substitutability of ``sub`` for ``lak`` (0..100)."""
    return ds_components(lak, sub)["ds"]


# --------------------------------------------------------------------------
# Query / ranking
# --------------------------------------------------------------------------


@dataclass
class SubstitutionResult:
    sub: MedicinalProduct
    ds: float
    is_equivalent: bool
    penalty_ndxup: float
    penalty_st_total: float
    rank: int = 0


def find_substitutes(lak: MedicinalProduct,
                     catalogue: Sequence[MedicinalProduct],
                     mode: Optional[ScoringMode] = None,
                     ) -> List[SubstitutionResult]:
    """All MPs sharing the query's ATC, ranked by decreasing DS.

    Pharmaceutical equivalents (identical full code string) come first with
    DS = 100; the remaining alternatives follow in decreasing DS order, as in
    the paper's Excel macro output (Table 8).
    """
    results: List[SubstitutionResult] = []
    for mp in catalogue:
        if mp.aic == lak.aic:
            continue
        if mp.atc != lak.atc:
            continue
        comp = ds_components(lak, mp, mode)
        results.append(SubstitutionResult(
            sub=mp,
            ds=comp["ds"],
            is_equivalent=comp["is_equivalent"],
            penalty_ndxup=comp["penalty_ndxup"],
            penalty_st_total=comp["penalty_st_total"],
        ))
    # Equivalents first, then by decreasing DS; ties broken by AIC for a
    # deterministic order.
    results.sort(key=lambda r: (not r.is_equivalent, -r.ds, r.sub.aic))
    for i, r in enumerate(results, start=1):
        r.rank = i
    return results


# --------------------------------------------------------------------------
# Fixed-dose combinations
# --------------------------------------------------------------------------


def fc_ndxup(components: Sequence[Tuple[float, float]]) -> float:
    """NDXUP of a fixed-dose combination (paper Equation 4).

    ``components`` is a sequence of ``(dosage, ddd)`` pairs, one per API:
    the dosage contained in the presentation unit and the DDD of that API.
    Both numbers must already be expressed in the same unit.

        NDXUP_FC = sum_i Dosage_APIi / DDD_APIi
    """
    return float(sum(dosage / ddd for dosage, ddd in components))


# --------------------------------------------------------------------------
# Units for Equation 4
# --------------------------------------------------------------------------

# Mass units and their factor towards the milligram.  A "tab"/"tablet" DDD
# is a count of tablets and is therefore *not* convertible to a mass; the
# paper's Table 7 prints such a DDD (row 2, desogestrel, "1 tab").
UNIT_TO_MG: Dict[str, float] = {
    "mg": 1.0,
    "g": 1000.0,
    "mcg": 0.001,
    "ug": 0.001,
    "µg": 0.001,
}

#: The two unit conventions that can be applied to the printed Table 7.
FC_UNIT_LITERAL = "literal"
FC_UNIT_AWARE = "unit_aware"


def fc_ndxup_units(components: Sequence[Tuple[float, str, float, str]],
                   convention: str = FC_UNIT_AWARE) -> float:
    """NDXUP of a fixed-dose combination from *printed* dosages and DDDs.

    ``components`` is a sequence of
    ``(dosage_value, dosage_unit, ddd_value, ddd_unit)`` tuples.

    Two conventions are supported, because the published Table 7 mixes them:

    ``FC_UNIT_AWARE`` (unit-correct)
        Both quantities are converted to a common base (milligram) before
        the division.  A DDD expressed as a tablet count cannot be
        converted; it is used as the bare number, which is what makes the
        desogestrel row non-convertible.

    ``FC_UNIT_LITERAL`` (publication-compatible)
        The printed numbers are divided as they stand, ignoring the units
        entirely.  This is what reproduces the published gentamycin row
        (30 mg / 1 g becomes 30 / 1 = 30).

    The two conventions disagree on the published table: neither reproduces
    all five published sums.  See ``report.md``.
    """
    if convention not in (FC_UNIT_LITERAL, FC_UNIT_AWARE):
        raise ValueError(f"unknown convention {convention!r}")
    total = 0.0
    for dose, dose_unit, ddd, ddd_unit in components:
        if convention == FC_UNIT_LITERAL:
            total += dose / ddd
            continue
        d_factor = UNIT_TO_MG.get(dose_unit.strip().lower())
        q_factor = UNIT_TO_MG.get(ddd_unit.strip().lower())
        if d_factor is None or q_factor is None:
            # Not a convertible mass on both sides (e.g. "1 tab"): the
            # numbers are divided as printed.
            total += dose / ddd
        else:
            total += (dose * d_factor) / (ddd * q_factor)
    return float(total)


def fictitious_fc_atc(atc_fourth_level: str, taken: Optional[Sequence[int]] = None) -> str:
    """Fictitious ATC code for an FC with an ambiguous official code.

    The paper's convention: keep the fourth level of the API with the main
    therapeutic effect and use a fifth level in the 99..80 range that has not
    been used before.  If every number in 99..80 is taken, a letter (A..Z)
    plus a digit (0..9) is appended, giving 260 further codes per ATC and 520
    when the letter/digit order is also swapped.
    """
    used = set(taken or [])
    for fifth in range(99, 79, -1):
        if fifth not in used:
            return f"{atc_fourth_level}{fifth}"
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for digit in "0123456789":
            if f"{letter}{digit}" not in used:
                return f"{atc_fourth_level}{letter}{digit}"
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for digit in "0123456789":
            if f"{digit}{letter}" not in used:
                return f"{atc_fourth_level}{digit}{letter}"
    raise ValueError("no fictitious ATC code available")


# --------------------------------------------------------------------------
# Validation helpers (the paper's internal validation indicators)
# --------------------------------------------------------------------------


def validation_indicators(pairs: Sequence[Tuple[MedicinalProduct, List[SubstitutionResult]]]
                          ) -> Dict[str, float]:
    """The 10 similarity indicators the paper computes on its test set.

    For every query item the paper records the alternatives the algorithm
    proposed and computes:

      * percentage of alternatives with DS = 100%;
      * percentage of alternatives with DS in [90, 99];
      * percentage of alternatives with DS in [80, 89];
      * percentage of alternatives with DS < 80;
      * percentage of alternatives with the same BDF as the reference item;
      * percentage of reference items whose alternatives differ by at most
        1..5 STs (five separate indicators).

    ``pairs`` is a sequence of (query item, its ranked results).
    """
    n_alt = 0
    n_eq = n_90_99 = n_80_89 = n_lt80 = 0
    n_same_bdf = 0
    st_diff_counts: Dict[int, int] = {k: 0 for k in range(1, 6)}
    n_items = 0
    for lak, res in pairs:
        if not res:
            continue
        n_items += 1
        for r in res:
            n_alt += 1
            if r.ds >= 100.0 - 1e-9:
                n_eq += 1
            elif r.ds >= 90.0:
                n_90_99 += 1
            elif r.ds >= 80.0:
                n_80_89 += 1
            else:
                n_lt80 += 1
            if r.sub.bdf == lak.bdf:
                n_same_bdf += 1
            n_diff = sum(1 for a, b in zip(lak.st_tuple, r.sub.st_tuple) if a != b)
            for k in range(1, 6):
                if n_diff <= k:
                    st_diff_counts[k] += 1
    def pct(num: int, den: int) -> float:
        return 100.0 * num / den if den else float("nan")
    out = {
        "n_items": n_items,
        "n_alternatives": n_alt,
        "pct_ds_100": pct(n_eq, n_alt),
        "pct_ds_90_99": pct(n_90_99, n_alt),
        "pct_ds_80_89": pct(n_80_89, n_alt),
        "pct_ds_lt_80": pct(n_lt80, n_alt),
        "pct_same_bdf": pct(n_same_bdf, n_alt),
    }
    for k in range(1, 6):
        out[f"pct_items_within_{k}_st_diff"] = pct(st_diff_counts[k], n_alt)
    return out
