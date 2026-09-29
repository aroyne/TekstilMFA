#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refreshes the given years of SSB table 08801 (HS chapters 50-64) from the
SSB PxWebApi and merges them into data_files/Tab_08801_textiles.csv,
replacing any existing rows for those years (so revisions are picked up).

The API has no column for the supplementary unit ('S' pieces, 'P' pairs,
'1' none) that the original file carries; it is taken from the latest year
of the same HS code already in the file, and set to '1' for codes that are
new.

Usage: python scripts/update_trade_ssb_api.py 2023 2024 2025
"""
import sys
import time

import pandas as pd
import requests

API = 'https://data.ssb.no/api/v0/no/table/08801'
TARGET = 'data_files/Tab_08801_textiles.csv'
CHAPTERS = {str(c) for c in range(50, 65)}
# The API refuses queries above 800 000 cells; 2 directions x 262 countries
# x 3 variables x 3 years is about 4 700 cells per HS code.
CODES_PER_QUERY = 150
COLUMNS = ['year', 'impeks', 'HS_code', 'country', 'unit_code', 'amount', 'supp_quantity', 'value_nok']


def fetch(codes, years):
    query = {
        'query': [
            {'code': 'Varekoder', 'selection': {'filter': 'item', 'values': codes}},
            {'code': 'ImpEks', 'selection': {'filter': 'item', 'values': ['1', '2']}},
            {'code': 'Land', 'selection': {'filter': 'all', 'values': ['*']}},
            {'code': 'ContentsCode', 'selection': {'filter': 'item', 'values': ['Mengde1', 'Verdi', 'Mengde2']}},
            {'code': 'Tid', 'selection': {'filter': 'item', 'values': years}},
        ],
        'response': {'format': 'json-stat2'},
    }
    resp = requests.post(API, json=query, timeout=300)
    resp.raise_for_status()
    js = resp.json()

    dims = js['id']
    sizes = js['size']
    labels = [list(js['dimension'][d]['category']['index'].keys()) for d in dims]
    index = pd.MultiIndex.from_product(labels, names=dims)
    values = pd.Series(js['value'], index=index, dtype='float')
    df = values.unstack('ContentsCode').reset_index()
    assert len(values) == pd.Series(sizes).prod()
    return df


def main(years):
    meta = requests.get(API, timeout=60).json()
    all_codes = next(v['values'] for v in meta['variables'] if v['code'] == 'Varekoder')
    codes = [c for c in all_codes if c.split('_')[0].zfill(8)[:2] in CHAPTERS]
    print(f"{len(codes)} HS codes in chapters 50-64")

    parts = []
    for i in range(0, len(codes), CODES_PER_QUERY):
        chunk = codes[i:i + CODES_PER_QUERY]
        parts.append(fetch(chunk, years))
        print(f"  fetched codes {i + 1}-{i + len(chunk)}")
        time.sleep(1)  # SSB allows 30 queries per minute
    df = pd.concat(parts)

    df = df[(df['Mengde1'].fillna(0) != 0) | (df['Verdi'].fillna(0) != 0)]
    df = df.rename(columns={'Tid': 'year', 'ImpEks': 'impeks', 'Varekoder': 'HS_code', 'Land': 'country',
                            'Mengde1': 'amount', 'Mengde2': 'supp_quantity', 'Verdi': 'value_nok'})

    existing = pd.read_csv(TARGET, sep=';', header=None, names=COLUMNS, dtype=str)
    latest_unit = (existing.sort_values('year').groupby('HS_code')['unit_code'].last())
    df['unit_code'] = df['HS_code'].map(latest_unit).fillna('1')
    for col in ('amount', 'supp_quantity', 'value_nok'):
        df[col] = df[col].fillna(0).round().astype('int64')

    kept = existing[~existing['year'].isin(years)]
    merged = pd.concat([kept, df[COLUMNS].astype(str)])
    merged = merged.sort_values(['year', 'impeks', 'HS_code', 'country'], kind='stable')
    merged.to_csv(TARGET, sep=';', header=False, index=False)
    print(f"Replaced years {years}: {len(existing) - len(kept)} old rows, {len(df)} new rows -> {TARGET}")


if __name__ == '__main__':
    main(sys.argv[1:])
