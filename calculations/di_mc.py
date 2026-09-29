#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DI (distribution: wholesale and retail) pool.
"""
from calculations.trade import add_trade_flow_by_product
from calculations.utils import PRODUCTS


def execute_calculations_di(preloaded_data, current_params, dataset_noise):
    results = []

    # Export from DI.RT covers both re-export and export of domestically
    # manufactured products until the split in decision D6 is made.
    add_trade_flow_by_product(
        results, preloaded_data, dataset_noise,
        flow_code='DI.RT-RW.RW-Export of finished textile products-TOT',
        is_import=False, category='finished', products=PRODUCTS,
    )

    return results
