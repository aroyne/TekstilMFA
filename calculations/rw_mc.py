#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RW (rest of the world) pool: flows from abroad into the Norwegian system.
"""
from calculations.trade import add_trade_flow_by_product


def execute_calculations_rw(preloaded_data, current_params, dataset_noise):
    results = []

    add_trade_flow_by_product(
        results, preloaded_data, dataset_noise,
        flow_code='RW.RW-DI.RT-Finished textile products import-TOT',
        is_import=True, category='finished', products=['CL', 'HT', 'FW'],
    )

    return results
