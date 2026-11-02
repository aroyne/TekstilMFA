#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Structural sensitivity (phase A, A5): methodological choices that are not
part of the Monte Carlo are tested one at a time in the deterministic run,
and their effect on the main outputs is compared with the baseline. Each
variant overrides drawn parameters; the data and the rest of the model are
unchanged.

Writes output_files/structural_sensitivity.csv (variant, output, year,
baseline, variant value, difference).

Usage: python structural_sensitivity.py
"""
import pandas as pd

from calculations.fibre_layer import compute_fibre_layer
from calculations.params import Parameters
from calculations.sampling import DEFAULT_SEED
from calculations.system import close, make_system
from data_loader import load_all_data
from main_mc import ALL_POOLS, outputs, run_pools

OUTPUT = 'output_files/structural_sensitivity.csv'
YEARS_SHOWN = [1990, 2000, 2010, 2025]
OUTPUTS = [
    'US.HH-US.HH-Stock-TOT',
    'US.HH-US.HH-Stock change-TOT',
    'US.HH-US.HH-Stock model stock-TOT',
    'US.HH-US.HH-Stock model discards-TOT',
    'DI.RT-US.HH-Sales to households-TOT',
    'US.HH-EN.WA-Fibre release in laundry-TOT',
    'DI.RT-WM.RS-Unsold goods discarded-TOT',
]


def _shapes(value):
    return lambda params: {k: value for k in params if k.startswith('lifetime_shape_')}


# name: (description, function of the drawn parameters returning overrides)
VARIANTS = {
    'spinup_0.6': ('Inflow before 1988 at 60 % of the 1988 level (D2)',
                   lambda params: {'spinup_inflow_factor': 0.6}),
    'spinup_0.8': ('Inflow before 1988 at 80 % of the 1988 level (D2)',
                   lambda params: {'spinup_inflow_factor': 0.8}),
    'weibull_shape_1.5': ('Weibull shape 1.5 for all lifetimes (wider spread), same means', _shapes(1.5)),
    'weibull_shape_3': ('Weibull shape 3 for all lifetimes (narrower spread), same means', _shapes(3.0)),
    'no_online_returns': ('No returns of direct online purchases (VOEC as net, before D38)',
                          lambda params: {'online_return_share': 0.0}),
    'unsold_eea': ('Unsold goods destroyed at 6.5 % of what is placed on the market (EEA 2024 midpoint, D38)',
                   lambda params: {'unsold_destroyed_share': 0.065}),
    'laundry_mepex': ('Laundry release at the Mepex 2014 level (about 1.5 kt) with the same release per kg for all '
                      'fibres (before D37)',
                      lambda params: {'laundry_release_ppm': 955.0, 'natural_release_relative_to_synthetic': 1.0}),
}


def run_variant(params, preloaded_data, mfa, fibre, overrides):
    """{output: array (year,)} for one deterministic run with the given parameter overrides."""
    current_params, dataset_noise, anchors = params.draw(DEFAULT_SEED, 0)
    current_params.update(overrides(current_params))
    run_pools(mfa, ALL_POOLS, preloaded_data, current_params, dataset_noise, anchors)
    close(mfa)
    stock_model = compute_fibre_layer(fibre, mfa, preloaded_data, current_params, params.fibre_composition)
    arrays = {**outputs(mfa, True), **stock_model}
    years = list(mfa.dims['t'].items)
    result = {}
    for name in OUTPUTS:
        values = arrays[name].sum_to(('t',)).values
        result[name] = {year: values[years.index(year)] for year in YEARS_SHOWN}
    return result


def main():
    params = Parameters()
    preloaded_data = load_all_data(ALL_POOLS, params)
    mfa = make_system()
    fibre = make_system(fibre=True)
    baseline = run_variant(params, preloaded_data, mfa, fibre, lambda p: {})
    rows = []
    for name, (description, overrides) in VARIANTS.items():
        result = run_variant(params, preloaded_data, mfa, fibre, overrides)
        for output in OUTPUTS:
            for year in YEARS_SHOWN:
                base, value = baseline[output][year], result[output][year]
                rows.append({'variant': name, 'description': description, 'output': output, 'year': year,
                             'baseline': base, 'value': value, 'difference': value - base})
    table = pd.DataFrame(rows)
    table.to_csv(OUTPUT, index=False)
    print(f"[INFO] Wrote {OUTPUT}")
    pd.set_option('display.width', 250)
    print(table.pivot_table(index=['output', 'variant'], columns='year', values='difference').round(1))


if __name__ == '__main__':
    main()
