#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Foreign trade flows from SSB table 08801 (HS8 codes, net weight in kg),
split by product group through parameters/hs_mapping.csv.
"""
from calculations.utils import EXPECTED_YEARS, report_missing_years

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


def add_trade_flow_by_product(results, preloaded_data, dataset_noise, flow_code,
                              is_import, category, products):
    """
    Appends one result row per (product, year) for a trade flow, in kt.
    The whole flow shares the 08801 noise factor of the current iteration.
    """
    # 'trade_textiles' <- data_files/Tab_08801_textiles.csv
    # (SSB 08801, HS chapters 50-64 only; built by scripts/extract_textile_trade.py
    # and scripts/update_trade_ssb_api.py)
    df = preloaded_data['trade_textiles']
    noise_val = dataset_noise[TRADE_DATASET]
    data_sources = 'SSB tab 08801'

    direction = 1 if is_import else 2
    sel = df[(df['impeks'] == direction) & (df['category'] == category)
             & (df['in_scope'] == 'yes') & df['product'].isin(products)]
    kt = sel.groupby(['product', 'year'])['amount'].sum() / 1e6

    for product in products:
        collected_years = set()
        for (prod, year), value in kt.items():
            if prod != product or year not in EXPECTED_YEARS:
                continue
            collected_years.add(year)
            results.append({
                'flow_name': flow_code,
                'product': product,
                'year': int(year),
                'value': float(value * noise_val),
                'comment': 'ok',
                'data_sources': data_sources,
            })
        report_missing_years(flow_code, product, EXPECTED_YEARS - collected_years, results)


def trade_kt_by_year(preloaded_data, dataset_noise, is_import, category, products):
    """
    Total trade in kt per year for the given category and products (in-scope
    HS codes only), with the 08801 noise factor applied.
    """
    # 'trade_textiles' <- data_files/Tab_08801_textiles.csv (SSB 08801, HS 50-64)
    df = preloaded_data['trade_textiles']
    direction = 1 if is_import else 2
    sel = df[(df['impeks'] == direction) & (df['category'] == category)
             & (df['in_scope'] == 'yes') & df['product'].isin(products)]
    kt = sel.groupby('year')['amount'].sum() / 1e6 * dataset_noise[TRADE_DATASET]
    return {int(y): float(v) for y, v in kt.items() if y in EXPECTED_YEARS}


def import_unit_value_by_year(preloaded_data, products):
    """
    Customs import value per kg (NOK/kg) per year for the given finished
    products. A ratio of two quantities from the same records, so the 08801
    noise factor cancels out and is not applied.
    """
    # 'trade_textiles' <- data_files/Tab_08801_textiles.csv (SSB 08801, HS 50-64)
    df = preloaded_data['trade_textiles']
    sel = df[(df['impeks'] == 1) & (df['category'] == 'finished') & df['product'].isin(products)]
    sums = sel.groupby('year')[['value_nok', 'amount']].sum()
    return {int(y): float(r['value_nok'] / r['amount']) for y, r in sums.iterrows() if y in EXPECTED_YEARS}
