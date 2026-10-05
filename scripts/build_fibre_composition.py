#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds parameters/fibre_composition.csv: the fibre-group composition (SYN,
CO, WO, CV, OTH) used for import mass whose HS code states no fibre (main
fibre RES or UNK in parameters/hs_main_fibre.csv), per product. Also prints
the non-textile shares of clothing and footwear that the bills of materials
imply, as a check on nontextile_share_CL and nontextile_share_FW.

  CL, FW : unweighted mean of the bills of materials of the representative
           products in PEFCR Apparel & Footwear (Cascale 2025, tables A.IV 2
           and A.IV 3), textile materials only. No market weights are given
           for the representative products, hence the plain mean.
  others : composition of the import mass of the same product whose HS code
           does state the fibre, 2015-2025 (assumption: codes without fibre
           are like the rest of the product group).
  OM     : no OM code states a fibre, so the pooled composition of all
           finished products except footwear with fibre stated is used.

Usage: python scripts/build_fibre_composition.py
"""
import pandas as pd

TRADE = 'data_files/Tab_08801_textiles.csv'
HS_MAIN_FIBRE = 'parameters/hs_main_fibre.csv'
HS_MAPPING = 'parameters/hs_mapping.csv'
TARGET = 'parameters/fibre_composition.csv'
GROUPS = ['SYN', 'CO', 'WO', 'CV', 'OTH']
YEARS = range(2015, 2026)

# PEFCR 2025, table A.IV 2, RP1-RP10 (share of product weight, %), mapped to
# fibre groups; NT = materials that are not textile fibres.
APPAREL = {
    'SYN': [[23.3, 26.2, 32.7, 67.4, 44.9, 30.5, 67.8, 24.1, 99.6, 50.3]],  # acrylic, elastane, PA, PES (incl. recycled), PTFE
    'CO': [[70, 55, 34, 15, 47, 54, 22, 70.5, 0, 15]],
    'WO': [[0, 0, 28, 9.9, 0, 2, 2, 0, 0, 26]],  # wool, cashmere
    'CV': [[6, 13, 5, 4, 2, 13, 8, 5, 0, 0]],
    'OTH': [[0, 5, 0, 0, 4, 0, 0, 0, 0, 1]],  # linen, silk
    'NT': [[0.7, 0.8, 0.3, 3.6, 2.1, 0.5, 0.2, 0.4, 0.4, 7.7]],  # trims, leather, fur, down
}
# PEFCR 2025, table A.IV 3, RP11-RP13.
FOOTWEAR = {
    'SYN': [[3, 32, 18]],  # PA, PES (incl. recycled)
    'CO': [[0, 3, 0]],
    'WO': [[0, 4, 0]],
    'CV': [[0, 2, 2]],  # viscose/modal, wood-based nonwoven
    'OTH': [[0, 0, 0]],
    'NT': [[97, 59, 80]],  # cork, EVA, leather, metal, PU, PVC, rubber, TPU, trims
}
# Gottfridsson & Zhang (2015), Chalmers, fig. 8: textile share of shoes per
# HS heading (textile + 'synthetics').
FOOTWEAR_TEXTILE_BY_HEADING = {'6401': 0.056, '6402': 0.056, '6403': 0.069, '6404': 0.376, '6405': 0.216}
# Main fibre classes to fibre groups; MMF and RES/UNK are handled separately.
CLASS_TO_GROUP = {'CO': 'CO', 'WO': 'WO', 'SYN': 'SYN', 'ART': 'CV', 'OTH': 'OTH'}


def mean_composition(bom):
    means = {k: sum(v[0]) / len(v[0]) for k, v in bom.items()}
    textile = sum(means[g] for g in GROUPS)
    return {g: means[g] / textile for g in GROUPS}, means['NT'] / (textile + means['NT'])


def imports_by_class():
    trade = pd.read_csv(TRADE, sep=';', header=None, dtype=str,
                        names=['year', 'impeks', 'HS_code', 'country', 'unit', 'amount', 'supp_quantity', 'value_nok'])
    trade['amount'] = trade['amount'].astype(float)
    trade = trade[(trade['impeks'] == '1') & trade['year'].astype(int).isin(YEARS)]
    trade['HS_code'] = trade['HS_code'].str.strip()
    mapping = pd.read_csv(HS_MAPPING, dtype={'hs_prefix': str})
    fibre = pd.read_csv(HS_MAIN_FIBRE, dtype=str)
    trade = trade.merge(fibre[['HS_code', 'main_fibre']], on='HS_code', how='left', validate='many_to_one')
    product = pd.Series(index=trade.index, dtype=object)
    for n in (2, 4):  # longest prefix wins, as in calculations/trade.py
        prefixes = mapping[mapping['hs_prefix'].str.len() == n].set_index('hs_prefix')
        hit = trade['HS_code'].str[:n].isin(prefixes.index)
        product[hit] = trade.loc[hit, 'HS_code'].str[:n].map(prefixes['product'])
    trade['product'] = product
    return trade


def main():
    trade = imports_by_class()
    rows = []
    for product in ['CL', 'HT', 'FW', 'CA', 'SA', 'TA', 'OM']:
        if product in ('CL', 'FW'):
            comp, nt = mean_composition(APPAREL if product == 'CL' else FOOTWEAR)
            source = 'PEFCR Apparel & Footwear (Cascale 2025), tab. A.IV 2-3, mean of representative products'
            status = 'literature'
            print(f"{product}: non-textile share in PEFCR bills of materials = {nt:.3f}")
        else:
            same = [product] if product != 'OM' else ['CL', 'HT', 'CA', 'SA', 'TA']
            sel = trade[trade['product'].isin(same) & trade['main_fibre'].isin(CLASS_TO_GROUP)]
            kg = sel.groupby(sel['main_fibre'].map(CLASS_TO_GROUP))['amount'].sum().reindex(GROUPS, fill_value=0.0)
            comp = (kg / kg.sum()).to_dict()
            source = ('SSB 08801 2015-2025: imports of ' + ('the same product' if product != 'OM' else
                      'all finished products except footwear') + ' with fibre stated in the HS code')
            status = 'assumption'
        rows.append({'product': product, 'year': '', **{g: round(comp[g], 4) for g in GROUPS},
                     'source': source, 'status': status})
    pd.DataFrame(rows).to_csv(TARGET, index=False)
    print(pd.DataFrame(rows)[['product'] + GROUPS].to_string(index=False))

    fw = trade[(trade['product'] == 'FW') & trade['HS_code'].str[:4].isin(FOOTWEAR_TEXTILE_BY_HEADING)]
    kg = fw.groupby(fw['HS_code'].str[:4])['amount'].sum()
    textile = sum(kg[h] * s for h, s in FOOTWEAR_TEXTILE_BY_HEADING.items()) / kg.sum()
    print(f"FW: import-weighted non-textile share from Gottfridsson & Zhang = {1 - textile:.3f} "
          f"(heading shares {(kg / kg.sum()).round(3).to_dict()})")


if __name__ == '__main__':
    main()
