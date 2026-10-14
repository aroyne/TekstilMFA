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
    _used_textile_import_mc(mfa, preloaded_data, dataset_noise)
    _sorted_for_secondhand_mc(mfa, preloaded_data, dataset_noise, anchors)
    _sorted_for_recycling_mc(mfa, anchors)
    _sorting_residues_mc(mfa)
    _secondhand_sales_mc(mfa)


def _export_unsorted_mc(mfa, preloaded_data, dataset_noise):
    """
    Export of used textiles and rags (HS 6309+6310), SSB 08801. In 2025,
    95.7 % was used clothing and other used textile articles (6309) and 4.3 %
    rags and sorted textile waste (6310) (de Sadeleer & Rubach 2026).
    """
    export = trade_kt(preloaded_data, dataset_noise, False, 'used', ['UT', 'RG']).sum(axis=1)
    mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values[...] = core_group_only(export)


def _to_domestic_sorting_mc(mfa, anchors):
    """
    Collected textiles kept in Norway, as a share of the export. Anchors from
    Watson 2020, Rubach 2023 and de Sadeleer & Rubach 2026.
    """
    export = mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values
    retained_share = interpolate(anchors['retained_share_collected'], upper=1.0)
    mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values[...] = (
        export * retained_share[:, None])


def _used_textile_import_mc(mfa, preloaded_data, dataset_noise):
    """
    Imports of used clothing (HS 6309) and rags (HS 6310), SSB 08801. The
    used clothing is sold in second-hand and vintage shops, and the rags
    (mostly wiping rags for industry) are used up and discarded.
    """
    imports = trade_kt(preloaded_data, dataset_noise, True, 'used', ['UT', 'RG']).sum(axis=1)
    mfa.flows['RW.RW-CO.SO-Used textile import-TOT'].values[...] = core_group_only(imports)


def _sorted_for_secondhand_mc(mfa, preloaded_data, dataset_noise, anchors):
    """
    Share of the retained textiles sold second-hand in Norway (same anchors
    as the share retained), plus imported used clothing (HS 6309).
    """
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    reuse_fraction = interpolate(anchors['reuse_fraction_retained'], upper=1.0)
    imported = trade_kt(preloaded_data, dataset_noise, True, 'used', ['UT'])[:, 0]
    mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values[...] = (
        retained * reuse_fraction[:, None] + core_group_only(imported))


def _sorted_for_recycling_mc(mfa, anchors):
    """
    Part of the rejects from domestic sorting (retained minus sold second
    hand, imported clothing not counted) sent to material recycling: 93 of
    467 t in 2018 (Watson et al. 2020, recycled abroad) and 142 of 364 t in
    2025 (de Sadeleer & Rubach 2026, recycled at Norsk Tekstilgjenvinning).
    The share is held at the 2018 level before 2018 (D34).
    """
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    reuse_fraction = interpolate(anchors['reuse_fraction_retained'], upper=1.0)
    rejects = retained * (1.0 - reuse_fraction[:, None])
    share = interpolate(anchors['recycling_share_sorting_rejects'], upper=1.0)
    mfa.flows['CO.SO-WM.RC-Sorted for recycling-TOT'].values[...] = rejects * share[:, None]


def _sorting_residues_mc(mfa):
    """
    Balance of CO.SO: rejects from domestic sorting that are not recycled,
    and imported rags, which are used up and discarded.
    """
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    imported = mfa.flows['RW.RW-CO.SO-Used textile import-TOT'].values
    reuse = mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values
    recycled = mfa.flows['CO.SO-WM.RC-Sorted for recycling-TOT'].values
    mfa.flows['CO.SO-WM.RS-Sorting residues-TOT'].values[...] = retained + imported - reuse - recycled


def _secondhand_sales_mc(mfa):
    """Balance of CO.RE: everything sorted for second-hand sale is sold."""
    reuse = mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values
    mfa.flows['CO.RE-US.HH-Secondhand sales to households-TOT'].values[...] = reuse
