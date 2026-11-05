#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetches SSB's population projection (table 14740, the 2026 projection,
published 12 June 2026) from the SSB PxWebApi: the whole population on
1 January, summed over sex and age, for the main alternative (MMM) and
low (LLL) and high (HHH) national growth, 2026-2051. 2051 is included
because the model uses the mean of 1 January of a year and of the next.

Writes data_files/SSB_14740_befolkningsframskriving_2026_2051.csv
(year, alternative, population_1_january).

Usage: python scripts/fetch_population_projection.py
"""
import pandas as pd
import requests

API = 'https://data.ssb.no/api/v0/no/table/14740'
TARGET = 'data_files/SSB_14740_befolkningsframskriving_2026_2051.csv'
ALTERNATIVES = ['MMM', 'LLL', 'HHH']
YEARS = [str(y) for y in range(2026, 2052)]


def main():
    query = {
        'query': [
            {'code': 'Kjonn', 'selection': {'filter': 'all', 'values': ['*']}},
            {'code': 'Alder', 'selection': {'filter': 'all', 'values': ['*']}},
            {'code': 'InnvandrLandbakgr', 'selection': {'filter': 'item', 'values': ['00']}},
            {'code': 'Framskriv', 'selection': {'filter': 'item', 'values': ALTERNATIVES}},
            {'code': 'ContentsCode', 'selection': {'filter': 'item', 'values': ['Folkemengde']}},
            {'code': 'Tid', 'selection': {'filter': 'item', 'values': YEARS}},
        ],
        'response': {'format': 'json-stat2'},
    }
    resp = requests.post(API, json=query, timeout=300)
    resp.raise_for_status()
    js = resp.json()
    labels = [list(js['dimension'][d]['category']['index'].keys()) for d in js['id']]
    index = pd.MultiIndex.from_product(labels, names=js['id'])
    values = pd.Series(js['value'], index=index, dtype='float')
    total = values.groupby(['Tid', 'Framskriv']).sum().reset_index()
    total.columns = ['year', 'alternative', 'population_1_january']
    total['year'] = total['year'].astype(int)
    total['population_1_january'] = total['population_1_january'].astype(int)
    total.sort_values(['alternative', 'year']).to_csv(TARGET, index=False)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
