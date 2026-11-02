#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loads the parameter tables in parameters/ and draws one Monte Carlo set of
values per iteration. Parameters whose value is still blank (status 'todo')
are left out of the drawn set, so any calculation that uses one crashes with
a KeyError instead of silently running on a missing value.
"""
import numpy as np
import pandas as pd
from scipy import stats

from calculations.sampling import is_perturbed, normal_score, quantile
from calculations.timeseries import AnchorSeries, GapNoise
from calculations.utils import YEARS

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

    def draw(self, seed, sim_id, probe=None):
        """
        Returns (params, dataset_noise, anchors) for MC iteration sim_id;
        iteration 0 is the deterministic baseline, where every input has its
        base value. Every item is drawn from its own random-number stream
        (item_rng), so a draw depends only on the seed, the iteration and the
        item, and through its quantile function (D39).

        params        : {parameter_id: value} for every global parameter with
                        a value, plus 'lifetime_mean_<stock>_<product>' and
                        'lifetime_shape_<stock>_<product>' for every lifetime
                        with a mean (the mean is drawn, the shape is fixed).
        dataset_noise : DatasetNoise of the iteration.
        anchors       : {parameter_id: AnchorSeries}; anchor points with the
                        same method_group share part of their draw (D39), and
                        the years between and outside them get gap noise (D30).

        params also holds 'gap_noise', the GapNoise of the iteration, for
        series built from yearly data with gaps.

        probe (sampling.Probe) sets one source to a fixed score in the
        deterministic iteration, for the contribution analysis.
        """
        deterministic = sim_id == 0

        def value(group, item_id, val, row, method_group=None, common_share=0.0):
            if not is_perturbed(row):
                return val
            z = normal_score(seed, sim_id, group, item_id, probe)
            if method_group:
                z_common = normal_score(seed, sim_id, 'anchor_group', method_group, probe)
                z = np.sqrt(common_share) * z_common + np.sqrt(1 - common_share) * z
            if deterministic and z == 0:
                return val
            return quantile(stats.norm.cdf(z), val, row)

        params = {}
        for _, row in self.global_params.dropna(subset=['value']).iterrows():
            params[row['parameter_id']] = value('global', row['parameter_id'], float(row['value']), row)

        for _, row in self.lifetimes.dropna(subset=['mean_years']).iterrows():
            key = f"{row['stock']}_{row['product']}"
            # The lifetime table's distribution_type is the lifetime
            # distribution itself; the mean is drawn by mean_distribution.
            mean_row = row.rename({'distribution_type': 'lifetime_distribution',
                                   'mean_distribution': 'distribution_type'})
            params[f'lifetime_mean_{key}'] = value('lifetime', key, float(row['mean_years']), mean_row)
            params[f'lifetime_shape_{key}'] = float(row['shape'])

        dataset_noise = DatasetNoise(self.datasets, seed, sim_id, probe)

        points = {}
        for _, row in self.anchor_table.dropna(subset=['value']).iterrows():
            group = row['method_group'] if isinstance(row['method_group'], str) else None
            anchor_id = f"{row['parameter_id']}@{int(row['year'])}"
            points.setdefault(row['parameter_id'], {})[int(row['year'])] = value(
                'anchor', anchor_id, float(row['value']), row, group, row['common_share'])
        gap_noise = GapNoise(seed, sim_id, params['gap_cv_interpolation'], params['gap_cv_extrapolation'],
                             params['gap_cv_cap'], probe)
        anchors = {name: AnchorSeries(name, values, gap_noise) for name, values in points.items()}
        params['gap_noise'] = gap_noise

        return params, dataset_noise, anchors


class DatasetNoise:
    """
    Multiplicative uncertainty factors for the datasets in one iteration
    (dataset_uncertainties.csv), 1 in the deterministic baseline.

    factor(name, part) is an array with one factor per year. A dataset with
    annual_draw = 'yes' (registered data and surveys, whose errors are mostly
    new each year) gets an independent factor for each year; the others one
    factor for all years, since their errors are mostly systematic. Each part
    of a dataset (e.g. import and export of one goods category) is drawn
    independently from the same row, so that errors in different parts are
    not forced to be identical.
    """

    def __init__(self, table, seed, sim_id, probe=None):
        self.rows = {str(row['dataset_name']).strip(): row for _, row in table.iterrows()}
        self.seed = seed
        self.sim_id = sim_id
        self.probe = probe

    def _draw(self, name, item_id):
        row = self.rows[name]
        if not is_perturbed(row):
            return 1.0
        z = normal_score(self.seed, self.sim_id, 'dataset', item_id, self.probe)
        if self.sim_id == 0 and z == 0:
            return 1.0
        return quantile(stats.norm.cdf(z), 1.0, row)

    def factor(self, name, part='', years=YEARS):
        if self.rows[name]['annual_draw'] == 'yes':
            return np.array([self._draw(name, f'{name}:{part}@{year}') for year in years])
        return np.full(len(years), self._draw(name, f'{name}:{part}'))
