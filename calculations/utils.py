#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dimensions shared across the calculations/ modules.
"""
import numpy as np

# SSB table 08801 (HS8 trade) starts in 1988, which sets the first year with
# data for the dominant inflows; END_YEAR is the latest year in that table.
START_YEAR = 1988
END_YEAR = 2025
YEARS = list(range(START_YEAR, END_YEAR + 1))

# Clothing, household textiles and footwear: the scope of NORSUS (2023) and
# the EU textile EPR, kept separable for comparison with those figures.
CORE_PRODUCTS = ['CL', 'HT', 'FW']
# Other textile goods ('OT'): carpets, sacks, tarpaulins/tents and other
# made-up articles, split because their users and lifetimes differ widely.
OTHER_PRODUCTS = ['CA', 'SA', 'TA', 'OM']
PRODUCTS = CORE_PRODUCTS + OTHER_PRODUCTS

# Discard statistics (collection, pick analyses) cover CL+HT+FW together, so
# flows after use are split by product group ('g') instead of product ('p').
PRODUCT_GROUPS = ['CORE'] + OTHER_PRODUCTS
GROUP_OF_PRODUCT = {p: ('CORE' if p in CORE_PRODUCTS else p) for p in PRODUCTS}

# Fibre layer (D19): five fibre groups and non-textile material (buttons,
# zips, soles, backing), so that TOT = sum over all materials.
FIBRE_GROUPS = ['SYN', 'CO', 'WO', 'CV', 'OTH']
MATERIALS = FIBRE_GROUPS + ['NT']


def core_group_only(series):
    """
    Array (year, product group) with series in the CORE group and 0 in the
    others, for flows whose statistics cover CL+HT+FW only.
    """
    arr = np.zeros((len(YEARS), len(PRODUCT_GROUPS)))
    arr[:, PRODUCT_GROUPS.index('CORE')] = series
    return arr
