#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI entry point and Monte Carlo driver for the textile MFA: loads data and
parameters once, builds the flodym system from the register once, and runs
nsim iterations over the selected pools (iteration 0 is the deterministic
baseline). Every iteration resets all flows to NaN, lets the pools assign
them, and closes the system (flow check, stocks, mass balance). The fibre
layer (D19) then distributes the closed TOT system over materials in a
second system. Results are kept as one array per flow and written as
per-flow, per-product, per-year summary statistics to output_files/
(MC_summary.csv for TOT, MC_summary_fibre.csv per material).

Usage: python main_mc.py --pool all --nsim 1000 [--seed 1] [--export-raw-mc]
"""
import argparse
import importlib
import time

import numpy as np
import pandas as pd

from calculations.fibre_layer import compute_fibre_layer
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


COLUMN_OF_DIM = {'t': 'year', 'p': 'product', 'g': 'product', 'm': 'material'}
KEY_COLUMNS = ['flow_name', 'product', 'material', 'year']


def record(store, arrays, sim_id, n_runs):
    for name, arr in arrays.items():
        if name not in store:
            store[name] = (arr.copy(), np.empty((n_runs,) + arr.values.shape))
        store[name][1][sim_id] = arr.values


def to_long(name, arr, values):
    """
    Long table of one output: values has shape (iteration, *arr.dims). The
    columns are year, 'product' (product or product group, 'ALL' for flows
    without a product dimension) and, in the fibre layer, 'material'.
    """
    letters = arr.dims.letters
    grids = np.meshgrid(*[np.asarray(arr.dims[l].items) for l in letters], indexing='ij')
    frame = pd.DataFrame({COLUMN_OF_DIM[l]: g.ravel() for l, g in zip(letters, grids)})
    if 'product' not in frame:
        frame['product'] = 'ALL'
    frame['flow_name'] = name
    return values.reshape(values.shape[0], -1), frame[[c for c in KEY_COLUMNS if c in frame]]


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
    summary = pd.concat(frames)
    return summary.sort_values([c for c in KEY_COLUMNS if c in summary]).reset_index(drop=True)


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
    fibre = make_system(fibre=True)

    n_runs = args.nsim + 1
    store = {}  # name -> (FlodymArray of iteration 0, array (iteration, ...))
    fibre_store = {}
    start = time.time()
    for sim_id in range(n_runs):
        current_params, dataset_noise, anchors = params.draw(rng, deterministic=(sim_id == 0))
        run_pools(mfa, pools, preloaded_data, current_params, dataset_noise, anchors)
        if closed:
            close(mfa)
            stock_model = compute_fibre_layer(fibre, mfa, preloaded_data, current_params, params.fibre_composition)
            record(fibre_store, {**outputs(fibre, closed), **stock_model}, sim_id, n_runs)
            record(store, {name: arr.sum_over(('m',)) for name, arr in stock_model.items()}, sim_id, n_runs)
        record(store, outputs(mfa, closed), sim_id, n_runs)
    print(f"[INFO] {args.nsim} MC iterations + baseline in {time.time() - start:.1f} s")

    if not closed:
        store = {name: v for name, v in store.items() if not np.isnan(v[1]).all()}
    summarise(store).to_csv('output_files/MC_summary.csv', index=False)
    print("[INFO] Wrote output_files/MC_summary.csv")
    if closed:
        summarise(fibre_store).to_csv('output_files/MC_summary_fibre.csv', index=False)
        print("[INFO] Wrote output_files/MC_summary_fibre.csv")
    if args.export_raw_mc:
        raw_table(store).to_csv('output_files/MC_Raw_Simulations.csv.gz', index=False)


if __name__ == '__main__':
    main()
