#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds parameters/hs_main_fibre.csv: the main fibre of every HS8 code in
chapters 50-64 of SSB table 08801, read from the English commodity texts in
the table metadata. The HS nomenclature classifies a good by the fibre that
predominates by weight, so the text gives the main fibre, not the full
composition.

Rules are applied to the text with exclusion clauses '(excl. ...)' removed,
because those name the fibres a code does NOT cover. The first rule that
matches wins; 'rule' in the output records which one, so the table can be
reviewed line by line. Codes whose text names no fibre get 'UNK'.

Usage: python scripts/build_hs_main_fibre.py
"""
import re

import pandas as pd
import requests

API = 'https://data.ssb.no/api/v0/en/table/08801'
TARGET = 'parameters/hs_main_fibre.csv'
CHAPTERS = {str(c) for c in range(50, 65)}

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


def main():
    meta = requests.get(API, timeout=60).json()
    commodity = next(v for v in meta['variables'] if v['code'] == 'Varekoder')
    df = pd.DataFrame({'HS_code': commodity['values'], 'text': commodity['valueTexts']})
    df = df[df['HS_code'].str[:2].isin(CHAPTERS)].copy()
    df[['main_fibre', 'rule']] = df['text'].apply(lambda t: pd.Series(classify(t)))
    df.to_csv(TARGET, index=False)
    print(f"Wrote {len(df)} codes to {TARGET}")
    print(df['main_fibre'].value_counts().to_string())


if __name__ == '__main__':
    main()
