#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CO (collection, sorting and second-hand retail) pool. Everything is anchored
in the annual export of used textiles (HS 6309+6310) from SSB 08801 (D17):
nearly all separately collected textiles are exported, and the small part
kept in Norway is a share of the export anchored in the national mappings.
Collected textiles are not split by product group ('CORE').
"""
from calculations.trade import trade_kt_by_year
from calculations.timeseries import interpolate
from calculations.utils import EXPECTED_YEARS, add_series


def execute_calculations_co(preloaded_data, current_params, dataset_noise, anchors, computed):
    results = []

    export = trade_kt_by_year(preloaded_data, dataset_noise, False, 'used', ['UT'])
    add_series(results, 'CO.CO-RW.RW-Export of unsorted collected textiles-TOT', 'CORE', export,
               'SSB 08801 (HS 6309+6310 export)')

    retained_share = interpolate(anchors['retained_share_collected'], EXPECTED_YEARS)
    reuse_fraction = interpolate(anchors['reuse_fraction_retained'], EXPECTED_YEARS)
    retained = {y: export[y] * retained_share[y] for y in EXPECTED_YEARS}
    reuse = {y: retained[y] * reuse_fraction[y] for y in EXPECTED_YEARS}
    rest = {y: retained[y] - reuse[y] for y in EXPECTED_YEARS}

    sources = 'SSB 08801 x anchors from Watson 2020, Rubach 2023, de Sadeleer & Rubach 2026'
    add_series(results, 'CO.CO-CO.SO-Collected textiles to domestic sorting-TOT', 'CORE', retained, sources)
    add_series(results, 'CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT', 'CORE', reuse, sources)
    # Recycling and rejects are not yet separated (WM.RC is P2); both go to
    # residual waste here.
    add_series(results, 'CO.SO-WM.RS-Sorting residues-TOT', 'CORE', rest, sources)
    add_series(results, 'CO.RE-US.HH-Secondhand sales to households-TOT', 'CORE', reuse, sources)

    return results
