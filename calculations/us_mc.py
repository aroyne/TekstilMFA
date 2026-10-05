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
    _residual_waste_mc(mfa, anchors)
    _institutional_waste_mc(mfa)


def _separate_collection_mc(mfa):
    """Separately collected = exported used textiles + the part kept in Norway (D17)."""
    exported = mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    mfa.flows['US.HH-CO.CO-Separate collection from households-TOT'].values[...] = exported + retained


def _residual_waste_mc(mfa, anchors):
    """
    CORE: textiles in household residual and bulky waste from SSB and the
    Mepex pick analyses (D15). CA, TA and OM: discarded in the year supplied.
    Sacks (SA) are not used by households (D13).
    """
    flow = mfa.flows['US.HH-WM.RS-Textiles in residual and bulky waste-TOT']
    sales = mfa.flows['DI.RT-US.HH-Sales to households-TOT'].values
    flow.values[...] = core_group_only(interpolate(anchors['residual_core']))
    for product in ('CA', 'TA', 'OM'):
        flow.values[:, PRODUCT_GROUPS.index(product)] = sales[:, PRODUCTS.index(product)]


def _institutional_waste_mc(mfa):
    """All products used by institutions and businesses: discarded in the year supplied."""
    sales = mfa.flows['DI.RT-US.IC-Sales to institutions and businesses-TOT'].values
    mfa.flows['US.IC-WM.RS-Institutional textile waste-TOT'].values[...] = sales
