#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loads every source data file once, before the MC loop, and returns them in
one dict keyed by a short data key. DATA_MAP lists which pools need each
file, so a run of a single pool only loads what it uses. Every file is
described in DATA_SOURCES.md.
"""
import pandas as pd

from calculations.fibre_layer import aggregate_by_fibre_class
from calculations.trade import aggregate_trade, map_hs_to_product
from calculations.utils import PRODUCTS


def _load_trade_textiles(path, hs_mapping):
    df = pd.read_csv(path, sep=';', header=None, dtype=str)
    df.columns = ['year', 'impeks', 'HS_code', 'country', 'unit_code', 'amount', 'supp_quantity', 'value_nok']
    df['HS8'] = df['HS_code'].str.strip().str.split('_').str[0].str.zfill(8)
    df['year'] = df['year'].astype(int)
    df['impeks'] = df['impeks'].astype(int)
    for col in ('amount', 'supp_quantity', 'value_nok'):
        df[col] = pd.to_numeric(df[col])
    return map_hs_to_product(df, hs_mapping)


def _load_crossborder(path, hs_mapping):
    """{'total': {year: mill. NOK}, 'clothing': {year: mill. NOK}}"""
    df = pd.read_csv(path)
    total = df[df['series'] == 'total']
    clothing = df[df['series'] == 'clothing_and_shoes']
    return {
        'total': dict(zip(total['year'], total['mill_nok'])),
        'clothing': dict(zip(clothing['year'], clothing['mill_nok'])),
    }


def _load_wool_production(path, hs_mapping):
    """{year: tonnes of Norwegian wool}"""
    df = pd.read_csv(path)
    return dict(zip(df['year'], df['tonnes']))


def _load_prodcom(path, hs_mapping):
    """Long table: prodcom, text, variable, year, value, status (':' confidential, '..' missing)."""
    return pd.read_csv(path, dtype={'prodcom': str})


def _load_varetall(path, hs_mapping):
    """Long table: year, commodity, product, text, unit, quantity, value_1000_nok, source, note."""
    return pd.read_csv(path, dtype={'commodity': str})


def _load_domestic_production(path, hs_mapping):
    """One row per commodity and anchor year: source, code, product, mass_t and how it was derived."""
    return pd.read_csv(path, dtype={'code': str})


def _load_population(path, hs_mapping):
    """{year: mean population}, the mean of 1 January of the year and of the next year."""
    df = pd.read_csv(path).set_index('year')['population_1_january']
    return {year: (df[year] + df[year + 1]) / 2 for year in df.index[:-1]}


# key: (pools that need it, path, loader)
DATA_MAP = {
    'trade_textiles': ({'rw', 'di', 'ma', 'co'}, 'data_files/Tab_08801_textiles.csv', _load_trade_textiles),
    'crossborder': ({'rw'}, 'data_files/SSB_grensehandel_05678_14221.csv', _load_crossborder),
    'wool_production': ({'ma'}, 'data_files/NIBIO_totalkalkylen_ull.csv', _load_wool_production),
    'prodcom': ({'ma'}, 'data_files/SSB_10455_prodcom_garn_tau_nett_2008_2025.csv', _load_prodcom),
    'varetall': ({'ma'}, 'data_files/SSB_industristatistikk_varetall_1988_1989.csv', _load_varetall),
    'domestic_production': ({'ma'}, 'data_files/domestic_production_mass.csv', _load_domestic_production),
    'population': ({'us'}, 'data_files/SSB_05803_befolkning_1985_2026.csv', _load_population),
}


def load_all_data(selected_pools, params):
    preloaded = {}
    for key, (pools, path, loader) in DATA_MAP.items():
        if pools.isdisjoint(selected_pools):
            continue
        print(f"[DATA] {key} <- {path}")
        preloaded[key] = loader(path, params.hs_mapping)
    if 'trade_textiles' in preloaded:
        preloaded['trade_aggregated'] = aggregate_trade(preloaded['trade_textiles'])
        trade = preloaded['trade_textiles']
        preloaded['imports_by_fibre_class'] = aggregate_by_fibre_class(
            trade, params.hs_main_fibre, 1, 'finished', PRODUCTS)
        # The household cohorts in the US pool need the supply composition.
        preloaded['fibre_composition'] = params.fibre_composition
        preloaded['intermediate_by_fibre_class'] = {
            (product, impeks): aggregate_by_fibre_class(trade, params.hs_main_fibre, impeks, 'intermediate',
                                                        [product])
            for product in ('FY', 'FA') for impeks in (1, 2)}
    return preloaded
