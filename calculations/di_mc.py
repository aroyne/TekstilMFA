#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DI (distribution: wholesale and retail) pool.
"""
import numpy as np

from calculations.trade import trade_kt
from calculations.utils import PRODUCTS


def execute_calculations_di(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _finished_products_export_mc(mfa, preloaded_data, dataset_noise)
    _sales_to_users_mc(mfa, current_params)


def _finished_products_export_mc(mfa, preloaded_data, dataset_noise):
    """
    Registered exports of finished goods, SSB 08801. Export from DI.RT covers
    both re-export and export of domestically manufactured products (D6).
    In a year where exports of a product exceed what DI.RT has, they are
    reduced by the deficit (see _sales_to_users_mc).
    """
    flow = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT']
    flow.values[...] = trade_kt(preloaded_data, dataset_noise, False, 'finished', PRODUCTS)


def _sales_to_users_mc(mfa, current_params):
    """
    Balance of DI.RT per product: registered imports plus hand knitting yarn
    spun in Norway minus exports, split between households and
    institutions/businesses. Sacks (SA) are packaging
    used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
    entirely to households. Other domestic manufacturing (MA.TX) and unsold
    goods are not yet included. A negative balance is not physical: sales
    are clipped at 0 and exports of the product are reduced by the deficit.
    """
    imports = mfa.flows['RW.RW-DI.RT-Finished textile products import-TOT'].values
    exports = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT'].values
    domestic_yarn = mfa.flows['MA.FI-DI.RT-Domestic hand knitting yarn-TOT'].values
    balance = imports + domestic_yarn - exports
    net = np.clip(balance, 0.0, None)
    mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT'].values[...] += np.clip(balance, None, 0.0)

    institutional_share = current_params['institutional_share']
    share_ic = np.array([1.0 if p == 'SA' else 0.0 if p == 'YA' else institutional_share for p in PRODUCTS])
    mfa.flows['DI.RT-US.HH-Sales to households-TOT'].values[...] = net * (1.0 - share_ic)
    mfa.flows['DI.RT-US.IC-Sales to institutions and businesses-TOT'].values[...] = net * share_ic
