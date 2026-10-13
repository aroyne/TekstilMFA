#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Derives the mass of finished textile goods produced in Norway per product
in anchor years (D26), written to data_files/domestic_production_mass.csv.
The model uses the shares per product to split domestic finished products
(MA.TX -> DI.RT); the mass totals are only a check, because both sources
cover large units only.

Sources: SSB Industristatistikk, Hefte II Varetall, 1988 and 1989
(data_files/SSB_industristatistikk_varetall_1988_1989.csv) and Prodcom,
SSB 10455, 2008, 2009 and 2011, the years with most published quantities
(data_files/SSB_10455_prodcom_ferdigvarer_2008_2025.csv, with the codes in
scope and their HS codes in parameters/domestic_production_codes.csv).

Mass per commodity and year, in order of preference:
  tonnes/kg       as published;
  pieces/pairs    times the import mass per piece of the same HS codes in
                  the same year (SSB 08801, rows with pieces or pairs);
  value only      divided by a Norwegian price per kg: that of the same
                  commodity in another anchor year of the same source, or
                  else the import value per kg of the same HS codes in the
                  same year times the median ratio of Norwegian to import
                  price per kg over all commodities where both are known.

Usage: python scripts/derive_domestic_product_mass.py
"""
import numpy as np
import pandas as pd

VARETALL = 'data_files/SSB_industristatistikk_varetall_1988_1989.csv'
PRODCOM = 'data_files/SSB_10455_prodcom_ferdigvarer_2008_2025.csv'
CODES = 'parameters/domestic_production_codes.csv'
TRADE = 'data_files/Tab_08801_textiles.csv'
TARGET = 'data_files/domestic_production_mass.csv'
PRODCOM_YEARS = [2008, 2009, 2011]
PRODUCTS = ['CL', 'HT', 'FW', 'CA', 'SA', 'TA', 'OM']


def load_imports():
    trade = pd.read_csv(TRADE, sep=';', header=None, dtype=str)
    trade.columns = ['year', 'impeks', 'HS_code', 'country', 'unit_code', 'amount', 'supp_quantity', 'value_nok']
    trade = trade[trade['impeks'] == '1'].copy()
    trade['year'] = trade['year'].astype(int)
    trade['hs8'] = trade['HS_code'].str.strip().str.split('_').str[0].str.zfill(8)
    for col in ('amount', 'supp_quantity', 'value_nok'):
        trade[col] = pd.to_numeric(trade[col])
    return trade


def varetall_prefixes(commodity):
    """HS8 prefixes covered by a printed commodity or range, e.g. '6101.0000-6105.1000'."""
    first, _, last = commodity.partition('-')
    last = last or first
    return first.replace('.', '').rstrip('0'), last.replace('.', '').rstrip('0')


def import_rows(imports, year, hs):
    sel = imports[imports['year'] == year]
    if isinstance(hs, tuple):
        low, high = hs
        return sel[(sel['hs8'].str[:len(low)] >= low) & (sel['hs8'].str[:len(high)] <= high)]
    return sel[sel['hs8'].apply(lambda h: any(h.startswith(p) for p in hs))]


def import_kg_per_piece(rows):
    counted = rows[rows['unit_code'].isin(['S', 'P']) & (rows['supp_quantity'] > 0)]
    return counted['amount'].sum() / counted['supp_quantity'].sum() if len(counted) else np.nan


def import_nok_per_kg(rows):
    return rows['value_nok'].sum() / rows['amount'].sum() if rows['amount'].sum() > 0 else np.nan


def commodities():
    """One row per commodity and year: source, code, product, hs, unit, quantity, value (1000 NOK)."""
    varetall = pd.read_csv(VARETALL, dtype={'commodity': str})
    varetall = varetall[varetall['product'].isin(PRODUCTS)]
    rows = [dict(source='varetall', year=r.year, code=r.commodity, product=r.product,
                 hs=varetall_prefixes(r.commodity), unit=r.unit if isinstance(r.unit, str) else '',
                 quantity=r.quantity, value=r.value_1000_nok) for r in varetall.itertuples()]

    codes = pd.read_csv(CODES, dtype=str)
    prodcom = pd.read_csv(PRODCOM, dtype={'prodcom': str})
    prodcom = prodcom[prodcom['year'].isin(PRODCOM_YEARS) & prodcom['prodcom'].isin(codes['code'])]
    for code in codes.itertuples():
        sel = prodcom[prodcom['prodcom'] == code.code]
        unit = sel['text'].iloc[0].split('(M=')[1].split(')')[0] if '(M=' in sel['text'].iloc[0] else ''
        for year in PRODCOM_YEARS:
            values = sel[sel['year'] == year].set_index('variable')['value']
            quantity, value = values.get('Mengde'), values.get('Verdi')
            if pd.isna(quantity) and pd.isna(value):
                continue
            # m² and pieces of bedding cannot be converted to mass from 08801
            if unit == 'm²' or code.hs_prefixes.startswith('9404'):
                quantity = np.nan
            rows.append(dict(source='prodcom', year=year, code=code.code, product=code.product,
                             hs=code.hs_prefixes.split(';'), unit={'kg': 'kg', 'stk': 'pieces', 'par': 'pairs'}.get(
                                 unit, unit), quantity=quantity, value=value))
    return pd.DataFrame(rows)


def main():
    imports = load_imports()
    df = commodities()
    df['mass_t'] = np.nan
    df['method'] = ''
    df['import_nok_per_kg'] = [import_nok_per_kg(import_rows(imports, r.year, r.hs)) for r in df.itertuples()]

    for i, r in df.iterrows():
        if pd.isna(r['quantity']):
            continue
        if r['unit'] in ('tonnes',):
            df.at[i, 'mass_t'], df.at[i, 'method'] = r['quantity'], 'tonnes as published'
        elif r['unit'] == 'kg':
            df.at[i, 'mass_t'], df.at[i, 'method'] = r['quantity'] / 1000, 'kg as published'
        elif r['unit'] in ('1000 pieces', '1000 pairs', 'pieces', 'pairs'):
            pieces = r['quantity'] * (1000 if r['unit'].startswith('1000') else 1)
            kg_each = import_kg_per_piece(import_rows(imports, r['year'], r['hs']))
            if not np.isnan(kg_each):
                df.at[i, 'mass_t'] = pieces * kg_each / 1000
                df.at[i, 'method'] = f'{r["unit"]} x import kg per piece ({kg_each:.3f})'

    known = df['mass_t'].notna() & df['value'].notna()
    df['nok_per_kg'] = np.where(known, df['value'] * 1000 / (df['mass_t'] * 1000), np.nan)
    ratio = (df.loc[known, 'nok_per_kg'] / df.loc[known, 'import_nok_per_kg']).median()
    print(f"Median ratio of Norwegian to import price per kg: {ratio:.2f} "
          f"({known.sum()} commodities with both)")

    for i, r in df[df['mass_t'].isna() & df['value'].notna()].iterrows():
        same = df[(df['source'] == r['source']) & (df['code'] == r['code']) & df['nok_per_kg'].notna()]
        if len(same):
            price, how = same['nok_per_kg'].mean(), 'value / own Norwegian price per kg in another year'
        else:
            price, how = r['import_nok_per_kg'] * ratio, 'value / (import price per kg x median ratio)'
        df.at[i, 'mass_t'] = r['value'] * 1000 / price / 1000
        df.at[i, 'method'] = f'{how} ({price:.0f} NOK/kg)'

    df['hs'] = df['hs'].apply(lambda h: '-'.join(h) if isinstance(h, tuple) else ';'.join(h))
    out = df[['year', 'source', 'code', 'product', 'hs', 'unit', 'quantity', 'value', 'mass_t', 'method']]
    out.round({'mass_t': 1}).to_csv(TARGET, index=False)
    summary = out.pivot_table(index='year', columns='product', values='mass_t', aggfunc='sum').fillna(0)
    print((summary / 1000).round(2).to_string())
    print((summary.div(summary.sum(axis=1), axis=0)).round(3).to_string())
    print(f"Wrote {len(out)} rows to {TARGET}")


if __name__ == '__main__':
    main()
