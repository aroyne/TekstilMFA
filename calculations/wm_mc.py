#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WM (waste management) pool. Everything entering residual and mixed waste
(WM.RS) is split between landfill (share from SSB's waste accounts, D15),
export for incineration abroad (share of residual waste exported, SSB
KOSTRA, D11) and domestic incineration (the rest). The treatment shares are
not product specific, so these flows have no product dimension.
"""
import numpy as np

from calculations.timeseries import interpolate
from calculations.utils import YEARS

INFLOWS_WM_RS = [
    'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
    'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT',
    'US.IC-WM.RS-Institutional textile waste-TOT',
    'CO.SO-WM.RS-Sorting residues-TOT',
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
    """Balance of WM.RS."""
    landfill = mfa.flows['WM.RS-WM.LF-Landfilling of textiles-TOT'].values
    export = mfa.flows['WM.RS-RW.RW-Residual waste export for incineration-TOT'].values
    incineration = _total_wm_rs(mfa) - landfill - export
    if (incineration < 0).any():
        year = YEARS[int(np.argmax(incineration < 0))]
        raise ValueError(f"Landfill + export share exceeds 1 in {year}")
    mfa.flows['WM.RS-WM.IN-Domestic incineration-TOT'].values[...] = incineration
