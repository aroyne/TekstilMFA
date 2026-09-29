#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DI (distribution: wholesale and retail) pool.
"""
from calculations.trade import add_trade_flow_by_product
from calculations.utils import EXPECTED_YEARS, PRODUCTS, add_series, flow_by_year


def execute_calculations_di(preloaded_data, current_params, dataset_noise, anchors, computed):
    results = []

    # Export from DI.RT covers both re-export and export of domestically
    # manufactured products (D6).
    add_trade_flow_by_product(
        results, preloaded_data, dataset_noise,
        flow_code='DI.RT-RW.RW-Export of finished textile products-TOT',
        is_import=False, category='finished', products=PRODUCTS,
    )
    _add_sales_to_users_mc(results, current_params, computed)

    return results


def _add_sales_to_users_mc(results, current_params, computed):
    """
    Balance of DI.RT per product: registered imports minus exports, split
    between households and institutions/businesses. Sacks (SA) are packaging
    used by businesses (D13) and go entirely to US.IC. Domestic manufacturing
    (MA.TX) and unsold goods are not yet included.
    """
    data_sources = 'Balance of DI.RT (SSB 08801)'
    institutional_share = current_params['institutional_share']

    for product in PRODUCTS:
        imports = flow_by_year(computed, 'RW.RW-DI.RT-Finished textile products import-TOT', [product])
        exports = flow_by_year(results, 'DI.RT-RW.RW-Export of finished textile products-TOT', [product])
        share_ic = 1.0 if product == 'SA' else institutional_share

        to_hh, to_ic = {}, {}
        for year in EXPECTED_YEARS:
            net = imports[year] - exports[year]
            if net < 0:
                raise ValueError(f"Negative DI.RT balance for {product} in {year}: {net:.3f} kt")
            to_hh[year] = net * (1.0 - share_ic)
            to_ic[year] = net * share_ic

        add_series(results, 'DI.RT-US.HH-Sales to households-TOT', product, to_hh, data_sources)
        add_series(results, 'DI.RT-US.IC-Sales to institutions and businesses-TOT', product, to_ic, data_sources)
