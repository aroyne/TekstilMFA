#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
US (use) pool. Discards from households come from official and commissioned
statistics (D8, D15, D17); the change of the in-use stock is the residual of
the US.HH balance and is computed from the flows by calculations.system.
Collection and residual waste are not split by product within the CORE
group (CL+HT+FW).

Products without discard statistics (other textile goods CA/TA/OM, and all
products used by institutions and businesses) are assumed to be discarded in
the year they are supplied (no stock change) until a better basis exists.
"""
from calculations.timeseries import interpolate
from calculations.utils import PRODUCT_GROUPS, PRODUCTS, core_group_only


def execute_calculations_us(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _separate_collection_mc(mfa)
    _reusable_residual_waste_mc(mfa, anchors)
    _worn_residual_waste_mc(mfa, anchors)
    _institutional_waste_mc(mfa)


def _separate_collection_mc(mfa):
    """Separately collected = exported used textiles + the part kept in Norway (D17)."""
    exported = mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    mfa.flows['US.HH-CO.CO-Separate collection from households-TOT'].values[...] = exported + retained


def _residual_core(anchors):
    """CL+HT+FW in household residual and bulky waste, SSB and Mepex pick analyses (D15)."""
    return interpolate(anchors['residual_core'])


def _reusable_residual_waste_mc(mfa, anchors):
    """
    Part of the CORE residual textiles that could have been reused (D18),
    share from the pick analyses. The analyses cover CL+HT+FW only, so the
    other products are 0 here and counted as worn.
    """
    reusable_share = interpolate(anchors['reusable_share_residual'])
    mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values[...] = (
        core_group_only(_residual_core(anchors) * reusable_share))


def _worn_residual_waste_mc(mfa, anchors):
    """
    CORE: residual textiles that are not reusable. CA, TA and OM: discarded
    in the year supplied. Sacks (SA) are not used by households (D13).
    """
    flow = mfa.flows['US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT']
    reusable = mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values
    sales = mfa.flows['DI.RT-US.HH-Sales to households-TOT'].values
    flow.values[...] = core_group_only(_residual_core(anchors)) - reusable
    for product in ('CA', 'TA', 'OM'):
        flow.values[:, PRODUCT_GROUPS.index(product)] = sales[:, PRODUCTS.index(product)]


def _institutional_waste_mc(mfa):
    """All products used by institutions and businesses: discarded in the year supplied."""
    sales = mfa.flows['DI.RT-US.IC-Sales to institutions and businesses-TOT'].values
    mfa.flows['US.IC-WM.RS-Institutional textile waste-TOT'].values[...] = sales
