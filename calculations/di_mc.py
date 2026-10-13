#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DI (distribution: wholesale and retail) pool. Unsold goods are clothing
only and follow the clothing imports between and outside the years the
surveys cover (D27).
"""
import numpy as np

from calculations.system import clip_negative
from calculations.timeseries import interpolate
from calculations.trade import trade_kt
from calculations.utils import PRODUCTS, YEARS


def execute_calculations_di(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _finished_products_export_mc(mfa, preloaded_data, dataset_noise)
    _unsold_goods_donated_mc(mfa, anchors)
    _unsold_goods_discarded_mc(mfa, anchors)
    _sales_to_users_mc(mfa, current_params)


def _per_clothing_import(mfa, anchor):
    """
    Array (year, product) with the anchored mass (kt) in clothing: the mass
    per kt of clothing imports in the anchor years, interpolated, times the
    clothing imports of each year.
    """
    clothing = mfa.flows['RW.RW-DI.RT-Finished textile products import-TOT'].values[:, PRODUCTS.index('CL')]
    ratio = interpolate({year: kt / clothing[YEARS.index(year)] for year, kt in anchor.items()}, noise=anchor)
    values = np.zeros((len(YEARS), len(PRODUCTS)))
    values[:, PRODUCTS.index('CL')] = ratio * clothing
    return values


def _unsold_goods_donated_mc(mfa, anchors):
    """
    Unsold clothing that producers and retailers give to collectors. One
    collector received about 600 t in 2018, including from some of the
    largest retailers (Watson et al. 2020), and collectors reported about
    200 t in 2022 (Rubach et al. 2023). Most of it is exported to countries
    where the brand has no shops, i.e. with the export of used textiles
    (HS 6309), so it is subtracted from collection from households.
    """
    mfa.flows['DI.RT-CO.CO-Unsold goods donated-TOT'].values[...] = (
        _per_clothing_import(mfa, anchors['unsold_donated']))


def _unsold_goods_discarded_mc(mfa, anchors):
    """
    Unsold clothing that producers and retailers send to incineration or
    recycling, as minimums from surveys where the largest retailers did not
    report: 95 t incinerated in 2018 (Watson et al. 2020) and 221 t handled
    other than by donation in 2022 (Rubach et al. 2023). Material recycling
    is not split out yet, so all of it goes to WM.RS. The EEA (2024)
    estimates that 4-9 % of textiles put on the market in Europe are
    destroyed unused, which would be 4-10 kt a year in Norway; that is used
    for sensitivity and discussion only.
    """
    mfa.flows['DI.RT-WM.RS-Unsold goods discarded-TOT'].values[...] = (
        _per_clothing_import(mfa, anchors['unsold_discarded']))


def _finished_products_export_mc(mfa, preloaded_data, dataset_noise):
    """
    Registered exports of finished goods, SSB 08801. Export from DI.RT covers
    both re-export and export of domestically manufactured products (D6).
    """
    flow = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT']
    flow.values[...] = trade_kt(preloaded_data, dataset_noise, False, 'finished', PRODUCTS)


def _sales_to_users_mc(mfa, current_params):
    """
    Balance of DI.RT per product: registered imports plus finished goods
    and hand knitting yarn made in Norway minus exports and unsold goods,
    split between households and institutions/businesses. Sacks (SA) are packaging
    used by businesses (D13) and go entirely to US.IC; retail yarn (YA) goes
    entirely to households. A negative balance is not physical and is
    clipped at 0; the clipped mass is recorded and reported on the flow
    pages.
    """
    imports = mfa.flows['RW.RW-DI.RT-Finished textile products import-TOT'].values
    exports = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT'].values
    domestic_yarn = mfa.flows['MA.FI-DI.RT-Domestic hand knitting yarn-TOT'].values
    domestic_goods = mfa.flows['MA.TX-DI.RT-Domestic finished products-TOT'].values
    unsold = (mfa.flows['DI.RT-CO.CO-Unsold goods donated-TOT'].values
              + mfa.flows['DI.RT-WM.RS-Unsold goods discarded-TOT'].values)
    balance = imports + domestic_goods + domestic_yarn - exports - unsold

    institutional_share = current_params['institutional_share']
    share_ic = np.array([1.0 if p == 'SA' else 0.0 if p == 'YA' else institutional_share for p in PRODUCTS])
    clip_negative(mfa, 'DI.RT-US.HH-Sales to households-TOT', balance * (1.0 - share_ic))
    clip_negative(mfa, 'DI.RT-US.IC-Sales to institutions and businesses-TOT', balance * share_ic)
