#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scenarios for the future module (phase D, step 2,
claude_tekst/2026-11-05_D2_scenarier_forslag.md): the uncertain factors (X)
are deep uncertainties, so each is drawn flat within a plausible span by
Latin hypercube, without probabilities. The spread of the outcomes is a
range of what is possible, not a confidence interval. The same seed gives
the same scenarios, so the measures of step 3 can be run in them.

The uncertainty of the history enters as two factors (discard level and
collection share in 2025, X6 and X7), and population as SSB's three
projections (X1), each in a third of the scenarios.
"""
import numpy as np
from scipy.stats import qmc

from calculations.fibre_layer import DISCARD_FLOWS
from calculations.future import (COLLECTION, COMMERCIAL_BULKY, FUTURE_YEARS, INCINERATION, POPULATION_ALTERNATIVES,
                                 RESIDUAL_EXPORT, REUSABLE, SECONDHAND_SALES, UNSORTED_EXPORT, WORN, Scenario,
                                 _process_inflow)
from calculations.utils import FIBRE_GROUPS, MATERIALS, PRODUCT_GROUPS

SCENARIO_SEED = 2027
CORE = PRODUCT_GROUPS.index('CORE')

# Continuous factors: (Scenario field, low, high). Sources and reasons in
# the design note.
CONTINUOUS = [
    ('consumption_trend_core', -0.03, 0.02),     # X2
    ('consumption_trend_other', -0.02, 0.02),    # X3
    ('lifetime_level', 1.0, 1.75),               # X4
    ('lifetime_new_cohorts_2035', 0.75, 1.0),    # X4b
    ('stock_growth', 0.3, 1.0),                  # X5
    ('discard_level', 0.85, 1.15),               # X6
    ('collection_share', 0.38, 0.55),            # X7
    ('domestic_sorting_share_2035', 0.05, 0.30),  # X8
    ('recycled_fibre_capacity_2035', 0.4, 5.0),  # X10, limited by WM.RC inflow and by spinning in Norway
    ('residual_export_share_2035', 0.05, 0.25),  # X11
    ('synthetic_shift_2035', 0.0, 0.10),         # X12
]
# X9: shares of what is sorted in Norway (reuse, recycling, residues),
# flat on the simplex and truncated to these bounds.
SORTING_BOUNDS = [(0.25, 0.80), (0.02, 0.40), (0.10, 0.70)]


def _truncated_dirichlet(rng, n):
    out = []
    while len(out) < n:
        draw = rng.dirichlet(np.ones(len(SORTING_BOUNDS)))
        if all(lo <= x <= hi for x, (lo, hi) in zip(draw, SORTING_BOUNDS)):
            out.append(tuple(float(x) for x in draw))
    return out


def sample_scenarios(n, seed=SCENARIO_SEED):
    """n Scenarios: Latin hypercube over X1 and the continuous factors, X9 by rejection on the simplex."""
    lhs = qmc.LatinHypercube(d=1 + len(CONTINUOUS), seed=seed).random(n)
    sorting = _truncated_dirichlet(np.random.default_rng(seed), n)
    scenarios = []
    for row, outcome in zip(lhs, sorting):
        population = POPULATION_ALTERNATIVES[min(int(row[0] * 3), 2)]
        values = {name: lo + (hi - lo) * u for (name, lo, hi), u in zip(CONTINUOUS, row[1:])}
        scenarios.append(Scenario(population=population, sorting_outcome_2035=outcome, **values))
    return scenarios


def factor_table(scenario):
    """{factor: number} for one scenario; X1 as -1/0/1 (LLL/MMM/HHH) for rank correlations."""
    row = {name: getattr(scenario, name) for name, _, _ in CONTINUOUS}
    row['population'] = POPULATION_ALTERNATIVES.index(scenario.population) - 1
    for label, value in zip(('sorting_reuse_2035', 'sorting_recycling_2035', 'sorting_residues_2035'),
                            scenario.sorting_outcome_2035):
        row[label] = value
    return row


def _core(fut, code):
    return fut.flows[code].values[:, CORE]


def metrics(fut, ref, future_indicators, residual_stock_2025, fut_fibre=None):
    """
    {metric: array (year,)} over FUTURE_YEARS for one scenario (M1-M9 of
    the design note). residual_stock_2025 is the level of the CORE stock in
    US.HH at the end of 2025 (residual of the balance) in this scenario.
    """
    change = (fut.stocks['US.HH'].inflow - fut.stocks['US.HH'].outflow).values[:, CORE]
    collected = _process_inflow(fut, 'CO.CO', ('t', 'g'))[:, CORE]
    result = {
        'collection_rate': future_indicators['Separate collection rate, households, CORE (share)'],
        'household_discards_kt': sum(_core(fut, c) for c in (COLLECTION, REUSABLE, WORN, COMMERCIAL_BULKY)),
        'reuse_in_norway_kt': _core(fut, SECONDHAND_SALES),
        'unsorted_export_share': _core(fut, UNSORTED_EXPORT) / collected,
        'material_recycling_kt': _process_inflow(fut, 'WM.RC', ('t',)),
        'incineration_kt': fut.flows[INCINERATION].values + fut.flows[RESIDUAL_EXPORT].values,
        'epr_basis_net_kt': future_indicators['EPR basis, net of re-export and online returns (kt)'],
        'household_stock_kt': residual_stock_2025 + np.cumsum(change),
        'household_stock_change_kt': change,
        'cohort_stock_kt': ref.cohorts['stock'][-len(FUTURE_YEARS):],
        'commercial_bulky_kt': _core(fut, COMMERCIAL_BULKY),
        # Where recorded discards exceed supply minus the stock growth of the
        # scenario (high discard level or short lifetimes), commercial and
        # bulky waste is 0 and the stock grows less than X5, by this much.
        'stock_growth_shortfall_kt': fut.clipped[COMMERCIAL_BULKY].values[:, CORE],
    }
    if fut_fibre is not None:
        discards = sum(fut_fibre.flows[c].values[:, CORE, :] for c in DISCARD_FLOWS)
        textile = discards[:, [MATERIALS.index(g) for g in FIBRE_GROUPS]].sum(axis=1)
        result['synthetic_share_discards'] = discards[:, MATERIALS.index('SYN')] / textile
    return result
