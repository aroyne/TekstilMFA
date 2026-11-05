#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Runs the reference path of the future module (phase D, D12; the 2025
values carried on, Scenario.reference): the
deterministic historical run (iteration 0) is closed first, and the
future system (2026-2050, same register) starts from it
(calculations/future.py). Both are written to
output_files/future_reference.csv (flow_name, product, year, period,
value), with TOTAL rows for outputs split by product or group, the stock
change of every stock, the stock level in US.HH (CORE) as the residual of
the balance and in the cohort model, and the indicators (EPR basis,
collection rate). The fibre layer (D19) of both is written to
output_files/future_reference_fibre.csv with a material column.

Usage: python main_future.py [--seed 1]
"""
import argparse

import numpy as np
import pandas as pd

import flodym as fd

from calculations.fibre_layer import compute_fibre_layer
from calculations.future import (FUTURE_YEARS, Policy, Reference, Scenario, execute_future, future_composition_data,
                                 stock_driven_purchases)
from calculations.indicators import indicators
from calculations.params import Parameters
from calculations.sampling import DEFAULT_SEED
from calculations.system import close, make_system, reset
from calculations.utils import PRODUCT_GROUPS, YEARS
from data_loader import load_all_data
from main_mc import ALL_POOLS, _with_totals, outputs, run_pools, to_long

TARGET = 'output_files/future_reference.csv'
FIBRE_TARGET = 'output_files/future_reference_fibre.csv'
RESIDUAL_STOCK = 'US.HH-US.HH-Stock-TOT'
COHORT_STOCK = 'US.HH-US.HH-Stock model stock-TOT'
COHORT_DISCARDS = 'US.HH-US.HH-Stock model discards-TOT'


def parse_arguments():
    parser = argparse.ArgumentParser(description="Reference path of the future module.")
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED, help="Seed of the historical run")
    return parser.parse_args()


def prepare_history(seed=DEFAULT_SEED):
    """
    The closed historical system (iteration 0) and its fibre layer, run
    once for all scenarios: {'hist', 'hist_fibre', 'hist_stock',
    'preloaded_data', 'params', 'current_params'}.
    """
    params = Parameters()
    preloaded_data = load_all_data(ALL_POOLS + ['future'], params)
    current_params, dataset_noise, anchors = params.draw(seed, 0)
    hist = make_system()
    run_pools(hist, ALL_POOLS, preloaded_data, current_params, dataset_noise, anchors)
    close(hist)
    hist_fibre = make_system(fibre=True)
    hist_stock = compute_fibre_layer(hist_fibre, hist, preloaded_data, current_params, params.fibre_composition)
    return {'hist': hist, 'hist_fibre': hist_fibre, 'hist_stock': hist_stock, 'preloaded_data': preloaded_data,
            'params': params, 'current_params': current_params}


# The stock-driven purchases and the second-hand sales they depend on are
# solved by repeating the future run until the purchases no longer change.
STOCK_DRIVEN_TOLERANCE_KT = 1e-6
STOCK_DRIVEN_MAX_PASSES = 30


def run_future(history, scenario, policy=None, fibre=True, demand='supply', baseline_purchases=None):
    """
    Runs one scenario with one policy (Policy.none() if not given) and one
    demand (DEMAND_MODES) from the prepared history. baseline_purchases are
    the stock-driven purchases of the same scenario without measures, for
    the rebound. Returns (closed future
    system, Reference, closed future fibre system and its stock model
    outputs, or (None, None) without the fibre layer).
    """
    preloaded_data = history['preloaded_data']
    # 'population' <- data_files/SSB_05803_befolkning_1985_2026.csv:
    # population on 1 January (SSB 05803), as the mean of the year (2025)
    # 'population_projection' <- data_files/SSB_14740_befolkningsframskriving_2026_2051.csv:
    # SSB's 2026 population projection, as the mean of the year
    population = {**{YEARS[-1]: preloaded_data['population'][YEARS[-1]]},
                  **preloaded_data['population_projection'][scenario.population]}
    ref = Reference(history['hist'], population, history['current_params'], scenario,
                    Policy.none() if policy is None else policy, demand, baseline_purchases)
    fut = make_system(years=FUTURE_YEARS)
    reset(fut)
    execute_future(fut, ref)
    if demand == 'stock':
        for _ in range(STOCK_DRIVEN_MAX_PASSES):
            purchases = stock_driven_purchases(fut, ref)
            if ref.purchases is not None and np.abs(purchases - ref.purchases).max() < STOCK_DRIVEN_TOLERANCE_KT:
                break
            ref.set_purchases(purchases)
            reset(fut)
            execute_future(fut, ref)
        else:
            raise RuntimeError(f"Stock-driven purchases did not converge in {STOCK_DRIVEN_MAX_PASSES} passes")
    close(fut)
    if not fibre:
        return fut, ref, (None, None)
    fut_fibre = make_system(fibre=True, years=FUTURE_YEARS)
    fut_stock = compute_fibre_layer(fut_fibre, fut, future_composition_data(preloaded_data,
                                                                            scenario.synthetic_shift_2035),
                                    ref.current_params, history['params'].fibre_composition,
                                    history=history['hist_fibre'],
                                    household_lifetime_factor=ref.household_lifetime_factor,
                                    household_period_factor=ref.household_period_factor)
    return fut, ref, (fut_fibre, fut_stock)


def run_reference(seed=DEFAULT_SEED):
    """
    The reference path (Scenario.reference). Returns (closed historical
    system, closed future system, Reference, preloaded data, {'history',
    'future'}: (closed fibre system, stock model outputs)).
    """
    history = prepare_history(seed)
    fut, ref, fut_layer = run_future(history, Scenario.reference(history['hist']))
    layers = {'history': (history['hist_fibre'], history['hist_stock']), 'future': fut_layer}
    return history['hist'], fut, ref, history['preloaded_data'], layers


def _future_indicators(fut, preloaded_data):
    # 'epr_scope_share' <- data_files/Tab_08801_textiles.csv (SSB 08801):
    # the share of finished-goods mass within the EPR customs codes, held at
    # its 2025 value
    shares = {key: np.full(len(FUTURE_YEARS), values[-1])
              for key, values in preloaded_data['epr_scope_share'].items()}
    return indicators(fut, {'epr_scope_share': shares})


def _stock_levels(hist, fut, ref):
    core = PRODUCT_GROUPS.index('CORE')
    change = np.concatenate([(s.stocks['US.HH'].inflow - s.stocks['US.HH'].outflow).values[:, core]
                             for s in (hist, fut)])
    years = YEARS + FUTURE_YEARS
    return {
        RESIDUAL_STOCK: (years, ref.cohorts['stock_1987'] + np.cumsum(change)),
        COHORT_STOCK: (years, ref.cohorts['stock']),
        COHORT_DISCARDS: (years, ref.cohorts['outflow']),
    }


def table(hist, fut, ref, preloaded_data):
    frames = []
    for period, mfa, extra in (('history', hist, indicators(hist, preloaded_data)),
                               ('future', fut, _future_indicators(fut, preloaded_data))):
        arrays = outputs(mfa, closed=True)
        arrays.update({name: fd.FlodymArray(dims=mfa.dims[('t',)], values=v) for name, v in extra.items()})
        store = {name: (arr, arr.values[None]) for name, arr in arrays.items()}
        for name, arr, values, label in _with_totals(store):
            flat, frame = to_long(name, arr, values, label)
            frames.append(frame.assign(period=period, value=flat[0]))
    for name, (years, values) in _stock_levels(hist, fut, ref).items():
        frames.append(pd.DataFrame({'flow_name': name, 'product': 'CORE', 'year': years, 'value': values,
                                    'period': ['history' if y in YEARS else 'future' for y in years]}))
    result = pd.concat(frames, ignore_index=True)
    return result[['flow_name', 'product', 'year', 'period', 'value']].sort_values(
        ['flow_name', 'product', 'year']).reset_index(drop=True)


def fibre_table(layers):
    frames = []
    for period, (fibre, stock_model) in layers.items():
        store = {name: (arr, arr.values[None]) for name, arr in {**outputs(fibre, closed=True), **stock_model}.items()}
        for name, arr, values, label in _with_totals(store):
            flat, frame = to_long(name, arr, values, label)
            frames.append(frame.assign(period=period, value=flat[0]))
    result = pd.concat(frames, ignore_index=True)
    return result[['flow_name', 'product', 'material', 'year', 'period', 'value']].sort_values(
        ['flow_name', 'product', 'material', 'year']).reset_index(drop=True)


def main():
    args = parse_arguments()
    hist, fut, ref, preloaded_data, layers = run_reference(args.seed)
    print(f"[INFO] Cohort model scaled to the 2025 statistics: s = {ref.scale:.3f}")
    table(hist, fut, ref, preloaded_data).to_csv(TARGET, index=False)
    print(f"[INFO] Wrote {TARGET}")
    fibre_table(layers).to_csv(FIBRE_TARGET, index=False)
    print(f"[INFO] Wrote {FIBRE_TARGET}")


if __name__ == '__main__':
    main()
