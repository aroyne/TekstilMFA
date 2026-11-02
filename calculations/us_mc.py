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
import numpy as np

from calculations.cohorts import use_cohorts
from calculations.fibre_layer import (INSTITUTIONAL_COHORT_PRODUCTS, OTHER_HOUSEHOLD_GOODS,
                                      new_goods_to_households, supply_composition)
from calculations.system import clip_negative
from calculations.timeseries import interpolate
from calculations.utils import (CORE_GROUP_PRODUCTS, FIBRE_GROUPS, MATERIALS, PRODUCT_GROUPS, PRODUCTS, YEARS,
                                core_group_only)

COHORT_PRODUCTS = OTHER_HOUSEHOLD_GOODS
# Pick analyses of residual waste exist from 2009; before that the waste per
# inhabitant is held at the 2009 level plus what was not yet collected (D40).
FIRST_RESIDUAL_ANCHOR = 2009


def execute_calculations_us(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _separate_collection_mc(mfa)
    _reusable_residual_waste_mc(mfa, preloaded_data, anchors)
    _worn_residual_waste_mc(mfa, preloaded_data, current_params, anchors)
    _online_returns_mc(mfa, current_params)
    _laundry_fibre_release_mc(mfa, preloaded_data, current_params)
    _tumble_dryer_lint_mc(mfa, preloaded_data, current_params, anchors)
    _household_dust_fibres_mc(mfa, current_params)
    _air_and_dust_release_mc(mfa, preloaded_data, current_params, anchors)
    _institutional_recycling_mc(mfa, anchors)
    _institutional_waste_mc(mfa, current_params)
    _industrial_laundry_release_mc(mfa, preloaded_data, current_params)


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


def _residual_core(mfa, preloaded_data, anchors):
    """
    CL+HT+FW in household residual and bulky waste from pick analyses: 2009
    (Laitala et al. 2012), 2018, 2022 and 2025 (Mepex, via Watson et al. 2020
    and NORSUS 2023 and 2026), interpolated between them. SSB's textile
    accounts for 1998 (58.5 kt) are not used as a level: the clothing in the
    waste in 1991 and 1998 (34.8 and 47.2 kt) is nearly equal to net
    clothing imports those years (34.5 and 46.6 kt), so it was probably
    calculated from the supply, and it would make the stock shrink in the
    early 1990s.

    Before 2009 there are no pick analyses. The waste per inhabitant is held
    at the 2009 level, plus what was not yet collected separately: the
    separate collection per inhabitant in 2009 minus that of the year, times
    the population (D40). Textiles that were later collected went to residual
    waste before collection grew, so households did not discard less per
    inhabitant in 1990 than in 2009.
    """
    # 'population' <- data_files/SSB_05803_befolkning_1985_2026.csv:
    # population on 1 January (SSB 05803); the mean of two years is used
    population = preloaded_data['population']
    residual = interpolate(anchors['residual_core'])
    collection = mfa.flows['US.HH-CO.CO-Separate collection from households-TOT'].values[:, 0]
    first = YEARS.index(FIRST_RESIDUAL_ANCHOR)
    per_inhabitant = residual[first] / population[FIRST_RESIDUAL_ANCHOR]
    collected_per_inhabitant = collection[first] / population[FIRST_RESIDUAL_ANCHOR]
    for i, year in enumerate(YEARS[:first]):
        # residual[i] / residual[first] is the gap factor of the held value
        # (D30), so the held level keeps its growing uncertainty.
        not_yet_collected = collected_per_inhabitant * population[year] - collection[i]
        residual[i] = per_inhabitant * population[year] * residual[i] / residual[first] + not_yet_collected
    return residual


def _reusable_residual_waste_mc(mfa, preloaded_data, anchors):
    """
    Part of the CORE residual textiles that could have been reused (D18),
    share from the pick analyses. The analyses cover CL+HT+FW only, so the
    other products are 0 here and counted as worn.
    """
    reusable_share = interpolate(anchors['reusable_share_residual'], upper=1.0)
    mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values[...] = (
        core_group_only(_residual_core(mfa, preloaded_data, anchors) * reusable_share))


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
    flow.values[...] = core_group_only(_residual_core(mfa, preloaded_data, anchors)) - reusable
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
    new_goods = new_goods_to_households(mfa.flows)[:, core]
    stock = use_cohorts(new_goods[:, :, None] * supply[:, core, :], CORE_GROUP_PRODUCTS,
                              current_params)['stock'].sum(axis=1)
    return stock[:, [MATERIALS.index(g) for g in FIBRE_GROUPS]]


def _online_returns_mc(mfa, current_params):
    """
    Goods bought directly from foreign web shops and sent back (D38). The
    VOEC figures are deliveries to Norway, and returns to the web shop leave
    the country. Return share 0.2 (0.05-0.5): the EEA (2024) gives about
    20 % for clothing bought online, Zalando about 50 % and a German study
    (Bamberg) 24 % of parcels; Temu and Shein, which dominate the VOEC
    figures from 2024, are probably lower.
    """
    mfa.flows['US.HH-RW.RW-Returns of direct online purchases-TOT'].values[...] = (
        mfa.flows['RW.RW-US.HH-Direct online imports-TOT'].values * current_params['online_return_share'])


def _laundry_kt(preloaded_data, current_params):
    """
    Laundry washed in households per year (kt), array (year,): 280 kg per
    inhabitant (200-350; 70 loads of 4 kg, Mepex 2014 after Pakula &
    Stamminger 2010) times the population. It follows the population, not
    the textile stock: washing habits, not how much textile people own,
    set how much is washed (D37).
    """
    # 'population' <- data_files/SSB_05803_befolkning_1985_2026.csv:
    # population on 1 January (SSB 05803), as the mean of the year
    population = np.array([preloaded_data['population'][year] for year in YEARS])
    return current_params['laundry_kg_per_capita'] * population / 1e6


def _laundry_fibre_release_mc(mfa, preloaded_data, current_params):
    """
    Fibres released from household textiles in washing machines to
    wastewater, where the model stops following them: treatment, sludge and
    spread in the environment are not modelled (D35). The laundry washed per
    year times the release from real soiled laundry, 114 mg per kg (66-132;
    Lant et al. 2020, 79 loads from British households). About 96 % of what
    is released is natural or cellulosic fibre, so the fibre layer gives
    those fibres about 20 times the release per kg of synthetic fibre (D37).

    Mepex (Sundt et al. 2014) estimated 600 t synthetic microfibres a year,
    from single garments in laboratory tests, above their own two
    calculations (276 and 315 t); it is about ten times what real laundry
    gives and is kept for sensitivity only.
    """
    release = _laundry_kt(preloaded_data, current_params) * current_params['laundry_release_ppm'] * 1e-6
    mfa.flows['US.HH-EN.WA-Fibre release in laundry-TOT'].values[...] = core_group_only(release)


def _tumble_drying_release(preloaded_data, current_params, anchors):
    """
    Fibres released in tumble drying (kt), array (year,): laundry times the
    share of households with a tumble dryer (44 % in 1996 and 47 % in 2012,
    SSB via Store norske leksikon; held before and after) times the share of
    their loads that are dried (0.6, 0.4-0.8, assumption) times the release
    in drying, 300 mg per kg (256 for vented and 342 for condenser dryers,
    Cummins et al. 2023, real soiled laundry).
    """
    owners = interpolate(anchors['dryer_ownership_share'], upper=1.0)
    return (_laundry_kt(preloaded_data, current_params) * owners * current_params['tumble_dried_share']
            * current_params['drying_release_ppm'] * 1e-6)


def _tumble_dryer_lint_mc(mfa, preloaded_data, current_params, anchors):
    """
    Lint caught on the filter of tumble dryers, 88 % (86-91 %, Cummins et
    al. 2023) of the fibres released in drying (D37). The filter is emptied
    into residual waste, so the lint goes to WM.RS. Pick analyses count it
    as fines, not textile, so it is not in the residual waste anchors. It
    is mostly cotton (83-96 % on the filter from a 48 % cotton fabric, Lant
    et al. 2022), which the fibre layer gives through the higher release per
    kg of natural fibres. The rest goes to air (vented dryers) and is added
    to the release to air.
    """
    caught = _tumble_drying_release(preloaded_data, current_params, anchors) * current_params['lint_filter_share']
    mfa.flows['US.HH-WM.RS-Tumble dryer lint-TOT'].values[...] = core_group_only(caught)


def _wear_release(mfa, current_params):
    """
    Fibres shed while household textiles are worn and used, array (year,
    group): the release in laundry times a factor of 1 (0.3-3). De Falco et
    al. (2020) found a release during wear of the same order as in washing.
    There are no Norwegian data.
    """
    laundry = mfa.flows['US.HH-EN.WA-Fibre release in laundry-TOT'].values
    return laundry * current_params['air_release_relative_to_laundry']


def _household_dust_fibres_mc(mfa, current_params):
    """
    Fibres shed during wear that end up in house dust and are vacuumed:
    80 % (50-95 %, assumption) of the release during wear (D37). Mepex
    (2014) notes that the larger particles are vacuumed and go with residual
    waste to incineration. No measurements of textile fibre mass in vacuum
    cleaner bags have been found.
    """
    mfa.flows['US.HH-WM.RS-Household dust fibres-TOT'].values[...] = (
        _wear_release(mfa, current_params) * current_params['vacuumed_dust_share'])


def _air_and_dust_release_mc(mfa, preloaded_data, current_params, anchors):
    """
    Fibres to air and indoor dust that are not vacuumed (the rest of the
    release during wear, D37), plus the fibres from tumble drying that pass
    the lint filter and leave with the exhaust of vented dryers. In
    condenser dryers they go to the condensate, which is not split out.
    """
    exhaust = _tumble_drying_release(preloaded_data, current_params, anchors) * (
        1.0 - current_params['lint_filter_share'])
    mfa.flows['US.HH-EN.AI-Fibre release to air and dust-TOT'].values[...] = (
        _wear_release(mfa, current_params) * (1.0 - current_params['vacuumed_dust_share'])
        + core_group_only(exhaust))


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


def _industrial_laundry_release_mc(mfa, preloaded_data, current_params):
    """
    Fibres released when textiles used by institutions and businesses are
    washed (mostly in industrial laundries) to wastewater, where the model
    stops following them (D35). There are no Norwegian data, and the laundry
    washed in the sector is not known, so the release per kt textile fibre
    in use is that of household laundry (the household release divided by
    the textile stock of the household cohort model), applied to the textile
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
    household_release = mfa.flows['US.HH-EN.WA-Fibre release in laundry-TOT'].values.sum(axis=1)
    release_per_kt = household_release / _household_textile_stock(mfa, preloaded_data, current_params).sum(axis=1)
    flow = mfa.flows['US.IC-EN.WA-Fibre release in industrial laundry-TOT']
    flow.values[...] = 0.0
    flow.values[:, cohort] = release_per_kt[:, None] * textile

