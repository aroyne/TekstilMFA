#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Derives the anchor points 'wool_scoured_domestic' (greasy wool scoured in
Norway, kt) in data_files/anchor_values.csv from official data:

    Norwegian wool (Totalkalkylen, NIBIO) + import of greasy wool
    - export of greasy wool (SSB 08801, HS 5101.11 and 5101.19)

Exports declared as carbonised wool (5101.30) in 1996-2000 and 2002 are
counted as greasy: they went to Great Britain like the greasy wool, their
customs value per kg is that of greasy wool and below that of degreased
wool (carbonised wool is cleaner and should cost more), and the greasy
exports drop by about the same amount in those years. The rule is applied
per year: 5101.30 is greasy when its export value per kg is below that of
degreased wool (5101.21).

The annual balance is noisy: shearing and export fall in different years and
wool is stored in between, so it is negative in 2017 and close to zero in
most years after 2007. The model therefore uses the mean over periods with a
stable export share instead of the annual values. The periods follow the
export share (printed below); the step from one period to the next is placed
between two adjacent years. The uncertainty of each anchor is the standard
error of the period mean, in percent.

Usage: python scripts/derive_wool_scouring_anchors.py
"""
import pandas as pd

WOOL = 'data_files/NIBIO_totalkalkylen_ull.csv'
TRADE = 'data_files/Tab_08801_textiles.csv'
GREASY_HS6 = ['510111', '510119']
DEGREASED_HS6 = '510121'
CARBONISED_HS6 = '510130'
PERIODS = [(1988, 1995), (1996, 2000), (2001, 2006), (2007, 2025)]


def greasy_balance():
    wool = pd.read_csv(WOOL).set_index('year')['tonnes'] / 1000
    trade = pd.read_csv(TRADE, sep=';', header=None, dtype=str)
    trade.columns = ['year', 'impeks', 'HS_code', 'country', 'unit_code', 'amount', 'supp_quantity', 'value_nok']
    trade['year'] = trade['year'].astype(int)
    trade['impeks'] = trade['impeks'].astype(int)
    trade['amount'] = pd.to_numeric(trade['amount'])
    trade['value_nok'] = pd.to_numeric(trade['value_nok'])
    trade['hs6'] = trade['HS_code'].str.strip().str.split('_').str[0].str.zfill(8).str[:6]
    exports = trade[trade['impeks'] == 2].groupby(['hs6', 'year'])[['amount', 'value_nok']].sum()
    unit_value = exports['value_nok'] / exports['amount']
    carbonised = unit_value.loc[CARBONISED_HS6]
    greasy_years = carbonised[carbonised < unit_value.loc[DEGREASED_HS6].reindex(carbonised.index)].index
    misdeclared = (trade['hs6'] == CARBONISED_HS6) & (trade['impeks'] == 2) & trade['year'].isin(greasy_years)
    greasy = trade[trade['hs6'].isin(GREASY_HS6) | misdeclared]
    kt = greasy.groupby(['year', 'impeks'])['amount'].sum().unstack(fill_value=0.0) / 1e6
    df = pd.DataFrame({'production': wool.reindex(kt.index), 'import': kt[1], 'export': kt[2]})
    df['scoured_domestic'] = df['production'] + df['import'] - df['export']
    df['export_share'] = df['export'] / df['production']
    return df


def main():
    df = greasy_balance()
    print(df.round(3).to_string())
    print()
    for first, last in PERIODS:
        period = df.loc[first:last, 'scoured_domestic']
        mean = period.mean()
        standard_error = period.std() / len(period) ** 0.5
        print(f"{first}-{last}: mean scoured in Norway {mean:.3f} kt, "
              f"standard error {standard_error:.3f} kt ({100 * standard_error / mean:.0f} %)")


if __name__ == '__main__':
    main()
