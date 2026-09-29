#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loads every source data file once, before the MC loop, and returns them in
one dict keyed by a short data key. DATA_MAP lists which pools need each
file, so a run of a single pool only loads what it uses. Every file is
described in DATA_SOURCES.md.
"""
import pandas as pd

from calculations.trade import map_hs_to_product


def _load_trade_textiles(path, hs_mapping):
    df = pd.read_csv(path, sep=';', header=None, dtype=str)
    df.columns = ['year', 'impeks', 'HS_code', 'country', 'unit_code', 'amount', 'supp_quantity', 'value_nok']
    df['HS8'] = df['HS_code'].str.strip().str.split('_').str[0].str.zfill(8)
    df['year'] = df['year'].astype(int)
    df['impeks'] = df['impeks'].astype(int)
    for col in ('amount', 'supp_quantity', 'value_nok'):
        df[col] = pd.to_numeric(df[col])
    return map_hs_to_product(df, hs_mapping)


# key: (pools that need it, path, loader)
DATA_MAP = {
    'trade_textiles': ({'rw', 'di', 'ma', 'co'}, 'data_files/Tab_08801_textiles_1988_2024.csv', _load_trade_textiles),
}


def load_all_data(selected_pools, params):
    preloaded = {}
    for key, (pools, path, loader) in DATA_MAP.items():
        if pools.isdisjoint(selected_pools):
            continue
        print(f"[DATA] {key} <- {path}")
        preloaded[key] = loader(path, params.hs_mapping)
    return preloaded
