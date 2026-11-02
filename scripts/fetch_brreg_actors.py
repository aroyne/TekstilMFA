#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetches the legal units (enheter) registered under the industry codes that
map to the model's processes, from the Central Coordinating Register for
Legal Entities (Enhetsregisteret), and their annual accounts from the
Register of Company Accounts (Regnskapsregisteret). Both are open APIs at
data.brreg.no.

The industry codes are SN2025 (the register switched in 2025; SN2007 codes
such as 14.130 no longer match anything). A unit is included if any of its
up to three industry codes is in NACE_NODES; 'matched_code' is the first
one that is. The accounts API only serves the last three years, so the
files are a snapshot named by the fetch date and must be kept to build a
series.

Turnover is for the whole legal unit and says nothing about tonnes or about
the share of the activity that concerns textiles; 'coverage' marks codes
where textiles are only part of the trade. Units without a duty to file
accounts (most sole proprietorships, many associations) are listed without
accounts.

Usage: python scripts/fetch_brreg_actors.py
Writes data_files/BRREG_enheter_<date>.csv and
data_files/BRREG_regnskap_<date>.csv.
"""
import datetime
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

ENHETER_API = 'https://data.brreg.no/enhetsregisteret/api/enheter'
REGNSKAP_API = 'https://data.brreg.no/regnskapsregisteret/regnskap/'
# The search API refuses page * size above 10 000.
MAX_HITS = 10_000
PAGE_SIZE = 1_000
WORKERS = 8

# (node, coverage, note). 'outside' marks codes for products outside the
# model boundary (D22), kept because they may absorb fabric and yarn that
# the MA.TX balance otherwise sends to finished goods.
NACE_NODES = {
    '13.100': ('MA.FI', 'full', 'Preparation and spinning of textile fibres'),
    '13.200': ('MA.TX', 'full', 'Weaving'),
    '13.300': ('MA.TX', 'full', 'Finishing'),
    '13.910': ('MA.TX', 'full', 'Knitted and crocheted fabrics'),
    '13.920': ('MA.TX', 'full', 'Made-up household textiles'),
    '13.930': ('MA.TX', 'full', 'Carpets and rugs'),
    '13.990': ('MA.TX', 'full', 'Other textiles n.e.c.'),
    '13.940': ('outside', 'full', 'Cordage, rope, twine and netting (D22)'),
    '13.950': ('outside', 'full', 'Non-wovens (D22)'),
    '13.960': ('outside', 'full', 'Technical and industrial textiles (D22)'),
    '14.100': ('MA.TX', 'full', 'Knitted and crocheted apparel'),
    '14.210': ('MA.TX', 'full', 'Outerwear'),
    '14.220': ('MA.TX', 'full', 'Underwear'),
    '14.230': ('MA.TX', 'full', 'Workwear'),
    '14.240': ('MA.TX', 'full', 'Leather and fur apparel'),
    '14.290': ('MA.TX', 'full', 'Other apparel and accessories'),
    '15.200': ('outside', 'full', 'Footwear; not an output of MA.TX in the model (D26)'),
    '46.160': ('DI.RT', 'full', 'Agents in textiles, clothing, fur, footwear and leather'),
    '46.410': ('DI.RT', 'full', 'Wholesale of textiles'),
    '46.420': ('DI.RT', 'full', 'Wholesale of clothing and footwear'),
    '47.510': ('DI.RT', 'full', 'Retail of textiles'),
    '47.710': ('DI.RT', 'full', 'Retail of clothing'),
    '47.720': ('DI.RT', 'full', 'Retail of footwear and leather goods'),
    '47.631': ('DI.RT', 'partial', 'Retail of sports goods'),
    '47.120': ('DI.RT', 'partial', 'Non-specialised retail (department stores)'),
    '47.790': ('CO.RE', 'partial', 'Retail of second-hand goods'),
    '96.100': ('US.IC', 'partial', 'Washing and dry-cleaning (industrial laundries)'),
    '38.110': ('CO.CO', 'partial', 'Collection of non-hazardous waste; also WM.RS'),
    '38.210': ('WM.RC', 'partial', 'Material recovery'),
    '38.220': ('WM.IN', 'partial', 'Energy recovery'),
    '38.310': ('WM.IN', 'partial', 'Incineration without energy recovery'),
    '38.320': ('WM.LF', 'partial', 'Landfill'),
}


def fetch_units(code):
    first = requests.get(ENHETER_API, params={'naeringskode': code, 'size': 1}, timeout=60)
    first.raise_for_status()
    total = first.json()['page']['totalElements']
    assert total <= MAX_HITS, f'{code}: {total} units exceed the API limit; split the query'
    units = []
    for page in range(-(-total // PAGE_SIZE)):
        resp = requests.get(ENHETER_API, params={'naeringskode': code, 'size': PAGE_SIZE, 'page': page},
                            timeout=120)
        resp.raise_for_status()
        units.extend(resp.json()['_embedded']['enheter'])
    assert len(units) == total, f'{code}: got {len(units)} of {total} units'
    return units


def unit_row(unit):
    codes = [unit[k]['kode'] for k in ('naeringskode1', 'naeringskode2', 'naeringskode3') if k in unit]
    matched = next(c for c in codes if c in NACE_NODES)
    node, coverage, _ = NACE_NODES[matched]
    address = unit.get('forretningsadresse', unit.get('postadresse', {}))
    return {
        'orgnr': unit['organisasjonsnummer'],
        'name': unit['navn'],
        'org_form': unit['organisasjonsform']['kode'],
        'nace1': codes[0],
        'nace2': codes[1] if len(codes) > 1 else '',
        'nace3': codes[2] if len(codes) > 2 else '',
        'matched_code': matched,
        'node': node,
        'coverage': coverage,
        # The register withholds the count for units with 1-4 employees; they
        # have registered employees but no 'antallAnsatte'.
        'employees': unit.get('antallAnsatte') if unit['harRegistrertAntallAnsatte'] else 0,
        'employees_1_to_4': unit['harRegistrertAntallAnsatte'] and 'antallAnsatte' not in unit,
        'municipality_no': address.get('kommunenummer', ''),
        'in_group': unit.get('erIKonsern', False),
        'parent_orgnr': unit.get('overordnetEnhet', ''),
        'bankrupt': unit['konkurs'],
        'winding_up': unit['underAvvikling'],
        'last_accounts_year': unit.get('sisteInnsendteAarsregnskap', ''),
    }


def fetch_accounts(orgnr):
    resp = requests.get(REGNSKAP_API + orgnr, timeout=60)
    # 404 means the unit has filed no accounts in the years the API serves.
    if resp.status_code == 404:
        return []
    # The API cannot serve accounts in the non-profit layout (e.g. UFF and
    # other collectors); they are listed with a note so they can be read
    # from the annual reports instead.
    if resp.status_code == 500 and 'oppstillingsplan som ikke er stottet' in resp.text:
        return [{'orgnr': orgnr, 'note': resp.json()['message']}]
    resp.raise_for_status()
    rows = []
    for acc in resp.json():
        # Units without operating income (holding companies, dormant units)
        # file accounts without these items; they are kept as missing, not 0.
        income = acc['resultatregnskapResultat'].get('driftsresultat', {}).get('driftsinntekter', {})
        rows.append({
            'orgnr': orgnr,
            'year': int(acc['regnskapsperiode']['tilDato'][:4]),
            'period_from': acc['regnskapsperiode']['fraDato'],
            'period_to': acc['regnskapsperiode']['tilDato'],
            'accounts_type': acc['regnskapstype'],
            'currency': acc['valuta'],
            'sales_revenue': income.get('salgsinntekter'),
            'operating_revenue': income.get('sumDriftsinntekter'),
        })
    return rows


def main():
    today = datetime.date.today().isoformat()
    rows = {}
    for code in NACE_NODES:
        units = fetch_units(code)
        print(f'{code}: {len(units)} units')
        for unit in units:
            # A unit with two matching codes is found twice; unit_row picks the same first match.
            rows[unit['organisasjonsnummer']] = unit_row(unit)
    units = pd.DataFrame(rows.values()).sort_values(['node', 'matched_code', 'orgnr'])
    units.to_csv(f'data_files/BRREG_enheter_{today}.csv', index=False)

    filers = units.loc[units['last_accounts_year'] != '', 'orgnr'].tolist()
    print(f'Fetching accounts for {len(filers)} of {len(units)} units')
    with ThreadPoolExecutor(WORKERS) as pool:
        accounts = [row for rows_ in pool.map(fetch_accounts, filers) for row in rows_]
    accounts = pd.DataFrame(accounts).sort_values(['orgnr', 'year', 'accounts_type'])
    print(f'{len(accounts)} accounts, {accounts["operating_revenue"].isna().sum()} without operating revenue')
    accounts.to_csv(f'data_files/BRREG_regnskap_{today}.csv', index=False)


if __name__ == '__main__':
    main()
