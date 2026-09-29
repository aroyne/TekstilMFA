#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers shared across the calculations/ modules.
"""
import numpy as np

# SSB table 08801 (HS8 trade) starts in 1988, which sets the first year with
# data for the dominant inflows; END_YEAR is the latest year in that table.
START_YEAR = 1988
END_YEAR = 2025
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


def add_series(results, flow_code, product, series, data_sources, comment='ok'):
    """
    Appends one result row per year in EXPECTED_YEARS from a {year: value}
    series (kt). Every model year must be present in the series.
    """
    for year in sorted(EXPECTED_YEARS):
        results.append({
            'flow_name': flow_code,
            'product': product,
            'year': year,
            'value': float(series[year]),
            'comment': comment,
            'data_sources': data_sources,
        })


def flow_by_year(results, flow_code, products=None):
    """
    Sums an already computed flow over the given products (all products if
    None) and returns {year: value}. Raises KeyError if the flow has not been
    computed yet, which means the pools ran in the wrong order.
    """
    series = {}
    for rec in results:
        if rec['flow_name'] != flow_code:
            continue
        if products is not None and rec['product'] not in products:
            continue
        series[rec['year']] = series.get(rec['year'], 0.0) + rec['value']
    if not series:
        raise KeyError(f"Flow '{flow_code}' (products {products}) has not been computed")
    return series
