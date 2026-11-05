#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measures (L) of the future module (phase D, step 3,
claude_tekst/2026-11-05_D3_tiltak_forslag.md), run in every scenario of
step 2. The measures are deliberately ambitious, to see whether any effect
can be traced. The effect of each measure is itself an uncertain factor,
drawn per scenario by Latin hypercube with its own seed; a measure has the
same draw in every alternative it is part of, so that the difference
between alternatives within a scenario is the measures only.

Targets are compared on two bases: as the statistics measure them
('recorded', without household textiles in commercial and bulky waste,
D42, which pick analyses do not see) and including that flow ('with D42').
"""
import dataclasses

import numpy as np
from scipy.stats import qmc

from calculations.future import COLLECTION, COMMERCIAL_BULKY, INCINERATION, RESIDUAL_EXPORT, REUSABLE, WORN, Policy
from calculations.utils import PRODUCT_GROUPS

EFFECT_SEED = 2028
CORE = PRODUCT_GROUPS.index('CORE')

# Effects: (Policy field, low, high). Sources and reasons in the note.
EFFECTS = [
    ('collection_increase', 0.10, 0.35),         # L1, share points in 2032
    ('collection_from_reusable', 0.5, 0.9),      # L1
    ('durability_increase', 0.10, 0.50),         # L3, clothing cohorts from 2029
    ('destruction_ban_share_2027', 0.5, 0.9),    # L4
    ('consumption_reduction', 0.10, 0.30),       # L5, CL+HT+FW in 2030
]
# Alternative: which measures it holds (L4 and L5 are separate alternatives,
# and 'Lall' has all five).
ALTERNATIVES = {
    'L0': set(),
    'L1': {'L1'},
    'L2': {'L2'},
    'L3': {'L3'},
    'L4': {'L4'},
    'L5': {'L5'},
    'Lall': {'L1', 'L2', 'L3', 'L4', 'L5'},
}
MEASURE_FIELDS = {
    'L1': ('collection_increase', 'collection_from_reusable'),
    'L3': ('durability_increase',),
    'L4': ('destruction_ban_share_2027',),
    'L5': ('consumption_reduction',),
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


def targets(hist_2025):
    """
    (metric, year, direction, threshold, basis) for the satisficing measure.
    hist_2025: {'incineration_kt', 'household_discards_kt'} in 2025 from the
    history. Thresholds are deliberately ambitious (decision 2026-11-05).
    """
    return [
        ('collection_rate_recorded', 2035, '>=', 0.50, 'recorded'),
        ('collection_rate', 2035, '>=', 0.50, 'with D42'),
        ('unsorted_export_share', 2035, '<=', 0.01, 'recorded'),
        ('reuse_in_norway_kt', 2035, '>=', 8.0, 'recorded'),
        ('incineration_recorded_kt', 2035, '<=', 0.5 * hist_2025['incineration_kt'], 'recorded'),
        ('incineration_kt', 2035, '<=', 0.5 * hist_2025['incineration_kt'], 'with D42'),
        ('household_discards_recorded_kt', 2040, '<=', hist_2025['household_discards_kt'], 'recorded'),
        ('household_discards_kt', 2040, '<=', hist_2025['household_discards_kt'], 'with D42'),
    ]


def met(value, direction, threshold):
    return value >= threshold if direction == '>=' else value <= threshold


def regret(values, direction):
    """Regret per alternative in one scenario: distance to the best alternative, array like values."""
    best = np.max(values) if direction == '>=' else np.min(values)
    return np.abs(best - values)
