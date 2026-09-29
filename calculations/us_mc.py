#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
US (use) pool. Discards from households come from official and commissioned
statistics (D8, D15, D17); the change of the in-use stock is the residual of
the US.HH balance. Collection and residual waste are not split by product
group ('CORE' = CL+HT+FW).

Products without discard statistics (other textile goods CA/TA/OM, and all
products used by institutions and businesses) are assumed to be discarded in
the year they are supplied (no stock change) until a better basis exists.
"""
from calculations.timeseries import interpolate
from calculations.utils import CORE_PRODUCTS, EXPECTED_YEARS, OTHER_PRODUCTS, PRODUCTS, add_series, flow_by_year

STEADY_STATE_NOTE = 'Discarded in the year supplied (no statistics)'


def execute_calculations_us(preloaded_data, current_params, dataset_noise, anchors, computed):
    results = []

    _add_collection_mc(results, computed)
    _add_residual_waste_mc(results, anchors)
    _add_steady_state_discards(results, computed)
    _add_household_stock_change(results, computed)

    return results


def _add_collection_mc(results, computed):
    """Separately collected = exported used textiles + the part kept in Norway (D17)."""
    exported = flow_by_year(computed, 'CO.CO-RW.RW-Export of unsorted collected textiles-TOT')
    retained = flow_by_year(computed, 'CO.CO-CO.SO-Collected textiles to domestic sorting-TOT')
    collected = {y: exported[y] + retained[y] for y in EXPECTED_YEARS}
    add_series(results, 'US.HH-CO.CO-Separate collection from households-TOT', 'CORE', collected,
               'SSB 08801 (HS 6309+6310 export) + retained share (D17)')


def _add_residual_waste_mc(results, anchors):
    """Textiles in household residual and bulky waste, pick analyses and SSB (D15)."""
    series = interpolate(anchors['residual_core'], EXPECTED_YEARS)
    add_series(results, 'US.HH-WM.RS-Textiles in residual and bulky waste-TOT', 'CORE', series,
               'SSB 1990-1998; Mepex pick analyses via Watson 2020, Rubach 2023, de Sadeleer & Rubach 2026')


def _add_steady_state_discards(results, computed):
    for product in OTHER_PRODUCTS:
        if product == 'SA':
            continue  # sacks are only used by businesses (D13)
        supplied = flow_by_year(computed, 'DI.RT-US.HH-Sales to households-TOT', [product])
        add_series(results, 'US.HH-WM.RS-Textiles in residual and bulky waste-TOT', product, supplied,
                   STEADY_STATE_NOTE)
    for product in PRODUCTS:
        supplied = flow_by_year(computed, 'DI.RT-US.IC-Sales to institutions and businesses-TOT', [product])
        add_series(results, 'US.IC-WM.RS-Institutional textile waste-TOT', product, supplied, STEADY_STATE_NOTE)


def _add_household_stock_change(results, computed):
    """
    Change of the household in-use stock of CL+HT+FW: all inflows minus the
    discards reported by the statistics. May be negative.
    """
    inflow_codes = [
        ('DI.RT-US.HH-Sales to households-TOT', CORE_PRODUCTS),
        ('RW.RW-US.HH-Private imports-TOT', None),
        ('RW.RW-US.HH-Direct online imports-TOT', None),
        ('CO.RE-US.HH-Secondhand sales to households-TOT', None),
    ]
    inflow = {y: 0.0 for y in EXPECTED_YEARS}
    for code, products in inflow_codes:
        series = flow_by_year(computed, code, products)
        for y in EXPECTED_YEARS:
            inflow[y] += series[y]

    collected = flow_by_year(results, 'US.HH-CO.CO-Separate collection from households-TOT')
    residual = flow_by_year(results, 'US.HH-WM.RS-Textiles in residual and bulky waste-TOT', ['CORE'])
    change = {y: inflow[y] - collected[y] - residual[y] for y in EXPECTED_YEARS}
    add_series(results, 'US.HH-US.HH-Stock change-TOT', 'CORE', change, 'Balance of US.HH (D8)')
