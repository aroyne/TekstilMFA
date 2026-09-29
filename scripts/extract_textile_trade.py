#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extracts HS chapters 50-64 (textiles and footwear) from the full SSB table
08801 export used in NitrogenBudsjett (about 230 MB), so this project only
carries the textile part (same column layout, no header).

Columns in 08801: year; impeks (1 import, 2 export); HS8 code with a
'_<first year>' suffix; country; supplementary unit ('S' pieces, 'P' pairs,
'1' none); net weight in kg; supplementary quantity; value in NOK.

Usage: python scripts/extract_textile_trade.py [path/to/Tab_08801_1988_2024.csv]
"""
import sys
import pandas as pd

SOURCE = '../NitrogenBudsjett/data_files/Tab_08801_1988_2024.csv'
TARGET = 'data_files/Tab_08801_textiles.csv'
CHAPTERS = {str(c) for c in range(50, 65)}

source = sys.argv[1] if len(sys.argv) > 1 else SOURCE
df = pd.read_csv(source, sep=';', header=None, dtype=str)
chapter = df[2].str.strip().str.split('_').str[0].str.zfill(8).str[:2]
df_tex = df[chapter.isin(CHAPTERS)]
df_tex.to_csv(TARGET, sep=';', header=False, index=False)
print(f"Wrote {len(df_tex)} of {len(df)} rows to {TARGET}")
