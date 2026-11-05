#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measures of the future module (phase D, steps 3 and 4): every alternative
(calculations/future_policies.ALTERNATIVES) is run in the reference path
(scenario 0) and in the n scenarios of step 2, under both demands
(supply-driven and stock-driven), with the effects of the measures drawn
per scenario. Under the stock-driven demand the scenario without measures
is run first, and its purchases are the baseline of the rebound. The
scenarios are spread over worker processes. Writes to output_files/:

  future_policies.csv                scenario, demand, alternative, year,
                                     metric, value (for KEY_YEARS)
  future_policies_effects.csv        the factors and drawn effects per scenario
  future_policies_robustness.csv     per demand, alternative and target: share
                                     of scenarios that meet it (satisficing),
                                     failure rate, regret (90th percentile and
                                     max) and median, 5th and 95th percentile
  future_policies_vulnerability.csv  Spearman correlation of every factor and
                                     effect with the margin to each target,
                                     per demand and alternative

Usage: python future_policies.py [--n 1000] [--workers 8]
"""
import argparse
import logging
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from calculations.fibre_layer import new_goods_to_households, supply_composition
from calculations.future import BASE, COLLECTION, COMMERCIAL_BULKY, DEMAND_MODES, REUSABLE, Scenario, WORN
from calculations.future_policies import (ALTERNATIVES, CORE_PRODUCTS_INDEX, met, new_material_metrics, policy,
                                          recorded_metrics, regret, sample_effects, targets)
from calculations.future_scenarios import factor_table, metrics, sample_scenarios
from calculations.utils import MATERIALS, PRODUCT_GROUPS, YEARS
from future_scenarios import _residual_stock_2025
from main_future import _future_indicators, prepare_history, run_future

CORE = PRODUCT_GROUPS.index('CORE')
KEY_YEARS = [2030, 2035, 2040, 2050]
_HISTORY = {}


def parse_arguments():
    parser = argparse.ArgumentParser(description="Measures of the future module in the scenarios.")
    parser.add_argument('--n', type=int, default=1000, help="Number of Latin hypercube scenarios")
    parser.add_argument('--workers', type=int, default=8, help="Worker processes")
    return parser.parse_args()


def _textile_share(history):
    # 'imports_by_fibre_class' <- data_files/Tab_08801_textiles.csv (SSB 08801)
    # and parameters/hs_main_fibre.csv, via supply_composition: the textile
    # (non-NT) share of the new goods of each CORE product in 2025
    composition = supply_composition(history['preloaded_data'], history['current_params'],
                                     history['params'].fibre_composition)
    return 1.0 - composition[BASE, CORE_PRODUCTS_INDEX, MATERIALS.index('NT')]


def _init_worker():
    logging.disable(logging.WARNING)
    history = prepare_history()
    _HISTORY.update(history)
    _HISTORY['textile_share'] = _textile_share(history)


def _run_one(history, scenario, alternative, effects, demand, baseline):
    fut, ref, _ = run_future(history, scenario, policy(alternative, effects), fibre=False, demand=demand,
                             baseline_purchases=baseline)
    values = metrics(fut, ref, _future_indicators(fut, history['preloaded_data']),
                     _residual_stock_2025(history, ref))
    values.update(recorded_metrics(fut))
    values.update(new_material_metrics(fut, ref, history['textile_share']))
    return ref, values


def run_scenario(task):
    """All alternatives under both demands for one scenario; long rows for KEY_YEARS."""
    i, scenario, effects = task
    history = _HISTORY
    years = list(range(YEARS[-1] + 1, YEARS[-1] + 1 + 25))
    index = [years.index(y) for y in KEY_YEARS]
    rows = []
    for demand in DEMAND_MODES:
        baseline_ref, baseline_values = _run_one(history, scenario, 'L0', effects, demand, None)
        baseline = baseline_ref.purchases if demand == 'stock' else None
        for alternative in ALTERNATIVES:
            values = baseline_values if alternative == 'L0' else _run_one(
                history, scenario, alternative, effects, demand, baseline)[1]
            for metric, series in values.items():
                for year, j in zip(KEY_YEARS, index):
                    rows.append((i, demand, alternative, year, metric, float(series[j])))
    return rows


def _base_2025(history):
    hist = history['hist']
    reference = pd.read_csv('output_files/future_reference.csv')
    incineration = reference[reference['flow_name'].isin(['WM.RS-WM.IN-Domestic incineration-TOT',
                                                          'WM.RS-RW.RW-Residual waste export for incineration-TOT'])
                             & (reference['year'] == 2025)]['value'].sum()
    discards = sum(hist.flows[c].values[-1, CORE] for c in (COLLECTION, REUSABLE, WORN, COMMERCIAL_BULKY))
    # 'population' <- data_files/SSB_05803_befolkning_1985_2026.csv:
    # population on 1 January (SSB 05803), as the mean of the year
    population = history['preloaded_data']['population'][YEARS[-1]]
    new_goods = new_goods_to_households(hist.flows)[BASE, CORE_PRODUCTS_INDEX]
    return {'incineration_kt': incineration, 'household_discards_kt': discards,
            'new_goods_kg_per_capita': new_goods.sum() * 1e6 / population,
            'virgin_fibre_kg_per_capita': (new_goods * _textile_share(history)).sum() * 1e6 / population}


def robustness(results, target_list):
    rows = []
    for metric, year, direction, threshold, basis in target_list:
        sel = results[(results['scenario'] > 0) & (results['metric'] == metric) & (results['year'] == year)]
        for demand, group in sel.groupby('demand'):
            table = group.pivot(index='scenario', columns='alternative', values='value')[list(ALTERNATIVES)]
            regrets = np.array([regret(row, direction) for row in table.to_numpy()])
            for j, name in enumerate(table.columns):
                satisficed = met(table[name], direction, threshold)
                rows.append({'demand': demand, 'alternative': name, 'metric': metric, 'year': year, 'basis': basis,
                             'target': f'{direction} {threshold:.3g}', 'satisficing': satisficed.mean(),
                             'failure_rate': 1.0 - satisficed.mean(), 'regret_p90': np.quantile(regrets[:, j], 0.9),
                             'regret_max': regrets[:, j].max(), 'median': table[name].median(),
                             'p5': table[name].quantile(0.05), 'p95': table[name].quantile(0.95)})
    return pd.DataFrame(rows)


def vulnerability(results, target_list, factors):
    # A margin that is the same in every scenario (e.g. no unsorted export
    # under L2) has no rank correlation; it is reported as NaN.
    warnings.filterwarnings('ignore', message='An input array is constant')
    rows = []
    for metric, year, direction, threshold, basis in target_list:
        sel = results[(results['scenario'] > 0) & (results['metric'] == metric) & (results['year'] == year)]
        for (demand, name), group in sel.groupby(['demand', 'alternative']):
            margin = (group.set_index('scenario')['value'] - threshold) * (1 if direction == '>=' else -1)
            for factor in factors.columns:
                rho = spearmanr(factors.loc[margin.index, factor], margin).statistic
                rows.append({'demand': demand, 'alternative': name, 'metric': metric, 'year': year,
                             'basis': basis, 'factor': factor, 'spearman': rho})
    return pd.DataFrame(rows)


def main():
    args = parse_arguments()
    logging.disable(logging.WARNING)
    history = prepare_history()
    history['textile_share'] = _textile_share(history)
    scenarios = [Scenario.reference(history['hist'])] + sample_scenarios(args.n)
    # The reference path gets the middle of each effect span.
    effects = sample_effects(args.n)
    effects = [{k: float(np.mean([e[k] for e in effects])) for k in effects[0]}] + effects
    start = time.time()
    with ProcessPoolExecutor(max_workers=args.workers, initializer=_init_worker) as pool:
        chunks = list(pool.map(run_scenario, [(i, s, e) for i, (s, e) in enumerate(zip(scenarios, effects))],
                               chunksize=8))
    results = pd.DataFrame([row for chunk in chunks for row in chunk],
                           columns=['scenario', 'demand', 'alternative', 'year', 'metric', 'value'])
    print(f"[INFO] {len(scenarios)} scenarios x {len(ALTERNATIVES)} alternatives x {len(DEMAND_MODES)} demands "
          f"in {time.time() - start:.1f} s")
    target_list = targets(_base_2025(history))
    factors = pd.DataFrame([{**factor_table(s), **e} for s, e in zip(scenarios, effects)])
    factors.index.name = 'scenario'
    results.to_csv('output_files/future_policies.csv', index=False)
    factors.to_csv('output_files/future_policies_effects.csv')
    table = robustness(results, target_list)
    table.to_csv('output_files/future_policies_robustness.csv', index=False)
    vulnerability(results, target_list, factors).to_csv('output_files/future_policies_vulnerability.csv',
                                                         index=False)
    print("[INFO] Wrote output_files/future_policies*.csv")
    pd.set_option('display.width', 300)
    print(table.pivot_table(index=['metric', 'year', 'target', 'demand'], columns='alternative',
                            values='satisficing')[list(ALTERNATIVES)].round(2).to_string())


if __name__ == '__main__':
    main()
