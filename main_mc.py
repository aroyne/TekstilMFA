#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI entry point and Monte Carlo driver for the textile MFA: loads data and
parameters once, builds the flodym system from the register once, and runs
nsim iterations over the selected pools (iteration 0 is the deterministic
baseline). Every iteration resets all flows to NaN, lets the pools assign
them, and closes the system (flow check, stocks, mass balance). Results are
kept as one array per flow and written as per-flow, per-product, per-year
summary statistics to output_files/.

Usage: python main_mc.py --pool all --nsim 1000 [--seed 1] [--export-raw-mc]
"""
import argparse
import importlib
import time

import numpy as np
import pandas as pd

from calculations.params import Parameters
from calculations.system import close, load_register, make_system, reset, stock_change
from data_loader import load_all_data

# Pools run in this order within each iteration: a pool may read flows
# assigned by the pools before it (goods flow downstream).
ALL_POOLS = ['rw', 'di', 'co', 'us', 'wm']


def parse_arguments():
    parser = argparse.ArgumentParser(description="Monte Carlo framework for the textile MFA.")
    parser.add_argument('--pool', type=str, required=True, help="Pool(s) to run, e.g. 'rw,di' or 'all'")
    parser.add_argument('--nsim', type=int, default=100, help="Number of MC iterations")
    parser.add_argument('--seed', type=int, default=None, help="RNG seed for reproducible runs")
    parser.add_argument('--export-raw-mc', action='store_true',
                        help="Also write every iteration to output_files/MC_Raw_Simulations.csv.gz")
    return parser.parse_args()


def run_pools(mfa, pools, preloaded_data, current_params, dataset_noise, anchors):
    reset(mfa)
    for pool in pools:
        module = importlib.import_module(f'calculations.{pool}_mc')
        getattr(module, f'execute_calculations_{pool}')(mfa, preloaded_data, current_params, dataset_noise, anchors)


def outputs(mfa, closed):
    """
    {name: FlodymArray} of everything reported: all flows, and when the
    system is closed the stock change of every in-use stock (named like a
    flow from the process to itself).
    """
    result = dict(mfa.flows)
    if closed:
        processes, _ = load_register()
        for code in processes.loc[processes['has_stock'] == 'yes', 'code']:
            if code in mfa.stocks:
                result[f'{code}-{code}-Stock change-TOT'] = stock_change(mfa, code)
    return result


def to_long(name, arr, values):
    """
    Long table of one output: values has shape (..., year[, product]) matching
    arr.dims. 'product' is the product or product group, or 'ALL' for flows
    without a product dimension.
    """
    letters = arr.dims.letters
    years = arr.dims['t'].items
    product_letter = next((l for l in letters if l in ('p', 'g')), None)
    products = arr.dims[product_letter].items if product_letter else ['ALL']
    lead = values.shape[:values.ndim - len(letters)]
    flat = values.reshape(lead + (len(years), len(products)))
    year_col = np.repeat(years, len(products))
    product_col = np.tile(products, len(years))
    return flat.reshape(lead + (-1,)), pd.DataFrame({'flow_name': name, 'product': product_col, 'year': year_col})


def summarise(store):
    """Median and 95 % interval over iterations 1..n, plus the deterministic value."""
    frames = []
    for name, (arr, runs) in store.items():
        flat, frame = to_long(name, arr, runs)
        mc = flat[1:]
        frame['median'] = np.median(mc, axis=0)
        frame['p2_5'] = np.quantile(mc, 0.025, axis=0)
        frame['p97_5'] = np.quantile(mc, 0.975, axis=0)
        frame['n'] = mc.shape[0]
        frame['deterministic'] = flat[0]
        frames.append(frame)
    return pd.concat(frames).sort_values(['flow_name', 'product', 'year']).reset_index(drop=True)


def raw_table(store):
    frames = []
    for name, (arr, runs) in store.items():
        flat, frame = to_long(name, arr, runs)
        for sim_id, values in enumerate(flat):
            frames.append(frame.assign(sim_id=sim_id, value=values))
    return pd.concat(frames, ignore_index=True)


def main():
    args = parse_arguments()
    pools = ALL_POOLS if args.pool == 'all' else [p.strip() for p in args.pool.lower().split(',')]
    # With a subset of pools some flows stay unset, so the system cannot be
    # closed and only the flows that were assigned are reported.
    closed = pools == ALL_POOLS
    rng = np.random.default_rng(args.seed)

    params = Parameters()
    preloaded_data = load_all_data(pools, params)
    mfa = make_system()

    n_runs = args.nsim + 1
    store = {}  # name -> (FlodymArray of iteration 0, array (iteration, ...))
    start = time.time()
    for sim_id in range(n_runs):
        current_params, dataset_noise, anchors = params.draw(rng, deterministic=(sim_id == 0))
        run_pools(mfa, pools, preloaded_data, current_params, dataset_noise, anchors)
        if closed:
            close(mfa)
        for name, arr in outputs(mfa, closed).items():
            if name not in store:
                store[name] = (arr.copy(), np.empty((n_runs,) + arr.values.shape))
            store[name][1][sim_id] = arr.values
    print(f"[INFO] {args.nsim} MC iterations + baseline in {time.time() - start:.1f} s")

    if not closed:
        store = {name: v for name, v in store.items() if not np.isnan(v[1]).all()}
    summarise(store).to_csv('output_files/MC_summary.csv', index=False)
    print("[INFO] Wrote output_files/MC_summary.csv")
    if args.export_raw_mc:
        raw_table(store).to_csv('output_files/MC_Raw_Simulations.csv.gz', index=False)


if __name__ == '__main__':
    main()
