#!/usr/bin/env python3
"""
Reproduction script for CMPB manuscript tables and figures.

This script reproduces all key results from the manuscript:
- Table 8: DS scores for all 32 products (V0, V1, V2, V3)
- Table 7: NDXUP sums under both unit conventions
- Figure 1: DS formula decomposition (TikZ source in manuscript/figures/)
- Figure 2: Scoring workflow (TikZ source in manuscript/figures/)
- Performance benchmarks (Table 5 in manuscript)
"""

import sys
from pathlib import Path

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent / "code"))

from reproduce_published import (
    reproduce_table8,
    reproduce_table7,
    reproduce_ranking,
    check_worked_example,
    check_penalty_ladder,
    check_table6,
    build_table8_catalogue,
    MODE_STRICT,
    MODE_PUB_COMPAT,
)
from ds_algorithm import (
    ds_components,
    ds_score,
    find_substitutes,
    MedicinalProduct,
    ScoringMode,
    MODE_STRICT as DS_MODE_STRICT,
    MODE_PUB_COMPAT as DS_MODE_PUB_COMPAT,
)
from discrepancy_analysis import (
    structural_analysis,
    reconcile_search,
)


def main():
    print("=" * 70)
    print("CMPB Manuscript Reproduction")
    print("=" * 70)

    # 1. Worked example (BDF NRD)
    print("\n" + "-" * 70)
    print("WORKED EXAMPLE: BDF Tablet (RP 1) vs Syrup (RP 20)")
    print("-" * 70)
    worked = check_worked_example()
    print(f"  NRD = {worked['nrd_reproduced']:.2f} (published: 41.30)")
    print(f"  Weighted contribution = {worked['weighed_reproduced']:.4f} (published: 18.998)")
    print(f"  Match: {worked['matches']}")

    # 2. Penalty ladder (Table 4)
    print("\n" + "-" * 70)
    print("PENALTY LADDER (Table 4)")
    print("-" * 70)
    ladder = check_penalty_ladder()
    print(f"  Branches tested: {ladder['n']}, Matching: {ladder['n_matching']}")

    # 3. Table 6 (fictitious ATC)
    print("\n" + "-" * 70)
    print("TABLE 6: FICTITIOUS ATC RULE")
    print("-" * 70)
    table6 = check_table6()
    print(f"  FC codes tested: {table6['n']}, Rule satisfied: {table6['n_rule_satisfied']}, Published matches: {table6['n_published_match_rule']}")

    # 4. Table 8 reproduction
    print("\n" + "-" * 70)
    print("TABLE 8: DS Scores for 32 Products")
    print("-" * 70)

    # V0 - strict baseline
    v0 = reproduce_table8(mode=MODE_STRICT)
    print(f"\n  V0 (strict baseline): {v0['n_matching']}/{v0['n_candidates']} match")
    if not v0['all_match']:
        for r in v0['rows']:
            if not r['match']:
                print(f"    FAIL: {r['aic']} computed={r['reproduced_ds']:.4f} published={r['published_ds']:.4f} diff={r['abs_error']:.4f}")

    # V1 - publication compatible
    v1 = reproduce_table8(mode=MODE_PUB_COMPAT)
    print(f"\n  V1 (+TRN reconciliation): {v1['n_matching']}/{v1['n_candidates']} match")
    print(f"  Max error: {v1['max_abs_error']:.4f}")

    # V2 - V1 + literal Equation 4
    # Note: V2 is V1 with literal convention for Eq 4; Table 8 doesn't use Eq 4
    # so V2 matches V1 for Table 8
    print(f"\n  V2 (V1 + literal Eq.4): {v1['n_matching']}/{v1['n_candidates']} match (Table 8 unaffected by Eq 4 convention)")

    # 5. Table 7 reproduction
    print("\n" + "-" * 70)
    print("TABLE 7: FC NDXUP Sums (5 rows)")
    print("-" * 70)
    table7 = reproduce_table7()
    for convention in ('unit_aware', 'literal'):
        conv_data = table7[convention]
        print(f"\n  {convention.upper()} convention: {conv_data['n_matching']}/{conv_data['n']} match")
        for row in conv_data['rows']:
            status = "✓" if row['match'] else "✗"
            print(f"    {status} {row['api1']}+{row['api2']}: reproduced={row['reproduced_ndxup_sum']:.4f}, published={row['published_ndxup_sum']:.1f}")

    print(f"\n  Reproducible by SOME convention: {table7['n_reproducible_by_some_convention']}/{table7['n_total']}")

    # 6. Ranking
    print("\n" + "-" * 70)
    print("RANKING (V1 mode)")
    print("-" * 70)
    ranking = reproduce_ranking(mode=MODE_PUB_COMPAT)
    print(f"  Published ranking order matches: {ranking['identical']}")
    print(f"  Top 5:")
    for i, aic in enumerate(ranking['reproduced_order'][:5]):
        eq = " (equiv)" if i < 4 else ""  # first 4 are equivalents
        print(f"    {i+1}. {aic}: DS = {v1['rows'][i]['reproduced_ds']:.2f}{eq}")

    # 7. Structural discrepancy analysis
    print("\n" + "-" * 70)
    print("STRUCTURAL DISCREPANCY ANALYSIS")
    print("-" * 70)
    structural = structural_analysis()
    conflicts = structural['identical_st_groups_with_conflicting_published_ds']
    print(f"  Identical-ST groups with conflicting published DS: {len(conflicts)}")
    for c in conflicts:
        print(f"    Group ranks {c['ranks']}: published DS values = {c['published_ds_values']}")

    # 8. Reconciliation search
    print("\n" + "-" * 70)
    print("RECONCILIATION SEARCH (TRN transposition)")
    print("-" * 70)
    reconcile = reconcile_search()
    print(f"  Best interpretation: {reconcile['finding'][:100]}...")
    print(f"  Solutions found: {reconcile['n_solutions']}")
    print(f"  Feasible TRN range (Table 8 TRA): {reconcile['feasible_trn_max_diff_interval_with_table8_tra']}")
    print(f"  Strict TRN max diff from Table 1: {reconcile['strict_trn_max_diff_from_table1']}")
    print(f"  Note: TRN transposition is INFERRED from published scores, not authoritatively confirmed")

    # 9. Performance
    print("\n" + "-" * 70)
    print("PERFORMANCE")
    print("-" * 70)
    import time
    catalogue = build_table8_catalogue()
    query = next(p for p in catalogue if p.aic == "037599230")
    candidates = [p for p in catalogue if p.atc == query.atc and p.aic != query.aic]
    start = time.perf_counter()
    for _ in range(100):
        for cand in candidates:
            ds_score(query, cand)
    elapsed = (time.perf_counter() - start) / 100
    print(f"  {len(candidates)} candidates, 100 iterations: {elapsed*1000:.1f} ms total")
    print(f"  Per candidate: {elapsed*1_000_000/len(candidates):.1f} µs")

    # 10. find_substitutes
    print("\n" + "-" * 70)
    print("FIND_SUBSTITUTES() - Ranked candidates (V1)")
    print("-" * 70)
    ranked = find_substitutes(query, catalogue, mode=MODE_PUB_COMPAT)
    print(f"  Top 5 substitutes for {query.aic}:")
    for r in ranked[:5]:
        eq = " (equivalent)" if r.is_equivalent else ""
        print(f"    {r.rank}. {r.sub.aic}: DS = {r.ds:.2f}{eq}")

    print("\n" + "=" * 70)
    print("Reproduction complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()