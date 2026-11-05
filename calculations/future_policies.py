#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measures (L) of the future module (phase D, steps 3 and 4,
claude_tekst/2026-11-05_D3_tiltak_forslag.md and
claude_tekst/2026-11-05_D4_ny_tilforsel_forslag.md), run in every scenario
of step 2 under both demands (supply-driven and stock-driven). The measures
are deliberately ambitious, to see whether any effect can be traced. The
effect of each measure is itself an uncertain factor, drawn per scenario by
Latin hypercube with its own seed; a measure has the same draw in every
alternative it is part of, so that the difference between alternatives
within a scenario is the measures only.

Targets are compared on two bases where it matters: as the statistics
measure them ('recorded', without household textiles in commercial and
bulky waste, D42, which pick analyses do not see) and including that flow
('with D42'). The main target of step 4 is lower new material input: new
goods and virgin fibre per inhabitant.
"""
import dataclasses

import numpy as np
from scipy.stats import qmc

from calculations.fibre_layer import new_goods_to_households
from calculations.future import (COLLECTION, COMMERCIAL_BULKY, FUTURE_YEARS, INCINERATION, RESIDUAL_EXPORT, REUSABLE,
                                 SORTED_REUSE_EXPORT, WORN, Policy, ramp)
from calculations.utils import CORE_GROUP_PRODUCTS, PRODUCT_GROUPS, PRODUCTS

EFFECT_SEED = 2028
CORE = PRODUCT_GROUPS.index('CORE')
CORE_PRODUCTS_INDEX = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]

# Effects: (Policy field, low, high). Sources and reasons in the notes.
EFFECTS = [
    ('collection_increase', 0.10, 0.35),         # L1, share points in 2032
    ('collection_from_reusable', 0.5, 0.9),      # L1
    ('durability_increase', 0.10, 0.50),         # L3, clothing cohorts from 2029 (times X18)
    ('destruction_ban_share_2027', 0.5, 0.9),    # L4
    ('consumption_reduction', 0.10, 0.30),       # L5, CL+HT+FW in 2030
    ('reuse_market_increase', 1.5, 3.0),         # L6, factor on the second-hand market in 2032
    ('repair_increase', 0.05, 0.20),             # L7, all CORE goods in use, full in 2032
    ('sharing_reduction', 0.05, 0.15),           # L8, clothing in 2030
    ('recycled_content_2035', 0.05, 0.25),       # L9, recycled share of fibre in new goods
]
ALL_MEASURES = {'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9'}
# Alternative: which measures it holds.
ALTERNATIVES = {'L0': set(), **{m: {m} for m in sorted(ALL_MEASURES)}, 'Lall': ALL_MEASURES}
MEASURE_FIELDS = {
    'L1': ('collection_increase', 'collection_from_reusable'),
    'L3': ('durability_increase',),
    'L4': ('destruction_ban_share_2027',),
    'L5': ('consumption_reduction',),
    'L6': ('reuse_market_increase',),
    'L7': ('repair_increase',),
    'L8': ('sharing_reduction',),
    'L9': ('recycled_content_2035',),
}


def sample_effects(n, seed=EFFECT_SEED):
    """n dicts {effect field: drawn value}, Latin hypercube over EFFECTS."""
    lhs = qmc.LatinHypercube(d=len(EFFECTS), seed=seed).random(n)
    return [{name: lo + (hi - lo) * u for (name, lo, hi), u in zip(EFFECTS, row)} for row in lhs]


def policy(name, effects):
    """The Policy of alternative name with the drawn effects of one scenario."""
    measures = ALTERNATIVES[name]
    values = dataclasses.asdict(Policy.none())
    values['name'] = name
    for measure, fields in MEASURE_FIELDS.items():
        if measure in measures:
            for field in fields:
                values[field] = effects[field]
    values['domestic_sorting'] = 'L2' in measures
    values['destruction_ban'] = 'L4' in measures
    return Policy(**values)


def recorded_metrics(fut):
    """
    {metric: array (year,)} as the statistics measure them, without
    household textiles in commercial and bulky waste (D42): the collection
    rate, discards and incineration on the same basis as in 2025.
    """
    def core(code):
        return fut.flows[code].values[:, CORE]
    recorded = core(COLLECTION) + core(REUSABLE) + core(WORN)
    return {
        'collection_rate_recorded': core(COLLECTION) / recorded,
        'household_discards_recorded_kt': recorded,
        'incineration_recorded_kt': (fut.flows[INCINERATION].values + fut.flows[RESIDUAL_EXPORT].values
                                     - core(COMMERCIAL_BULKY)),
    }


def new_material_metrics(fut, ref, textile_share):
    """
    {metric: array (year,)} for new material input (step 4): new CL+HT+FW+YA
    entering households (kt and kg per inhabitant), the virgin fibre in them
    (textile part times one minus the recycled content of L9, phased in
    2028-2035) and the new goods that exported sorted reuse may replace
    abroad (times the displacement X16; reported apart, not netted).
    textile_share: textile (non-NT) share of the new goods of each CORE
    product in 2025, array (CORE product,).
    """
    new_goods = new_goods_to_households(fut.flows)[:, CORE_PRODUCTS_INDEX]
    recycled = ref.policy.recycled_content_2035 * ramp(2027, 2035)
    virgin = (new_goods * textile_share[None, :]).sum(axis=1) * (1.0 - recycled)
    per_inhabitant = 1e6 / ref.population
    return {
        'new_goods_kt': new_goods.sum(axis=1),
        'new_goods_kg_per_capita': new_goods.sum(axis=1) * per_inhabitant,
        'virgin_fibre_kg_per_capita': virgin * per_inhabitant,
        'displaced_abroad_kt': fut.flows[SORTED_REUSE_EXPORT].values[:, CORE] * ref.scenario.displacement,
    }


def targets(base_2025):
    """
    (metric, year, direction, threshold, basis) for the satisficing measure.
    base_2025: values in 2025 from the history ('incineration_kt',
    'household_discards_kt', 'new_goods_kg_per_capita',
    'virgin_fibre_kg_per_capita'). Thresholds are deliberately ambitious
    (decisions 2026-11-05).
    """
    return [
        ('new_goods_kg_per_capita', 2035, '<=', 0.7 * base_2025['new_goods_kg_per_capita'], 'new material'),
        ('virgin_fibre_kg_per_capita', 2035, '<=', 0.7 * base_2025['virgin_fibre_kg_per_capita'], 'new material'),
        ('collection_rate_recorded', 2035, '>=', 0.50, 'recorded'),
        ('collection_rate', 2035, '>=', 0.50, 'with D42'),
        ('unsorted_export_share', 2035, '<=', 0.01, 'recorded'),
        ('reuse_in_norway_kt', 2035, '>=', 8.0, 'recorded'),
        ('incineration_recorded_kt', 2035, '<=', 0.5 * base_2025['incineration_kt'], 'recorded'),
        ('household_discards_recorded_kt', 2040, '<=', base_2025['household_discards_kt'], 'recorded'),
    ]


def met(value, direction, threshold):
    return value >= threshold if direction == '>=' else value <= threshold


def regret(values, direction):
    """Regret per alternative in one scenario: distance to the best alternative, array like values."""
    best = np.max(values) if direction == '>=' else np.min(values)
    return np.abs(best - values)


def year_index(year):
    return FUTURE_YEARS.index(year)
