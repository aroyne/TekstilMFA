#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Foreign trade flows from SSB table 08801 (HS8 codes, net weight in kg),
split by product group through parameters/hs_mapping.csv. The table is
summed once per direction, category, product and year before the MC loop;
each iteration only applies the 08801 noise factor.
"""
import pandas as pd

from calculations.utils import YEARS

TRADE_DATASET = '08801'


def map_hs_to_product(df_trade, df_mapping):
    """
    Adds 'product', 'category' and 'in_scope' columns to the trade table by
    matching each HS8 code against the longest HS prefix in hs_mapping.csv
    (a 4-digit heading such as 6309 takes precedence over its chapter 63).
    Codes that match no prefix get product NaN.
    """
    df = df_trade.copy()
    mapping = df_mapping.set_index('hs_prefix')
    df['product'] = None
    df['category'] = None
    df['in_scope'] = None
    for prefix_len in (2, 4):
        prefixes = mapping[mapping.index.str.len() == prefix_len]
        hs_prefix = df['HS8'].str[:prefix_len]
        hit = hs_prefix.isin(prefixes.index)
        for col in ('product', 'category', 'in_scope'):
            df.loc[hit, col] = hs_prefix[hit].map(prefixes[col])
    return df


def aggregate_trade(df_trade):
    """Net weight (kg) and value (NOK) of in-scope codes per direction, category, product and year."""
    sel = df_trade[df_trade['in_scope'] == 'yes']
    return sel.groupby(['impeks', 'category', 'product', 'year'])[['amount', 'value_nok']].sum()


def _by_product_and_year(preloaded_data, column, is_import, category, products):
    """Array (year, product) of one column; a year without trade is NaN and fails the flow check."""
    # 'trade_aggregated' <- data_files/Tab_08801_textiles.csv (SSB 08801, HS
    # 50-64), summed by aggregate_trade() when the data is loaded
    agg = preloaded_data['trade_aggregated']
    direction = 1 if is_import else 2
    index = pd.MultiIndex.from_product([[direction], [category], products, YEARS])
    return agg[column].reindex(index).to_numpy().reshape(len(products), len(YEARS)).T


def trade_kt(preloaded_data, dataset_noise, is_import, category, products):
    """Trade in kt, array (year, product), with the 08801 noise factor of the iteration."""
    kg = _by_product_and_year(preloaded_data, 'amount', is_import, category, products)
    return kg / 1e6 * dataset_noise[TRADE_DATASET]


def import_unit_value(preloaded_data, products):
    """
    Customs import value per kg (NOK/kg) per year for the given finished
    products together, array (year,). A ratio of two quantities from the same
    records, so the 08801 noise factor cancels out and is not applied.
    """
    nok = _by_product_and_year(preloaded_data, 'value_nok', True, 'finished', products).sum(axis=1)
    kg = _by_product_and_year(preloaded_data, 'amount', True, 'finished', products).sum(axis=1)
    return nok / kg
