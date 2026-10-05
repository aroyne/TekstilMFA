#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CO (collection, sorting and second-hand retail) pool. Everything is anchored
in the annual export of used textiles (HS 6309+6310) from SSB 08801 (D17):
nearly all separately collected textiles are exported, and the small part
kept in Norway is a share of the export anchored in the national mappings.
The collection statistics cover CL+HT+FW, so all CO flows are in the CORE
product group.
"""
from calculations.timeseries import interpolate
from calculations.trade import trade_kt
from calculations.utils import core_group_only


def execute_calculations_co(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _export_unsorted_mc(mfa, preloaded_data, dataset_noise)
    _to_domestic_sorting_mc(mfa, anchors)
    _sorted_for_secondhand_mc(mfa, anchors)
    _sorting_residues_mc(mfa)
    _secondhand_sales_mc(mfa)


def _export_unsorted_mc(mfa, preloaded_data, dataset_noise):
    """Export of used textiles and rags (HS 6309+6310), SSB 08801."""
    export = trade_kt(preloaded_data, dataset_noise, False, 'used', ['UT'])[:, 0]
    mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values[...] = core_group_only(export)


def _to_domestic_sorting_mc(mfa, anchors):
    """
    Collected textiles kept in Norway, as a share of the export. Anchors from
    Watson 2020, Rubach 2023 and de Sadeleer & Rubach 2026.
    """
    export = mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values
    retained_share = interpolate(anchors['retained_share_collected'])
    mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values[...] = (
        export * retained_share[:, None])


def _sorted_for_secondhand_mc(mfa, anchors):
    """Share of the retained textiles sold second-hand in Norway (same anchors)."""
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    reuse_fraction = interpolate(anchors['reuse_fraction_retained'])
    mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values[...] = (
        retained * reuse_fraction[:, None])


def _sorting_residues_mc(mfa):
    """
    Balance of CO.SO. Recycling and rejects are not yet separated (WM.RC is
    P2); both go to residual waste here.
    """
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    reuse = mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values
    mfa.flows['CO.SO-WM.RS-Sorting residues-TOT'].values[...] = retained - reuse


def _secondhand_sales_mc(mfa):
    """Balance of CO.RE: everything sorted for second-hand sale is sold."""
    reuse = mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values
    mfa.flows['CO.RE-US.HH-Secondhand sales to households-TOT'].values[...] = reuse
