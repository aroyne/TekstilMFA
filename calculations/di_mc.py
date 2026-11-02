#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DI (distribution: wholesale and retail) pool. Unsold goods donated are
clothing only and follow the clothing imports between and outside the
years the surveys cover (D27). Unsold goods discarded are a share of the
clothing, household textiles and footwear placed on the market (D38).
"""
import numpy as np

from calculations.system import clip_negative
from calculations.timeseries import interpolate
from calculations.trade import trade_kt
from calculations.utils import PRODUCTS, YEARS

UNSOLD_DESTROYED_PRODUCTS = ['CL', 'HT', 'FW']


def execute_calculations_di(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _finished_products_export_mc(mfa, preloaded_data, dataset_noise)
    _unsold_goods_donated_mc(mfa, anchors)
    _unsold_goods_discarded_mc(mfa, current_params)
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


def _unsold_goods_discarded_mc(mfa, current_params):
    """
    Unsold clothing, household textiles and footwear that producers and
    retailers send to incineration (D38): a share of what is placed on the
    market (registered imports plus finished goods made in Norway minus
    exports). The share is lognormal with median 1 % (an assumption close
    to the overstock found by Samfunnsøkonomisk analyse (2022), at least
    825 t or about 0.8 % of the clothing supply) and 95 % interval 0.2-5 %.
    The lower end is the survey minimums where the largest retailers did
    not report (95 t incinerated in 2018, Watson et al. 2020; 221 t in
    2022, Rubach et al. 2023), and the upper end reaches the EEA (2024)
    estimate that 4-9 % of textiles put on the market in Europe are
    destroyed unused. Destroyed goods are commercial waste and are not in
    the pick analyses of household waste, so they are not counted twice.
    Material recycling is not split out, so all of it goes to WM.RS. Large
    enterprises may not destroy unsold clothing and footwear from 19 July
    2026 (ESPR), which matters only for scenarios.
    """
    imports = mfa.flows['RW.RW-DI.RT-Finished textile products import-TOT'].values
    domestic_goods = mfa.flows['MA.TX-DI.RT-Domestic finished products-TOT'].values
    exports = mfa.flows['DI.RT-RW.RW-Export of finished textile products-TOT'].values
    on_market = imports + domestic_goods - exports
    flow = mfa.flows['DI.RT-WM.RS-Unsold goods discarded-TOT']
    flow.values[...] = 0.0
    for product in UNSOLD_DESTROYED_PRODUCTS:
        j = PRODUCTS.index(product)
        flow.values[:, j] = on_market[:, j] * current_params['unsold_destroyed_share']


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
    entirely to households. The institutional share of the other products is
    12 % (4-15 %), the Danish split used by Watson et al. 2020 and Rubach et
    al. 2023; no Norwegian statistic gives it. The lower bound is the share
    of clothing imported directly by businesses and the public sector outside
    wholesale and retail, 3-4 % of the import value in 2016-2024 (Eurostat
    ext_tec05, D36); the rest of their purchases goes through wholesale and
    cannot be separated. A negative balance is not physical and is
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
