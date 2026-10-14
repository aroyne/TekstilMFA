#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
US (use) pool. Discards from households come from official and commissioned
statistics (D8, D15, D17); the change of the in-use stock is the residual of
the US.HH balance and is computed from the flows by calculations.system.
Collection and residual waste are not split by product within the CORE
group (CL+HT+FW and retail yarn).

Other textile goods in households (CA, TA, OM) and all goods used by
institutions and businesses have no discard statistics and are discarded
by a cohort model with lifetimes per product, an exception to D8. Sacks
(SA) are packaging and are discarded in the year they are supplied (D13).
"""
from calculations.cohorts import use_cohorts
from calculations.fibre_layer import (INSTITUTIONAL_COHORT_PRODUCTS, NEW_GOODS_TO_HOUSEHOLDS, OTHER_HOUSEHOLD_GOODS,
                                      supply_composition)
from calculations.system import clip_negative
from calculations.timeseries import interpolate
from calculations.utils import (CORE_GROUP_PRODUCTS, FIBRE_GROUPS, MATERIALS, PRODUCT_GROUPS, PRODUCTS, YEARS,
                                core_group_only)

COHORT_PRODUCTS = OTHER_HOUSEHOLD_GOODS
# Pick analyses of residual waste exist from 2009; before that the waste per
# inhabitant is held at the 2009 level.
FIRST_RESIDUAL_ANCHOR = 2009


def execute_calculations_us(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _separate_collection_mc(mfa)
    _reusable_residual_waste_mc(mfa, preloaded_data, anchors)
    _worn_residual_waste_mc(mfa, preloaded_data, current_params, anchors)
    _laundry_fibre_release_mc(mfa, preloaded_data, current_params, anchors)
    _air_and_dust_release_mc(mfa, current_params)
    _institutional_recycling_mc(mfa, anchors)
    _institutional_waste_mc(mfa, current_params)
    _industrial_laundry_release_mc(mfa, preloaded_data, current_params, anchors)


def _separate_collection_mc(mfa):
    """
    Separately collected from households = exported used textiles + the part
    kept in Norway (D17) - unsold clothing donated by retailers, which is
    exported with the used textiles (D27). A negative value is not physical
    and is clipped at 0; the clipped mass is recorded and reported on the
    flow page.
    """
    exported = mfa.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values
    retained = mfa.flows['CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'].values
    donated = mfa.flows['DI.RT-CO.CO-Unsold goods donated-TOT'].values.sum(axis=1)
    clip_negative(mfa, 'US.HH-CO.CO-Separate collection from households-TOT',
                  exported + retained - core_group_only(donated), balance_of='target')


def _residual_core(preloaded_data, anchors):
    """
    CL+HT+FW in household residual and bulky waste from pick analyses: 2009
    (Laitala et al. 2012), 2018, 2022 and 2025 (Mepex, via Watson et al. 2020
    and NORSUS 2023 and 2026), interpolated between them. Before 2009 the
    waste per inhabitant is held at the 2009 level. SSB's textile accounts
    for 1998 (58.5 kt) are not used as a level: the clothing in the waste in
    1991 and 1998 (34.8 and 47.2 kt) is nearly equal to net clothing imports
    those years (34.5 and 46.6 kt), so it was probably calculated from the
    supply, and it would make the stock shrink in the early 1990s.
    """
    # 'population' <- data_files/SSB_05803_befolkning_1985_2026.csv:
    # population on 1 January (SSB 05803); the mean of two years is used
    population = preloaded_data['population']
    residual = interpolate(anchors['residual_core'])
    first = YEARS.index(FIRST_RESIDUAL_ANCHOR)
    per_inhabitant = residual[first] / population[FIRST_RESIDUAL_ANCHOR]
    for i, year in enumerate(YEARS[:first]):
        # residual[i] / residual[first] is the gap factor of the held value
        # (D30), so the extrapolation keeps its growing uncertainty.
        residual[i] = per_inhabitant * population[year] * residual[i] / residual[first]
    return residual


def _reusable_residual_waste_mc(mfa, preloaded_data, anchors):
    """
    Part of the CORE residual textiles that could have been reused (D18),
    share from the pick analyses. The analyses cover CL+HT+FW only, so the
    other products are 0 here and counted as worn.
    """
    reusable_share = interpolate(anchors['reusable_share_residual'], upper=1.0)
    mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values[...] = (
        core_group_only(_residual_core(preloaded_data, anchors) * reusable_share))


def _worn_residual_waste_mc(mfa, preloaded_data, current_params, anchors):
    """
    CORE: residual textiles that are not reusable. CA, TA and OM: the
    outflow of a cohort model of the goods sold to households, with Weibull
    lifetimes (carpets 10, tarpaulins and tents 4, other made-up articles 2
    years), because there are no discard statistics for them (an exception
    to D8). Sacks (SA) are not used by households (D13).
    """
    flow = mfa.flows['US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT']
    reusable = mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values
    flow.values[...] = core_group_only(_residual_core(preloaded_data, anchors)) - reusable
    discards = _other_goods_discards(mfa, current_params)
    for j, product in enumerate(COHORT_PRODUCTS):
        flow.values[:, PRODUCT_GROUPS.index(product)] = discards[:, j]


def _other_goods_discards(mfa, current_params):
    """Outflow of the household cohort model for CA, TA and OM, array (year, product)."""
    sales = mfa.flows['DI.RT-US.HH-Sales to households-TOT'].values
    inflow = sales[:, [PRODUCTS.index(p) for p in COHORT_PRODUCTS], None]
    return use_cohorts(inflow, COHORT_PRODUCTS, current_params)['outflow'][:, :, 0]


def _supply(preloaded_data, current_params):
    # 'fibre_composition' <- parameters/fibre_composition.csv (fibre groups of
    # import mass whose HS code states no fibre), passed with the data
    return supply_composition(preloaded_data, current_params, preloaded_data['fibre_composition'])


def _household_textile_stock(mfa, preloaded_data, current_params):
    """
    Stock of textile fibre in the CORE group of US.HH by fibre group, array
    (year, fibre group), from the cohort model of new goods entering the
    households, with the composition of registered imports.
    """
    supply = _supply(preloaded_data, current_params)
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    new_goods = sum(mfa.flows[code].values for code in NEW_GOODS_TO_HOUSEHOLDS)[:, core]
    stock = use_cohorts(new_goods[:, :, None] * supply[:, core, :], CORE_GROUP_PRODUCTS,
                              current_params)['stock'].sum(axis=1)
    return stock[:, [MATERIALS.index(g) for g in FIBRE_GROUPS]]


def _laundry_fibre_release_mc(mfa, preloaded_data, current_params, anchors):
    """
    Fibres released from household textiles in washing machines and sent to
    wastewater treatment. Mepex (Sundt et al. 2014, cited in Sundt et al.
    2016 for the Norwegian Environment Agency) estimated about 600 t
    synthetic microfibres a year from household laundry. The release per kt
    synthetic fibre in the household stock is set so that the synthetic
    release in 2014 matches that estimate, and the other fibre groups
    (cotton, wool, regenerated cellulose, other) release the same per kt
    (Lant et al. 2020 found that most fibres released in real laundry are
    natural). The stock is that of the household cohort model, because the
    residual stock of the balance is probably too high. The fibre layer
    splits the flow into synthetic and other fibres.
    """
    stock = _household_textile_stock(mfa, preloaded_data, current_params)
    mfa.flows['US.HH-WM.WW-Fibre release in laundry-TOT'].values[...] = core_group_only(
        _laundry_release_per_kt(stock, anchors) * stock.sum(axis=1))


def _laundry_release_per_kt(household_stock, anchors):
    """Fibres released in laundry per kt textile fibre in use, from the synthetic release in 2014."""
    synthetic = household_stock[:, FIBRE_GROUPS.index('SYN')]
    return anchors['laundry_release_synthetic'][2014] / synthetic[YEARS.index(2014)]


def _air_and_dust_release_mc(mfa, current_params):
    """
    Fibres released to air and indoor dust while household textiles are worn
    and used, set to the same level as the release in laundry, with a factor
    of 1 (0.3-3): De Falco et al. (2020) found a release during wear of the
    same order as in washing. There are no Norwegian data.
    """
    laundry = mfa.flows['US.HH-WM.WW-Fibre release in laundry-TOT'].values
    mfa.flows['US.HH-EN.AI-Fibre release to air and dust-TOT'].values[...] = (
        laundry * current_params['air_release_relative_to_laundry'])


def _institutional_recycling_mc(mfa, anchors):
    """
    Textiles from industry (mainly hotels and health care) recycled at Norsk
    Tekstilgjenvinning: their share of the plant's intake (75 of 153 t in
    2024, 358 of 651 t in 2025) times the mass recycled (93 and 364 t),
    i.e. 46 and 200 t (de Sadeleer & Rubach 2026, fig. 3-8 and 3-9). Counted
    as household textiles (linen) and zero before 2024 (D34).
    """
    flow = mfa.flows['US.IC-WM.RC-Institutional textiles to recycling-TOT']
    flow.values[...] = 0.0
    flow.values[:, PRODUCTS.index('HT')] = interpolate(anchors['recycling_institutional'])


def _institutional_waste_mc(mfa, current_params):
    """
    Goods discarded by institutions and businesses: the outflow of a cohort
    model of the goods sold to them, with Weibull lifetimes per product
    (workwear 3, footwear 2, institutional linen 2, carpets 10, tarpaulins
    and awnings 5 and other made-up articles 2 years; all but workwear are
    assumptions). There are no discard statistics for this sector: textiles
    from businesses are mostly in mixed waste in SSB's waste accounts.
    Sacks (SA) are packaging and are discarded in the year they are
    supplied (D13), and retail yarn is not sold to this sector.
    """
    sales = mfa.flows['DI.RT-US.IC-Sales to institutions and businesses-TOT'].values
    discarded = sales.copy()
    cohort = [PRODUCTS.index(p) for p in INSTITUTIONAL_COHORT_PRODUCTS]
    discarded[:, cohort] = use_cohorts(sales[:, cohort, None], INSTITUTIONAL_COHORT_PRODUCTS, current_params,
                                       stock='US.IC')['outflow'][:, :, 0]
    # Textiles recycled at Norsk Tekstilgjenvinning are subtracted; a
    # negative value is not physical and is clipped at 0.
    recycled = mfa.flows['US.IC-WM.RC-Institutional textiles to recycling-TOT'].values
    clip_negative(mfa, 'US.IC-WM.RS-Institutional textile waste-TOT', discarded - recycled)


def _industrial_laundry_release_mc(mfa, preloaded_data, current_params, anchors):
    """
    Fibres released when textiles used by institutions and businesses are
    washed (mostly in industrial laundries) and sent to wastewater
    treatment. There are no Norwegian data, so the release per kt textile
    fibre in use is the same as in household laundry, applied to the textile
    stock of the US.IC cohort model per product. Institutional textiles are
    washed more often, but industrial laundries often filter and treat their
    water; the two pull in opposite directions. Sacks have no stock and
    release nothing.
    """
    supply = _supply(preloaded_data, current_params)
    sales = mfa.flows['DI.RT-US.IC-Sales to institutions and businesses-TOT'].values
    cohort = [PRODUCTS.index(p) for p in INSTITUTIONAL_COHORT_PRODUCTS]
    stock = use_cohorts(sales[:, cohort, None] * supply[:, cohort, :], INSTITUTIONAL_COHORT_PRODUCTS,
                        current_params, stock='US.IC')['stock']
    textile = stock[:, :, [MATERIALS.index(g) for g in FIBRE_GROUPS]].sum(axis=2)
    release_per_kt = _laundry_release_per_kt(_household_textile_stock(mfa, preloaded_data, current_params), anchors)
    flow = mfa.flows['US.IC-WM.WW-Fibre release in industrial laundry-TOT']
    flow.values[...] = 0.0
    flow.values[:, cohort] = release_per_kt * textile

