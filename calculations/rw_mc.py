#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RW (rest of the world) pool: flows from abroad into the Norwegian system.
"""
import numpy as np

from calculations.timeseries import interpolate
from calculations.trade import import_unit_value, trade_kt
from calculations.utils import PRODUCTS, YEARS


def execute_calculations_rw(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _finished_products_import_mc(mfa, preloaded_data, dataset_noise)
    _private_imports_mc(mfa, preloaded_data, current_params, dataset_noise)
    _direct_online_imports_mc(mfa, anchors)


def _finished_products_import_mc(mfa, preloaded_data, dataset_noise):
    """Registered imports of finished goods, SSB 08801."""
    flow = mfa.flows['RW.RW-DI.RT-Finished textile products import-TOT']
    flow.values[...] = trade_kt(preloaded_data, dataset_noise, True, 'finished', PRODUCTS)


def _private_imports_mc(mfa, preloaded_data, current_params, dataset_noise):
    """
    Clothing and shoes bought on cross-border day trips (D16). SSB reports
    shopping in NOK at Swedish retail prices; it is converted to mass with the
    customs import value per kg of CL+FW times a retail markup, and split
    between CL and FW by their shares of registered import mass. The
    statistics cover clothing and shoes only, so other products are 0.
    """
    flow = mfa.flows['RW.RW-US.HH-Private imports-TOT']

    # 'crossborder' <- data_files/SSB_grensehandel_05678_14221.csv:
    # day-trip shopping in total (mill. NOK, 2004-2022) and for clothing and
    # shoes (mill. NOK, 2023-2025)
    crossborder = preloaded_data['crossborder']
    noise_val = dataset_noise['grensehandel']
    clothing_share = current_params['crossborder_clothing_share']
    markup = current_params['retail_markup']

    mill_nok = np.full(len(YEARS), np.nan)
    for i, year in enumerate(YEARS):
        if year in crossborder['clothing']:
            mill_nok[i] = crossborder['clothing'][year]
        elif year in crossborder['total']:
            mill_nok[i] = crossborder['total'][year] * clothing_share
    # mill. NOK / (NOK/kg) = million kg = kt
    total_kt = mill_nok * noise_val / (import_unit_value(preloaded_data, ['CL', 'FW']) * markup)
    # Before the SSB series starts (2004) the mass is held at the first
    # year's level (D16).
    first = YEARS.index(min(crossborder['total']))
    total_kt[:first] = total_kt[first]
    imports = trade_kt(preloaded_data, dataset_noise, True, 'finished', ['CL', 'FW'])
    split = imports / imports.sum(axis=1, keepdims=True)

    flow.values[...] = 0.0
    for j, product in enumerate(['CL', 'FW']):
        flow.values[:, PRODUCTS.index(product)] = total_kt * split[:, j]


def _direct_online_imports_mc(mfa, anchors):
    """
    Low-value parcels bought directly from foreign web shops, which are not in
    08801 under their HS codes (D7). Official VOEC data 2022-2025, one
    estimate for 2018, and zero around 2000. VOEC figures exist for clothing
    (HS 61+62) and household textiles (HS 63) only, so other products are 0.
    """
    flow = mfa.flows['RW.RW-US.HH-Direct online imports-TOT']
    flow.values[...] = 0.0
    for product, anchor_id in (('CL', 'online_direct_CL'), ('HT', 'online_direct_HT')):
        flow.values[:, PRODUCTS.index(product)] = interpolate(anchors[anchor_id])
