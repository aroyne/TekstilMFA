#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI entry point and Monte Carlo driver for the textile MFA: loads data and
parameters once, runs nsim iterations over the selected pools (iteration 0
is the deterministic baseline), and writes per-flow, per-product, per-year
summary statistics to output_files/.

Usage: python main_mc.py --pool all --nsim 1000 [--seed 1] [--export-raw-mc]
"""
import argparse
import importlib
import time

import numpy as np
import pandas as pd

from calculations.params import Parameters
from data_loader import load_all_data

ALL_POOLS = ['rw', 'di']   # extended as pool modules are added


def parse_arguments():
    parser = argparse.ArgumentParser(description="Monte Carlo framework for the textile MFA.")
    parser.add_argument('--pool', type=str, required=True, help="Pool(s) to run, e.g. 'rw,di' or 'all'")
    parser.add_argument('--nsim', type=int, default=100, help="Number of MC iterations")
    parser.add_argument('--seed', type=int, default=None, help="RNG seed for reproducible runs")
    parser.add_argument('--export-raw-mc', action='store_true',
                        help="Also write every iteration to output_files/MC_Raw_Simulations.csv.gz")
    return parser.parse_args()


def summarise(df_all):
    """Median and 95 % interval per flow, product and year, plus the deterministic value."""
    df_mc = df_all[df_all['sim_id'] > 0]
    grouped = df_mc.groupby(['flow_name', 'product', 'year'])['value']
    summary = grouped.agg(
        median='median',
        p2_5=lambda v: v.quantile(0.025),
        p97_5=lambda v: v.quantile(0.975),
        n='count',
    ).reset_index()
    deterministic = (df_all[df_all['sim_id'] == 0]
                     .set_index(['flow_name', 'product', 'year'])[['value', 'comment', 'data_sources']]
                     .rename(columns={'value': 'deterministic'}))
    return summary.join(deterministic, on=['flow_name', 'product', 'year'])


def main():
    args = parse_arguments()
    pools = ALL_POOLS if args.pool == 'all' else [p.strip() for p in args.pool.lower().split(',')]
    rng = np.random.default_rng(args.seed)

    params = Parameters()
    preloaded_data = load_all_data(pools, params)

    records = []
    start = time.time()
    for sim_id in range(args.nsim + 1):
        current_params, dataset_noise = params.draw(rng, deterministic=(sim_id == 0))
        for pool in pools:
            module = importlib.import_module(f'calculations.{pool}_mc')
            pool_results = getattr(module, f'execute_calculations_{pool}')(preloaded_data, current_params, dataset_noise)
            for rec in pool_results:
                rec['sim_id'] = sim_id
            records.extend(pool_results)
    print(f"[INFO] {args.nsim} MC iterations + baseline in {time.time() - start:.1f} s")

    df_all = pd.DataFrame(records)
    summarise(df_all).to_csv('output_files/MC_summary.csv', index=False)
    print("[INFO] Wrote output_files/MC_summary.csv")
    if args.export_raw_mc:
        df_all.to_csv('output_files/MC_Raw_Simulations.csv.gz', index=False)


if __name__ == '__main__':
    main()
