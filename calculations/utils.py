#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers shared across the calculations/ modules.
"""
import numpy as np

# SSB table 08801 (HS8 trade) starts in 1988, which sets the first year with
# data for the dominant inflows.
START_YEAR = 1988
END_YEAR = 2024
EXPECTED_YEARS = set(range(START_YEAR, END_YEAR + 1))

# Clothing, household textiles and footwear: the scope of NORSUS (2023) and
# the EU textile EPR, kept separable for comparison with those figures.
CORE_PRODUCTS = ['CL', 'HT', 'FW']
# Other textile goods ('OT'): carpets, sacks, tarpaulins/tents and other
# made-up articles, split because their users and lifetimes differ widely.
OTHER_PRODUCTS = ['CA', 'SA', 'TA', 'OM']
PRODUCTS = CORE_PRODUCTS + OTHER_PRODUCTS


def report_missing_years(flow_code, product, missing_years, results):
    """Appends NaN rows for years a flow has no value, so gaps stay visible."""
    for year in sorted(missing_years):
        results.append({
            'flow_name': flow_code,
            'product': product,
            'year': year,
            'value': np.nan,
            'comment': 'not done',
            'data_sources': 'no data',
        })
