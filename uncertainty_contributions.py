#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Which uncertainty sources drive the uncertainty of each flow, and how much
(phase A, D39).

A first-order analysis around the deterministic run:

1. A traced run (sampling.Probe without a target) records every uncertain
   source the model asks for: global parameters, lifetimes, dataset factors
   (one per year for annual datasets), anchor points, the shared factor of
   each anchor method group, and gap noise.
2. Each source is set on its own to its 2.5th and 97.5th percentile
   (standard-normal score -1.96 and +1.96), with all other inputs at their
   base values. Half the swing divided by 1.96 is the source's standard
   deviation in the flow, and its square the contribution to the variance.
3. Contributions are summed per source label (all years of an annual
   dataset part, all points of an anchor series, all gaps of a series) and
   shared out per flow and year.

The sources are drawn independently in the Monte Carlo, so the
contributions add up to first order. Non-linear effects are not included:
residuals near zero or clipped at zero, skewed sources, and products of
uncertain factors. 'linear_half_width' (1.96 times the root of the summed
variance) can be compared with the Monte Carlo interval to see how far the
first-order picture holds.

Writes output_files/MC_uncertainty_contributions.csv, read by
report_generator.py for the uncertainty section of each flow page.

Usage: python uncertainty_contributions.py
"""
import time
from collections import defaultdict

import numpy as np
import pandas as pd

from calculations.fibre_layer import compute_fibre_layer
from calculations.params import Parameters
from calculations.sampling import DEFAULT_SEED, Probe, Z95
from calculations.system import close, make_system
from data_loader import load_all_data
from main_mc import ALL_POOLS, outputs, run_pools

OUTPUT = 'output_files/MC_uncertainty_contributions.csv'
# Sources below this share of the variance in a flow and year are left out of the file.
MIN_SHARE = 0.005


def run_once(params, preloaded_data, mfa, fibre, probe):
    """{flow name: array (year,)} summed over products and materials, for one deterministic run."""
    current_params, dataset_noise, anchors = params.draw(DEFAULT_SEED, 0, probe)
    run_pools(mfa, ALL_POOLS, preloaded_data, current_params, dataset_noise, anchors)
    close(mfa)
    stock_model = compute_fibre_layer(fibre, mfa, preloaded_data, current_params, params.fibre_composition)
    arrays = {**outputs(mfa, True), **stock_model}
    return {name: arr.sum_to(('t',)).values.copy() for name, arr in arrays.items()}


def label(group, item_id, group_members):
    """Name a source is reported under: one per dataset part, anchor series, gap series or parameter."""
    if group == 'dataset':
        return item_id.split('@')[0].rstrip(':')
    if group == 'anchor':
        return item_id.split('@')[0]
    if group == 'anchor_group':
        members = group_members[item_id]
        return members[0] if len(members) == 1 else f'{item_id} (shared method)'
    if group == 'gap':
        return f"gap: {item_id.split(':')[0]}"
    if group == 'lifetime':
        return f'lifetime_mean_{item_id}'
    return item_id


def main():
    start = time.time()
    params = Parameters()
    preloaded_data = load_all_data(ALL_POOLS, params)
    mfa = make_system()
    fibre = make_system(fibre=True)

    trace = Probe()
    base = run_once(params, preloaded_data, mfa, fibre, trace)
    years = list(mfa.dims['t'].items)
    anchors = params.anchor_table
    group_members = {g: sorted(set(anchors.loc[anchors['method_group'] == g, 'parameter_id']))
                     for g in anchors['method_group'].dropna().unique() if g}
    sources = sorted(trace.requested, key=str)
    print(f"[INFO] {len(sources)} uncertainty sources")

    variance = defaultdict(lambda: {name: np.zeros(len(years)) for name in base})
    for i, (group, item_id) in enumerate(sources):
        high = run_once(params, preloaded_data, mfa, fibre, Probe(group, item_id, Z95))
        low = run_once(params, preloaded_data, mfa, fibre, Probe(group, item_id, -Z95))
        target = variance[label(group, item_id, group_members)]
        for name in base:
            target[name] += ((high[name] - low[name]) / 2 / Z95) ** 2
        if (i + 1) % 100 == 0:
            print(f"[INFO] {i + 1} of {len(sources)} sources, {time.time() - start:.0f} s")

    total = {name: sum(v[name] for v in variance.values()) for name in base}
    rows = []
    for source, by_flow in variance.items():
        for name, var in by_flow.items():
            for j, year in enumerate(years):
                if total[name][j] > 0 and var[j] / total[name][j] >= MIN_SHARE:
                    rows.append({'flow_name': name, 'year': year, 'source': source,
                                 'share': var[j] / total[name][j], 'half_width': Z95 * np.sqrt(var[j]),
                                 'linear_half_width': Z95 * np.sqrt(total[name][j]),
                                 'deterministic': base[name][j]})
    result = pd.DataFrame(rows).sort_values(['flow_name', 'year', 'share'], ascending=[True, True, False])
    result.to_csv(OUTPUT, index=False)
    print(f"[INFO] Wrote {OUTPUT} ({len(result)} rows) in {time.time() - start:.0f} s")


if __name__ == '__main__':
    main()
