#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetches industry-level series for the textile industries and the textile
retail trade from the SSB PxWebApi:

* Main figures for establishments (bedrifter) in manufacturing, by
  industry: 03325 (SN2002, 1999-2008), 08596 (SN2007, 2007-2017) and 12910
  (SN2007, all industries, 2017-2024, unit 31 = establishments). Each table
  is fetched for all its years, so the overlap years 2007-2008 and 2017 can
  be used to check the splices; a series built from them must take each
  year from one table only.
* The retail trade index (Varehandelsindeksen) 09296, value and volume,
  2000-2025, for retail of textiles, clothing and footwear.

Writes data_files/SSB_industri_tekstil_1999_2024.csv (long format: table,
classification, industry code, variable, year, value) and
data_files/SSB_09296_varehandelsindeks_2000_2025.csv.

Usage: python scripts/fetch_ssb_industry_series.py
"""
import pandas as pd
import requests

API = 'https://data.ssb.no/api/v0/no/table/'

# SN2002: 17 textiles (17.7 is knitted apparel, which SN2007 moved to 14),
# 18 apparel, 19.3 footwear. SN2007: 13 textiles, 14 apparel, 15.2 footwear.
SN2002_CODES = ['17', '17.1', '17.2', '17.3', '17.4', '17.5', '17.51', '17.52', '17.53', '17.54',
                '17.6', '17.7', '18', '18.1', '18.2', '18.3', '19.3']
SN2007_CODES = ['13.1', '13.2', '13.3', '13.9', '13.91', '13.92', '13.93', '13.94', '13.95', '13.96',
                '13.99', '14.1', '14.11', '14.12', '14.13', '14.14', '14.19', '14.2', '14.3', '15.2']

INDUSTRY_TABLES = {
    '03325': ('SN2002', 'NACE', SN2002_CODES,
              ['Bedrifter', 'Sysselsatte', 'Omsetning', 'Produksjonsverdi'], {}),
    '08596': ('SN2007', 'NACE2007', SN2007_CODES,
              ['Bedrifter', 'Sysselsatte', 'Omsetning', 'Produksjonsverdi'], {}),
    '12910': ('SN2007', 'NACE2007', SN2007_CODES,
              ['Enheter', 'Sysselsatte', 'Oms', 'Produksjonsverdi'], {'Enhet': ['31']}),
}
# 12910 names the same variables differently.
VARIABLE_NAMES = {'Enheter': 'Bedrifter', 'Oms': 'Omsetning'}

RETAIL_CODES = ['47', '47.51', '47.71', '47.72']


def fetch(table, selection):
    query = {
        'query': [{'code': code, 'selection': {'filter': 'item', 'values': values}}
                  for code, values in selection.items()],
        'response': {'format': 'json-stat2'},
    }
    resp = requests.post(API + table, json=query, timeout=300)
    resp.raise_for_status()
    js = resp.json()
    labels = [list(js['dimension'][d]['category']['index'].keys()) for d in js['id']]
    index = pd.MultiIndex.from_product(labels, names=js['id'])
    return pd.Series(js['value'], index=index, dtype='float', name='value').reset_index()


def all_years(table):
    meta = requests.get(API + table, timeout=60).json()
    return next(v['values'] for v in meta['variables'] if v['code'] == 'Tid')


def main():
    parts = []
    for table, (classification, nace_dim, codes, variables, extra) in INDUSTRY_TABLES.items():
        df = fetch(table, {nace_dim: codes, 'ContentsCode': variables, 'Tid': all_years(table), **extra})
        df = df.rename(columns={nace_dim: 'industry', 'ContentsCode': 'variable', 'Tid': 'year'})
        df['variable'] = df['variable'].replace(VARIABLE_NAMES)
        df['table'] = table
        df['classification'] = classification
        parts.append(df[['table', 'classification', 'industry', 'variable', 'year', 'value']])
        print(f'{table}: {len(df)} rows')
    pd.concat(parts).to_csv('data_files/SSB_industri_tekstil_1999_2024.csv', index=False)

    retail = fetch('09296', {'NACE2007': RETAIL_CODES, 'ContentsCode': ['Verdiindeks', 'VolumUjustert'],
                             'Tid': all_years('09296')})
    retail = retail.rename(columns={'NACE2007': 'industry', 'ContentsCode': 'variable', 'Tid': 'year'})
    retail.to_csv('data_files/SSB_09296_varehandelsindeks_2000_2025.csv', index=False)
    print(f'09296: {len(retail)} rows')


if __name__ == '__main__':
    main()
