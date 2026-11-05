#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measures of the future module (phase D, step 3): every alternative
(calculations/future_policies.ALTERNATIVES) is run in the reference path
(scenario 0) and in the n scenarios of step 2, with the effects of the
measures drawn per scenario. Writes to output_files/:

  future_policies.csv                scenario, alternative, year, metric, value
  future_policies_effects.csv        the drawn effects per scenario
  future_policies_robustness.csv     per alternative and target: share of
                                     scenarios that meet it (satisficing),
                                     failure rate, regret (90th percentile
                                     and max) and median value
  future_policies_vulnerability.csv  Spearman correlation of every factor
                                     and effect with the margin to each
                                     target, per alternative

Usage: python future_policies.py [--n 1000]
"""
import argparse
import logging
import time
import warnings

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from calculations.future import COLLECTION, COMMERCIAL_BULKY, REUSABLE, Scenario, WORN
from calculations.future_policies import (ALTERNATIVES, met, policy, recorded_metrics, regret, sample_effects,
                                          targets)
from calculations.future_scenarios import factor_table, metrics, sample_scenarios
from calculations.utils import PRODUCT_GROUPS
from future_scenarios import _residual_stock_2025
from main_future import _future_indicators, prepare_history, run_future

CORE = PRODUCT_GROUPS.index('CORE')


def parse_arguments():
    parser = argparse.ArgumentParser(description="Measures of the future module in the scenarios.")
    parser.add_argument('--n', type=int, default=1000, help="Number of Latin hypercube scenarios")
    return parser.parse_args()


def _history_2025(history):
    hist = history['hist']
    reference = pd.read_csv('output_files/future_reference.csv')
    incineration = reference[reference['flow_name'].isin(['WM.RS-WM.IN-Domestic incineration-TOT',
                                                          'WM.RS-RW.RW-Residual waste export for incineration-TOT'])
                             & (reference['year'] == 2025)]['value'].sum()
    discards = sum(hist.flows[c].values[-1, CORE] for c in (COLLECTION, REUSABLE, WORN, COMMERCIAL_BULKY))
    return {'incineration_kt': incineration, 'household_discards_kt': discards}


def run_all(history, scenarios, effects):
    frames = []
    for i, (scenario, drawn) in enumerate(zip(scenarios, effects)):
        for name in ALTERNATIVES:
            fut, ref, (fut_fibre, _) = run_future(history, scenario, policy(name, drawn))
            values = metrics(fut, ref, _future_indicators(fut, history['preloaded_data']),
                             _residual_stock_2025(history, ref), fut_fibre)
            values.update(recorded_metrics(fut))
            values['sorted_reuse_export_kt'] = fut.flows['CO.SO-RW.RW-Export of sorted textiles for reuse-TOT'].values[
                :, CORE]
            for metric, series in values.items():
                frames.append(pd.DataFrame({'scenario': i, 'alternative': name, 'year': list(fut.dims['t'].items),
                                            'metric': metric, 'value': series}))
    return pd.concat(frames, ignore_index=True)


def robustness(results, target_list):
    rows = []
    sampled = results[results['scenario'] > 0]
    for metric, year, direction, threshold, basis in target_list:
        table = sampled[(sampled['metric'] == metric) & (sampled['year'] == year)].pivot(
            index='scenario', columns='alternative', values='value')[list(ALTERNATIVES)]
        regrets = np.array([regret(row, direction) for row in table.to_numpy()])
        for j, name in enumerate(table.columns):
            satisficed = met(table[name], direction, threshold)
            rows.append({'alternative': name, 'metric': metric, 'year': year, 'basis': basis,
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
    sampled = results[results['scenario'] > 0]
    for metric, year, direction, threshold, basis in target_list:
        table = sampled[(sampled['metric'] == metric) & (sampled['year'] == year)].pivot(
            index='scenario', columns='alternative', values='value')
        for name in ALTERNATIVES:
            margin = (table[name] - threshold) * (1 if direction == '>=' else -1)
            for factor in factors.columns:
                rho = spearmanr(factors.loc[table.index, factor], margin).statistic
                rows.append({'alternative': name, 'metric': metric, 'year': year, 'basis': basis,
                             'factor': factor, 'spearman': rho})
    return pd.DataFrame(rows)


def main():
    args = parse_arguments()
    logging.disable(logging.WARNING)
    history = prepare_history()
    scenarios = [Scenario.reference(history['hist'])] + sample_scenarios(args.n)
    # The reference path gets the middle of each effect span.
    effects = sample_effects(args.n)
    effects = [{k: float(np.mean([e[k] for e in effects])) for k in effects[0]}] + effects
    start = time.time()
    results = run_all(history, scenarios, effects)
    print(f"[INFO] {len(scenarios)} scenarios x {len(ALTERNATIVES)} alternatives in {time.time() - start:.1f} s")
    target_list = targets(_history_2025(history))
    factors = pd.DataFrame([{**factor_table(s), **e} for s, e in zip(scenarios, effects)])
    factors.index.name = 'scenario'
    results.to_csv('output_files/future_policies.csv', index=False)
    factors.to_csv('output_files/future_policies_effects.csv')
    table = robustness(results, target_list)
    table.to_csv('output_files/future_policies_robustness.csv', index=False)
    vulnerability(results, target_list, factors).to_csv('output_files/future_policies_vulnerability.csv',
                                                         index=False)
    print("[INFO] Wrote output_files/future_policies*.csv")
    pd.set_option('display.width', 250)
    print(table.pivot_table(index=['metric', 'year', 'basis', 'target'], columns='alternative',
                            values='satisficing')[list(ALTERNATIVES)].round(2).to_string())


if __name__ == '__main__':
    main()
