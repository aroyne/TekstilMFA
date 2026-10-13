#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds parameters/hs_main_fibre.csv: the main fibre of every HS8 code in
chapters 50-64 and in the bedding headings 9404.30/40/90 of SSB table
08801, read from the English commodity texts in the table metadata. The HS nomenclature classifies a good by the fibre that
predominates by weight, so the text gives the main fibre, not the full
composition.

Rules are applied to the text with exclusion clauses '(excl. ...)' removed,
because those name the fibres a code does NOT cover. The first rule that
matches wins; 'rule' in the output records which one, so the table can be
reviewed line by line. Codes whose text names no fibre get 'UNK'.

The bedding codes (9404) name no fibre in English, but the Norwegian texts
say whether the filling is down or feathers. The filling dominates the
weight, so down and feathers count as other fibre (OTH), and other filling
as synthetic (SYN, an assumption: polyester fibre is the usual filling).

Usage: python scripts/build_hs_main_fibre.py
"""
import re

import pandas as pd
import requests

API = 'https://data.ssb.no/api/v0/en/table/08801'
API_NO = 'https://data.ssb.no/api/v0/no/table/08801'
TARGET = 'parameters/hs_main_fibre.csv'
CHAPTERS = {str(c) for c in range(50, 65)}
EXTRA_HS6 = {'940430', '940440', '940490'}

# (main fibre, regex). Order matters: 'all types of textile materials' means
# any fibre and must be caught before the residual heading; specific
# synthetic polymers come before the generic 'man-made'.
#   OTH: a named fibre outside the main groups (silk, flax, jute ...)
#   RES: residual heading, 'of (other) textile materials' = any fibre not
#        named in the sibling codes, which may include man-made fibres
#   UNK: no fibre stated
RULES = [
    ('UNK', r'all types of textile materials'),
    ('WO', r'\bof wool\b|fine animal hair|kashmir|cashmere|\bwool\b'),
    ('CO', r'\bof cotton\b|\bcotton\b'),
    ('SYN', r'synthetic|polyamide|nylon|polyester|polypropylene|polyethylene|acrylic|elastomeric'),
    ('ART', r'artificial|viscose|cellulose acetate'),
    ('MMF', r'man-made'),
    ('OTH', r'\bsilk\b|\bflax\b|\bjute\b|\bramie\b|\bhemp\b|coconut|abaca|sisal|coarse animal hair'
            r'|vegetable textile (fibres|materials)|paper yarn'),
    ('RES', r'of (other )?textile materials'),
]


def strip_exclusions(text):
    """Removes '(excl. ...)' clauses, also when the API text cuts them off."""
    text = re.sub(r'\(excl[^)]*\)?', ' ', text, flags=re.IGNORECASE)
    return re.sub(r'\(\d{4}-\d{0,4}\)|\(Q1=.*?\)', ' ', text)


def classify(text):
    cleaned = strip_exclusions(text).lower()
    for fibre, pattern in RULES:
        if re.search(pattern, cleaned):
            return fibre, pattern
    return 'UNK', ''


def classify_bedding(text_no):
    """Main fibre of a 9404 code from its Norwegian text."""
    if 'ikke med dun' in text_no:
        return 'SYN', 'bedding, not down or feathers (assumed polyester filling)'
    if 'med dun eller fjær' in text_no:
        return 'OTH', 'bedding with down or feathers'
    return 'UNK', ''


def _commodities(api):
    meta = requests.get(api, timeout=60).json()
    commodity = next(v for v in meta['variables'] if v['code'] == 'Varekoder')
    return pd.Series(commodity['valueTexts'], index=commodity['values'])


def main():
    texts = _commodities(API)
    df = pd.DataFrame({'HS_code': texts.index, 'text': texts.values})
    hs8 = df['HS_code'].str.split('_').str[0].str.zfill(8)
    bedding = hs8.str[:6].isin(EXTRA_HS6)
    df = df[hs8.str[:2].isin(CHAPTERS) | bedding].copy()
    bedding = bedding[df.index]
    df[['main_fibre', 'rule']] = df['text'].apply(lambda t: pd.Series(classify(t)))
    texts_no = _commodities(API_NO)
    df.loc[bedding, ['main_fibre', 'rule']] = [
        classify_bedding(texts_no[code]) for code in df.loc[bedding, 'HS_code']]
    df.to_csv(TARGET, index=False)
    print(f"Wrote {len(df)} codes to {TARGET}")
    print(df['main_fibre'].value_counts().to_string())


if __name__ == '__main__':
    main()
