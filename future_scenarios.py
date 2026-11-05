#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scenarios of the future module (phase D, step 2): the history (iteration
0) is run once, then the reference path (scenario 0, the 2025 values
carried on) and n Latin hypercube scenarios over the uncertain factors
(calculations/future_scenarios.py), each with the fibre layer. Writes to
output_files/:

  future_scenarios.csv              scenario, year, metric, value
  future_scenarios_factors.csv      scenario and its factor values
  future_scenarios_summary.csv      per metric and year: reference, 5th,
                                    50th and 95th percentile, min and max
                                    over the scenarios (a range of what is
                                    possible, not a confidence interval)
  future_scenarios_sensitivity.csv  Spearman rank correlation of each
                                    factor with each metric in 2035 and 2050

Usage: python future_scenarios.py [--n 1000]
"""
import argparse
import logging
import time

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from calculations.future import COMMERCIAL_BULKY, Scenario
from calculations.future_scenarios import factor_table, metrics, sample_scenarios
from calculations.utils import PRODUCT_GROUPS
from main_future import _future_indicators, prepare_history, run_future

CORE = PRODUCT_GROUPS.index('CORE')
SENSITIVITY_YEARS = [2035, 2050]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Scenarios of the future module.")
    parser.add_argument('--n', type=int, default=1000, help="Number of Latin hypercube scenarios")
    return parser.parse_args()


def _residual_stock_2025(history, ref):
    hist = history['hist']
    change = (hist.stocks['US.HH'].inflow - hist.stocks['US.HH'].outflow).values[:, CORE]
    return ref.cohorts['stock_1987'] + change.sum()


def run_scenarios(history, scenarios):
    """Long table (scenario, year, metric, value) and the mass clipped in each scenario."""
    frames, clipped = [], []
    for i, scenario in enumerate(scenarios):
        fut, ref, (fut_fibre, _) = run_future(history, scenario)
        values = metrics(fut, ref, _future_indicators(fut, history['preloaded_data']),
                         _residual_stock_2025(history, ref), fut_fibre)
        for name, series in values.items():
            frames.append(pd.DataFrame({'scenario': i, 'year': list(fut.dims['t'].items), 'metric': name,
                                        'value': series}))
        # Commercial and bulky waste at 0 is a scenario outcome (metric
        # stock_growth_shortfall_kt); clipping of any other flow is reported.
        clipped.append(sum(c.values.sum() for code, c in fut.clipped.items() if code != COMMERCIAL_BULKY))
    return pd.concat(frames, ignore_index=True), np.array(clipped)


def summary(results):
    sampled = results[results['scenario'] > 0].groupby(['metric', 'year'])['value']
    table = pd.DataFrame({
        'reference': results[results['scenario'] == 0].set_index(['metric', 'year'])['value'],
        'p5': sampled.quantile(0.05), 'p50': sampled.median(), 'p95': sampled.quantile(0.95),
        'min': sampled.min(), 'max': sampled.max(),
    })
    return table.reset_index()


def sensitivity(results, factors):
    rows = []
    sampled = factors[factors['scenario'] > 0].set_index('scenario')
    for (metric, year), group in results[(results['scenario'] > 0)
                                         & results['year'].isin(SENSITIVITY_YEARS)].groupby(['metric', 'year']):
        outcome = group.set_index('scenario')['value'].reindex(sampled.index)
        for factor in sampled.columns:
            rho = spearmanr(sampled[factor], outcome).statistic
            rows.append({'metric': metric, 'year': year, 'factor': factor, 'spearman': rho})
    return pd.DataFrame(rows)


def main():
    args = parse_arguments()
    logging.disable(logging.WARNING)
    history = prepare_history()
    scenarios = [Scenario.reference(history['hist'])] + sample_scenarios(args.n)
    start = time.time()
    results, clipped = run_scenarios(history, scenarios)
    shortfall = results[results['metric'] == 'stock_growth_shortfall_kt'].groupby('scenario')['value'].sum()
    print(f"[INFO] {len(scenarios)} scenarios in {time.time() - start:.1f} s; stock grows less than X5 in "
          f"{(shortfall > 1e-9).sum()}; other clipping in {(clipped > 1e-9).sum()} (max {clipped.max():.3g} kt)")
    factors = pd.DataFrame([{'scenario': i, **factor_table(s)} for i, s in enumerate(scenarios)])
    results.to_csv('output_files/future_scenarios.csv', index=False)
    factors.to_csv('output_files/future_scenarios_factors.csv', index=False)
    table = summary(results)
    table.to_csv('output_files/future_scenarios_summary.csv', index=False)
    sens = sensitivity(results, factors)
    sens.to_csv('output_files/future_scenarios_sensitivity.csv', index=False)
    print("[INFO] Wrote output_files/future_scenarios*.csv")
    pd.set_option('display.width', 250)
    print(table[table['year'].isin([2030, 2035, 2050])].round(3).to_string(index=False))


if __name__ == '__main__':
    main()
