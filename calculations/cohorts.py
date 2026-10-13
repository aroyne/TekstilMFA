#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inflow-driven cohort model of goods in use, in households (US.HH) or
institutions and businesses (US.IC) (D20): Weibull lifetimes per stock and
product from parameters/lifetimes.csv, inflow counted as
arriving in the middle of the year (flodym's default). The inflow before
1988 is held at the 1988 level and composition from 1950 (D2), so the
stock in 1988 includes the spin-up cohorts.
"""
import math

import flodym as fd
import numpy as np

from calculations.utils import START_YEAR, YEARS

SPINUP_START = 1950
DSM_YEARS = list(range(SPINUP_START, YEARS[-1] + 1))
N_SPINUP = START_YEAR - SPINUP_START


def use_cohorts(inflow, products, current_params, stock='US.HH'):
    """
    inflow: array (year, product, material) over YEARS; stock: 'US.HH' or
    'US.IC', which selects the lifetimes. Returns
    {'outflow', 'stock'} as arrays (year, product, material) over YEARS, and
    'stock_1987' as an array (product, material).
    """
    inflow = np.concatenate([np.repeat(inflow[:1], N_SPINUP, axis=0), inflow], axis=0)
    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=DSM_YEARS),
        fd.Dimension(letter='p', name='Product', dtype=str, items=products),
        fd.Dimension(letter='m', name='Material', dtype=int, items=list(range(inflow.shape[2]))),
    ])
    shape = np.array([current_params[f'lifetime_shape_{stock}_{p}'] for p in products])
    mean = np.array([current_params[f'lifetime_mean_{stock}_{p}'] for p in products])
    scale = mean / np.array([math.gamma(1.0 + 1.0 / k) for k in shape])
    lifetime = fd.WeibullLifetime(
        dims=dims,
        weibull_shape=fd.Parameter(dims=dims[('p',)], values=shape),
        weibull_scale=fd.Parameter(dims=dims[('p',)], values=scale),
    )
    dsm = fd.InflowDrivenDSM(name=f'{stock} cohorts', dims=dims, lifetime_model=lifetime,
                             inflow=fd.StockArray(dims=dims, values=inflow))
    dsm.compute()
    return {
        'outflow': dsm.outflow.values[N_SPINUP:],
        'stock': dsm.stock.values[N_SPINUP:],
        'stock_1987': dsm.stock.values[N_SPINUP - 1],
    }
