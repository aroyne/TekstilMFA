#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loads the parameter tables in parameters/ and draws one Monte Carlo set of
values per iteration. Parameters whose value is still blank (status 'todo')
are left out of the drawn set, so any calculation that uses one crashes with
a KeyError instead of silently running on a missing value.
"""
import pandas as pd

from calculations.sampling import draw_perturbed_value
from calculations.timeseries import AnchorSeries, GapNoise

PARAM_DIR = 'parameters'
ANCHOR_VALUES = 'data_files/anchor_values.csv'


class Parameters:
    def __init__(self, param_dir=PARAM_DIR):
        self.global_params = pd.read_csv(f'{param_dir}/global_parameters.csv')
        # Anchor points for shares/rates (parameters/) and for observed
        # quantities from reports (data_files/anchor_values.csv) share one
        # format and are drawn the same way.
        self.anchor_table = pd.concat([
            pd.read_csv(f'{param_dir}/time_dependent_parameters.csv'),
            pd.read_csv(ANCHOR_VALUES),
        ], ignore_index=True)
        self.lifetimes = pd.read_csv(f'{param_dir}/lifetimes.csv')
        self.datasets = pd.read_csv(f'{param_dir}/dataset_uncertainties.csv', dtype={'dataset_name': str})
        self.hs_mapping = pd.read_csv(f'{param_dir}/hs_mapping.csv', dtype={'hs_prefix': str})
        # Fibre groups of import mass whose HS code states no fibre (D19);
        # fixed, without uncertainty bounds.
        self.fibre_composition = pd.read_csv(f'{param_dir}/fibre_composition.csv').set_index('product')
        # Main fibre stated by each HS8 code, built by scripts/build_hs_main_fibre.py.
        self.hs_main_fibre = pd.read_csv(f'{param_dir}/hs_main_fibre.csv', dtype=str)

    def draw(self, rng, deterministic):
        """
        Returns (params, dataset_noise, anchors) for one MC iteration.

        params        : {parameter_id: value} for every global parameter with
                        a value, plus 'lifetime_mean_<stock>_<product>' and
                        'lifetime_shape_<stock>_<product>' for every lifetime
                        with a mean (the mean is drawn, the shape is fixed).
        dataset_noise : {dataset_name: multiplicative factor}, 1.0 in the
                        deterministic round. One factor per dataset and
                        iteration, i.e. fully correlated across years.
        anchors       : {parameter_id: AnchorSeries}; every anchor point is
                        drawn independently of the others, and the years
                        between and outside them get gap noise (D30).

        params also holds 'gap_noise', the GapNoise of the iteration, for
        series built from yearly data with gaps.
        """
        params = {}
        for _, row in self.global_params.dropna(subset=['value']).iterrows():
            val = float(row['value'])
            if not deterministic:
                val = draw_perturbed_value(rng, val, row['lower_bound'], row['upper_bound'],
                                           row['uncertainty_type'], row['distribution_type'])
            params[row['parameter_id']] = val

        for _, row in self.lifetimes.dropna(subset=['mean_years']).iterrows():
            mean = float(row['mean_years'])
            if not deterministic:
                mean = draw_perturbed_value(rng, mean, row['lower_bound'], row['upper_bound'],
                                            row['uncertainty_type'], 'PERT')
            key = f"{row['stock']}_{row['product']}"
            params[f'lifetime_mean_{key}'] = mean
            params[f'lifetime_shape_{key}'] = float(row['shape'])

        dataset_noise = {}
        for _, row in self.datasets.iterrows():
            factor = 1.0
            if not deterministic:
                factor = draw_perturbed_value(rng, 1.0, row['lower_bound'], row['upper_bound'],
                                              row['uncertainty_type'], row['distribution_type'])
            dataset_noise[str(row['dataset_name']).strip()] = factor

        points = {}
        for _, row in self.anchor_table.dropna(subset=['value']).iterrows():
            val = float(row['value'])
            if not deterministic:
                val = draw_perturbed_value(rng, val, row['lower_bound'], row['upper_bound'],
                                           row['uncertainty_type'], row['distribution_type'])
            points.setdefault(row['parameter_id'], {})[int(row['year'])] = val
        gap_noise = GapNoise(rng, deterministic, params['gap_cv_interpolation'], params['gap_cv_extrapolation'],
                             params['gap_cv_cap'])
        anchors = {name: AnchorSeries(name, values, gap_noise) for name, values in points.items()}
        params['gap_noise'] = gap_noise

        return params, dataset_noise, anchors
