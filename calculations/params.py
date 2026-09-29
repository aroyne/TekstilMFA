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

PARAM_DIR = 'parameters'


class Parameters:
    def __init__(self, param_dir=PARAM_DIR):
        self.global_params = pd.read_csv(f'{param_dir}/global_parameters.csv')
        self.time_params = pd.read_csv(f'{param_dir}/time_dependent_parameters.csv')
        self.lifetimes = pd.read_csv(f'{param_dir}/lifetimes.csv')
        self.datasets = pd.read_csv(f'{param_dir}/dataset_uncertainties.csv', dtype={'dataset_name': str})
        self.hs_mapping = pd.read_csv(f'{param_dir}/hs_mapping.csv', dtype={'hs_prefix': str})

    def draw(self, rng, deterministic):
        """
        Returns (params, dataset_noise) for one MC iteration.

        params        : {parameter_id: value} for every global parameter with
                        a value.
        dataset_noise : {dataset_name: multiplicative factor}, 1.0 in the
                        deterministic round. One factor per dataset and
                        iteration, i.e. fully correlated across years.
        """
        params = {}
        for _, row in self.global_params.dropna(subset=['value']).iterrows():
            val = float(row['value'])
            if not deterministic:
                val = draw_perturbed_value(rng, val, row['lower_bound'], row['upper_bound'],
                                           row['uncertainty_type'], row['distribution_type'])
            params[row['parameter_id']] = val

        dataset_noise = {}
        for _, row in self.datasets.iterrows():
            factor = 1.0
            if not deterministic:
                factor = draw_perturbed_value(rng, 1.0, row['lower_bound'], row['upper_bound'],
                                              row['uncertainty_type'], row['distribution_type'])
            dataset_noise[str(row['dataset_name']).strip()] = factor

        return params, dataset_noise
