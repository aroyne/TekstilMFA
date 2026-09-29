#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RW (rest of the world) pool: flows from abroad into the Norwegian system.
"""
from calculations.trade import add_trade_flow_by_product, trade_kt_by_year, import_unit_value_by_year
from calculations.timeseries import interpolate
from calculations.utils import EXPECTED_YEARS, PRODUCTS, add_series


def execute_calculations_rw(preloaded_data, current_params, dataset_noise, anchors, computed):
    results = []

    add_trade_flow_by_product(
        results, preloaded_data, dataset_noise,
        flow_code='RW.RW-DI.RT-Finished textile products import-TOT',
        is_import=True, category='finished', products=PRODUCTS,
    )
    _add_private_imports_mc(results, preloaded_data, current_params, dataset_noise)
    _add_direct_online_imports_mc(results, anchors)

    return results


def _add_private_imports_mc(results, preloaded_data, current_params, dataset_noise):
    """
    Clothing and shoes bought on cross-border day trips (D16). SSB reports
    shopping in NOK at Swedish retail prices; it is converted to mass with the
    customs import value per kg of CL+FW times a retail markup, and split
    between CL and FW by their shares of registered import mass.
    """
    flow_code = 'RW.RW-US.HH-Private imports-TOT'
    data_sources = 'SSB 05678, 14221; SSB 08801 unit values'

    # 'crossborder' <- data_files/SSB_grensehandel_05678_14221.csv:
    # day-trip shopping in total (mill. NOK, 2004-2022) and for clothing and
    # shoes (mill. NOK, 2023-2025)
    crossborder = preloaded_data['crossborder']
    noise_val = dataset_noise['grensehandel']
    clothing_share = current_params['crossborder_clothing_share']
    markup = current_params['retail_markup']

    unit_value = import_unit_value_by_year(preloaded_data, ['CL', 'FW'])
    cl_kt = trade_kt_by_year(preloaded_data, dataset_noise, True, 'finished', ['CL'])
    fw_kt = trade_kt_by_year(preloaded_data, dataset_noise, True, 'finished', ['FW'])

    first_year = min(crossborder['total'])
    total_kt = {}
    for year in EXPECTED_YEARS:
        if year in crossborder['clothing']:
            mill_nok = crossborder['clothing'][year]
        elif year in crossborder['total']:
            mill_nok = crossborder['total'][year] * clothing_share
        else:
            continue
        # mill. NOK / (NOK/kg) = million kg = kt
        total_kt[year] = mill_nok * noise_val / (unit_value[year] * markup)

    # Before the SSB series starts (2004) the mass is held at the first
    # year's level (D16).
    for year in EXPECTED_YEARS:
        if year < first_year:
            total_kt[year] = total_kt[first_year]

    for product, kt in (('CL', cl_kt), ('FW', fw_kt)):
        series = {y: total_kt[y] * kt[y] / (cl_kt[y] + fw_kt[y]) for y in EXPECTED_YEARS}
        add_series(results, flow_code, product, series, data_sources)


def _add_direct_online_imports_mc(results, anchors):
    """
    Low-value parcels bought directly from foreign web shops, which are not in
    08801 under their HS codes (D7). Official VOEC data 2022-2025, one
    estimate for 2018, and zero around 2000.
    """
    flow_code = 'RW.RW-US.HH-Direct online imports-TOT'
    data_sources = 'Tolletaten VOEC via NORSUS 2026; Watson et al. 2020'
    for product, anchor_id in (('CL', 'online_direct_CL'), ('HT', 'online_direct_HT')):
        add_series(results, flow_code, product, interpolate(anchors[anchor_id], EXPECTED_YEARS), data_sources)
