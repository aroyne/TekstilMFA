#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DI (distribution: wholesale and retail) pool.
"""
import numpy as np

from calculations.trade import trade_kt
from calculations.utils import PRODUCTS, YEARS


def execute_calculations_di(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _finished_products_export_mc(mfa, preloaded_data, dataset_noise)
    _sales_to_users_mc(mfa, current_params)


def _finished_products_export_mc(mfa, preloaded_data, dataset_noise):
    """
    Registered exports of finished goods, SSB 08801. Export from DI.RT covers
    both re-export and export of domestically manufactured products (D6).
    """
    flow = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT']
    flow.values[...] = trade_kt(preloaded_data, dataset_noise, False, 'finished', PRODUCTS)


def _sales_to_users_mc(mfa, current_params):
    """
    Balance of DI.RT per product: registered imports minus exports, split
    between households and institutions/businesses. Sacks (SA) are packaging
    used by businesses (D13) and go entirely to US.IC. Domestic manufacturing
    (MA.TX) and unsold goods are not yet included.
    """
    imports = mfa.flows['RW.RW-DI.RT-Finished textile products import-TOT'].values
    exports = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT'].values
    net = imports - exports
    if (net < 0).any():
        t, p = np.argwhere(net < 0)[0]
        raise ValueError(f"Negative DI.RT balance for {PRODUCTS[p]} in {YEARS[t]}: {net[t, p]:.3f} kt")

    institutional_share = current_params['institutional_share']
    share_ic = np.array([1.0 if p == 'SA' else institutional_share for p in PRODUCTS])
    mfa.flows['DI.RT-US.HH-Sales to households-TOT'].values[...] = net * (1.0 - share_ic)
    mfa.flows['DI.RT-US.IC-Sales to institutions and businesses-TOT'].values[...] = net * share_ic
