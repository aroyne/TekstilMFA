#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WM (waste management) pool. Everything entering residual and mixed waste
(WM.RS) is split between landfill (share from SSB's waste accounts, D15),
export for incineration abroad (share of residual waste exported, SSB
KOSTRA, D11) and domestic incineration (the rest). The treatment shares are
not product specific, so these flows have no product dimension.
"""

from calculations.system import clip_negative
from calculations.timeseries import interpolate

INFLOWS_WM_RS = [
    'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
    'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT',
    'US.IC-WM.RS-Institutional textile waste-TOT',
    'CO.SO-WM.RS-Sorting residues-TOT',
    'MA.TX-WM.RS-Preconsumer production waste-TOT',
]


def execute_calculations_wm(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _landfilling_mc(mfa, anchors)
    _residual_export_mc(mfa, anchors)
    _domestic_incineration_mc(mfa)


def _total_wm_rs(mfa):
    return sum(mfa.flows[code].sum_to(('t',)).values for code in INFLOWS_WM_RS)


def _landfilling_mc(mfa, anchors):
    """Landfilled share from SSB Avfallsregnskap tekstiler 1990-1998, SSB 05281 and 10513 (D15)."""
    landfill_share = interpolate(anchors['landfill_share_residual'])
    mfa.flows['WM.RS-WM.LF-Landfilling of textiles-TOT'].values[...] = _total_wm_rs(mfa) * landfill_share


def _residual_export_mc(mfa, anchors):
    """
    Share of residual waste exported, SSB 13035 (D11). The share is measured
    for household residual waste and is applied to all textiles in WM.RS,
    including institutional waste.
    """
    export_share = interpolate(anchors['residual_export_share'])
    mfa.flows['WM.RS-RW.RW-Residual waste export for incineration-TOT'].values[...] = (
        _total_wm_rs(mfa) * export_share)


def _domestic_incineration_mc(mfa):
    """
    Balance of WM.RS. A negative balance (landfill and export shares
    summing to more than 1) is not physical and is clipped at 0; the
    clipped mass is recorded and reported on the flow page.
    """
    landfill = mfa.flows['WM.RS-WM.LF-Landfilling of textiles-TOT'].values
    export = mfa.flows['WM.RS-RW.RW-Residual waste export for incineration-TOT'].values
    clip_negative(mfa, 'WM.RS-WM.IN-Domestic incineration-TOT', _total_wm_rs(mfa) - landfill - export)
