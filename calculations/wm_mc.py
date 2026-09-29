#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WM (waste management) pool. Everything entering residual and mixed waste
(WM.RS) is split between landfill (share from SSB's waste accounts, D15),
export for incineration abroad (share of residual waste exported, SSB
KOSTRA, D11) and domestic incineration (the rest).
"""
from calculations.timeseries import interpolate
from calculations.utils import EXPECTED_YEARS, add_series, flow_by_year

INFLOWS_WM_RS = [
    'US.HH-WM.RS-Textiles in residual and bulky waste-TOT',
    'US.IC-WM.RS-Institutional textile waste-TOT',
    'CO.SO-WM.RS-Sorting residues-TOT',
]


def execute_calculations_wm(preloaded_data, current_params, dataset_noise, anchors, computed):
    results = []

    total = {y: 0.0 for y in EXPECTED_YEARS}
    for code in INFLOWS_WM_RS:
        series = flow_by_year(computed, code)
        for y in EXPECTED_YEARS:
            total[y] += series[y]

    landfill_share = interpolate(anchors['landfill_share_residual'], EXPECTED_YEARS)
    # The exported share is measured for household residual waste and is
    # applied to all textiles in WM.RS, including institutional waste.
    export_share = interpolate(anchors['residual_export_share'], EXPECTED_YEARS)
    landfill = {y: total[y] * landfill_share[y] for y in EXPECTED_YEARS}
    export = {y: total[y] * export_share[y] for y in EXPECTED_YEARS}
    incineration = {}
    for y in EXPECTED_YEARS:
        incineration[y] = total[y] - landfill[y] - export[y]
        if incineration[y] < 0:
            raise ValueError(f"Landfill + export share exceeds 1 in {y}: "
                             f"{landfill_share[y]:.3f} + {export_share[y]:.3f}")

    sources = 'SSB Avfallsregnskap tekstiler 1990-1998; SSB 05281; SSB 10513'
    add_series(results, 'WM.RS-WM.LF-Landfilling of textiles-TOT', 'ALL', landfill, sources)
    add_series(results, 'WM.RS-RW.RW-Residual waste export for incineration-TOT', 'ALL', export,
               'SSB 13035 (share of residual waste exported)')
    add_series(results, 'WM.RS-WM.IN-Domestic incineration-TOT', 'ALL', incineration, sources)
    add_series(results, 'WM.LF-WM.LF-Stock change-TOT', 'ALL', landfill, 'Landfilled textiles accumulate')

    return results
