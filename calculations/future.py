#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Future module (phase D, D12): the years 2026-2050 on the same register as
the historical model, in its own flodym system.

There are no statistics for the future, so the model is turned around
(design note 2026-11-02): supply is the 2025 level per inhabitant times
SSB's population projection, household discards come from the cohort
model of the stock in use, and the flows after discarding are split by
shares. The stock in use grows by a realistic amount only; the rest of the
gap between supply and recorded discards leaves as household textiles in
commercial and bulky waste (D42).

A Scenario holds every uncertain factor (X) of step 2. The reference path
(Scenario.reference) carries the 2025 values on and has today's policy
only: the ban on destroying unsold goods (2026), EPR (2027) and the waste
shipment rules (2027) are measures for step 3, so that their effect is
measured against the same scenarios. Factors that change over time move
linearly from their 2025 value to their value in TARGET_YEAR and are held
after it.

The starting point is the deterministic run (iteration 0) of the
historical model, which is a closed system; medians per flow are not
(D12, decision 2026-11-05). The base year is 2025 alone: it is where the
data end and where the cohort model is scaled to the statistics. The
uncertainty of the history enters as factors (discard level and
collection share in 2025), not by drawing historical iterations.

Every function sets one flow, or the outflows of one process that are
split by shares, in the order the flows depend on each other.
"""
import dataclasses

import numpy as np

from calculations.cohorts import use_cohorts
from calculations.fibre_layer import (FIBRE_CLASSES, INSTITUTIONAL_COHORT_PRODUCTS, OTHER_HOUSEHOLD_GOODS,
                                      new_goods_to_households)
from calculations.system import clip_negative, to_dims
from calculations.utils import (CORE_GROUP_PRODUCTS, END_YEAR, PRODUCT_GROUPS, PRODUCTS, YEARS,
                                core_group_only)

BASE_YEAR = END_YEAR
HORIZON = 2050
TARGET_YEAR = 2035
FUTURE_YEARS = list(range(BASE_YEAR + 1, HORIZON + 1))
BASE = YEARS.index(BASE_YEAR)
CORE = PRODUCT_GROUPS.index('CORE')
POPULATION_ALTERNATIVES = ['LLL', 'MMM', 'HHH']

SALES_HH = 'DI.RT-US.HH-Sales to households-TOT'
SALES_IC = 'DI.RT-US.IC-Sales to institutions and businesses-TOT'
ONLINE = 'RW.RW-US.HH-Direct online imports-TOT'
COLLECTION = 'US.HH-CO.CO-Separate collection from households-TOT'
REUSABLE = 'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'
WORN = 'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT'
INSTITUTIONAL_RECYCLING = 'US.IC-WM.RC-Institutional textiles to recycling-TOT'
INSTITUTIONAL_RELEASE = 'US.IC-EN.WA-Fibre release in industrial laundry-TOT'
RECYCLED_FIBRE = 'WM.RC-MA.FI-Recycled fibre to domestic spinning-TOT'
COMMERCIAL_BULKY = 'US.HH-WM.RS-Household textiles in commercial and bulky waste-TOT'
DOMESTIC_GOODS = 'MA.TX-DI.RT-Domestic finished products-TOT'
RAW_WOOL = 'PS.WO-MA.FI-Norwegian raw wool-TOT'
TO_DOMESTIC_SORTING = 'CO.CO-CO.SO-Collected textiles to domestic sorting-TOT'
UNSORTED_EXPORT = 'CO.CO-RW.RW-Export of unsorted collected textiles-TOT'
SORTED_REUSE = 'CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'
SORTED_RECYCLING = 'CO.SO-WM.RC-Sorted for recycling-TOT'
SORTING_RESIDUES = 'CO.SO-WM.RS-Sorting residues-TOT'
SECONDHAND_SALES = 'CO.RE-US.HH-Secondhand sales to households-TOT'
INCINERATION = 'WM.RS-WM.IN-Domestic incineration-TOT'
RESIDUAL_EXPORT = 'WM.RS-RW.RW-Residual waste export for incineration-TOT'
LANDFILL = 'WM.RS-WM.LF-Landfilling of textiles-TOT'
SORTING_OUTCOMES = (SORTED_REUSE, SORTED_RECYCLING, SORTING_RESIDUES)

# Flows that follow the population: the 2025 value per inhabitant times
# the consumption trend of the scenario for flows split by product.
PER_CAPITA_FLOWS = [
    # Final demand of households and of institutions and businesses.
    SALES_HH,
    SALES_IC,
    ONLINE,
    'RW.RW-US.HH-Private imports-TOT',
    # Re-export and unsold goods are taken to keep their 2025 ratio to the
    # market; the ban on destruction (2026) is a measure, not reference.
    'DI.RT-RW.RW-Export of finished textile products-TOT',
    'DI.RT-WM.RS-Unsold goods discarded-TOT',
    'DI.RT-CO.CO-Unsold goods donated-TOT',
    # Domestic manufacturing keeps its 2025 share of the market.
    DOMESTIC_GOODS,
    'MA.FI-DI.RT-Domestic hand knitting yarn-TOT',
    # Imported used textiles sorted in Norway.
    'RW.RW-CO.SO-Used textile import-TOT',
    # The laundry washed follows the population, not the textile stock (D37),
    # and the other household releases are tied to it.
    'US.HH-EN.WA-Fibre release in laundry-TOT',
    'US.HH-EN.AI-Fibre release to air and dust-TOT',
    'US.HH-WM.RS-Tumble dryer lint-TOT',
    'US.HH-WM.RS-Household dust fibres-TOT',
]

# Intermediate flows of textile manufacturing, which follow the domestic
# finished products, so that MA.TX keeps its 2025 balance per material.
MANUFACTURING_FLOWS = [
    'MA.FI-MA.TX-Yarn to textile manufacturing-TOT',
    'MA.TX-RW.RW-Textile export-TOT',
    'MA.TX-WM.RS-Preconsumer production waste-TOT',
    'MA.TX-WM.RC-Production waste to recycling-TOT',
]

# Flows held at their 2025 value: they are set by capacity or by sheep
# numbers, not by the population.
HELD_FLOWS = [
    RAW_WOOL,
    'MA.FI-EN.WA-Wool scouring loss-TOT',
    # Mostly Norwegian wool, so it follows the wool, not the population.
    'MA.FI-RW.RW-Fibre and yarn export-TOT',
    # Linen from hotels and hospitals at Norsk Tekstilgjenvinning.
    INSTITUTIONAL_RECYCLING,
]


@dataclasses.dataclass(frozen=True)
class Scenario:
    """
    The uncertain factors (X) of one future scenario (phase D, step 2,
    claude_tekst/2026-11-05_D2_scenarier_forslag.md). Values named *_2035
    are reached linearly in TARGET_YEAR from their 2025 value and held after.
    """
    population: str                 # X1: SSB 14740 alternative, LLL, MMM or HHH
    consumption_trend_core: float   # X2: change per year to 2035 per inhabitant, CL+HT+FW+YA
    consumption_trend_other: float  # X3: the same for CA, SA, TA, OM
    lifetime_level: float           # X4: CORE lifetimes in US.HH, whole period
    lifetime_new_cohorts_2035: float  # X4b: factor on the lifetime of cohorts entering from 2026
    stock_growth: float             # X5: growth of the CORE stock in US.HH, kg per inhabitant per year (D42)
    discard_level: float            # X6: factor on the scaling of the cohort model to 2025
    collection_share: float         # X7: separate collection share of recorded discards, held
    domestic_sorting_share_2035: float  # X8: share of collected textiles sorted in Norway
    sorting_outcome_2035: tuple     # X9: (reuse, recycling, residues) shares of what is sorted in Norway
    recycled_fibre_capacity_2035: float  # X10: recycled fibre spun in Norway, kt
    residual_export_share_2035: float  # X11: share of residual waste incinerated abroad
    synthetic_shift_2035: float     # X12: change in the synthetic share of new goods (fibre layer)

    @classmethod
    def reference(cls, hist):
        """The 2025 values carried on, from the closed historical system."""
        def base(code):
            return hist.flows[code].values[BASE]
        recorded = sum(base(c)[CORE] for c in (COLLECTION, REUSABLE, WORN))
        collected = _process_inflow(hist, 'CO.CO', ('t', 'g'))[BASE, CORE]
        sorted_in = _process_inflow(hist, 'CO.SO', ('t', 'g'))[BASE, CORE]
        residual = _process_inflow(hist, 'WM.RS', ('t',))[BASE]
        return cls(
            population='MMM', consumption_trend_core=0.0, consumption_trend_other=0.0,
            lifetime_level=1.0, lifetime_new_cohorts_2035=1.0, stock_growth=0.5, discard_level=1.0,
            collection_share=base(COLLECTION)[CORE] / recorded,
            domestic_sorting_share_2035=base(TO_DOMESTIC_SORTING)[CORE] / collected,
            sorting_outcome_2035=tuple(base(c)[CORE] / sorted_in for c in SORTING_OUTCOMES),
            recycled_fibre_capacity_2035=base(RECYCLED_FIBRE),
            residual_export_share_2035=base(RESIDUAL_EXPORT) / residual,
            synthetic_shift_2035=0.0,
        )


def path(start, end, years=FUTURE_YEARS):
    """Linear from start in BASE_YEAR to end in TARGET_YEAR, held after; array (year,)."""
    weight = np.minimum(np.array(years) - BASE_YEAR, TARGET_YEAR - BASE_YEAR) / (TARGET_YEAR - BASE_YEAR)
    return start + (end - start) * weight


class Reference:
    """
    The closed historical system (iteration 0), the scenario, the
    population and the parameters of iteration 0 with the scenario's
    lifetimes and stock growth, shared by the flow functions. The cohort
    models are run once and kept here.
    """

    def __init__(self, hist, population, current_params, scenario):
        """population: {year: mean population} for 2025 and FUTURE_YEARS, in the scenario's alternative."""
        self.hist = hist
        self.scenario = scenario
        self.current_params = dict(current_params)
        for product in CORE_GROUP_PRODUCTS:
            self.current_params[f'lifetime_mean_US.HH_{product}'] *= scenario.lifetime_level
        self.current_params['future_stock_growth_kg_per_capita'] = scenario.stock_growth
        self.population = np.array([population[year] for year in FUTURE_YEARS])
        self.growth = self.population / population[BASE_YEAR]
        years = np.minimum(np.array(FUTURE_YEARS) - BASE_YEAR, TARGET_YEAR - BASE_YEAR)
        rate = np.array([scenario.consumption_trend_core if p in CORE_GROUP_PRODUCTS
                         else scenario.consumption_trend_other for p in PRODUCTS])
        self.consumption_trend = (1.0 + rate[None, :]) ** years[:, None]
        # Lifetime of each CORE cohort relative to the parameters: 1 for the
        # history, the scenario's path for cohorts entering from 2026.
        self.household_lifetime_factor = np.concatenate([
            np.ones((len(YEARS), len(CORE_GROUP_PRODUCTS))),
            np.repeat(path(1.0, scenario.lifetime_new_cohorts_2035)[:, None], len(CORE_GROUP_PRODUCTS), axis=1)])

    def base(self, code):
        return self.hist.flows[code].values[BASE]

    def per_capita(self, code, letters):
        base = self.base(code)
        values = self.growth.reshape((-1,) + (1,) * base.ndim) * base
        if 'p' in letters:
            values = values * self.consumption_trend
        return values

    def held(self, code):
        return np.repeat(self.base(code)[None], len(FUTURE_YEARS), axis=0)


def future_composition_data(preloaded_data, synthetic_shift_2035=0.0):
    """
    Trade by fibre class for the fibre layer of the future years
    (compute_fibre_layer): the 2025 mass per fibre class of each product
    in every future year, so that goods supplied keep the 2025
    composition, except for the synthetic share of finished goods, which
    moves by synthetic_shift_2035 (share points of the textile classes, X12)
    at the expense of the other textile classes in proportion. The
    composition of discards still changes, because it comes from the cohort
    models, which carry the older cohorts on.
    """
    # 'imports_by_fibre_class' and 'intermediate_by_fibre_class' <-
    # data_files/Tab_08801_textiles.csv (SSB 08801) and
    # parameters/hs_main_fibre.csv, summed when the data is loaded
    def held(kg):
        return np.repeat(kg[BASE][None], len(FUTURE_YEARS), axis=0)
    finished = held(preloaded_data['imports_by_fibre_class'])
    textile = [i for i, c in enumerate(FIBRE_CLASSES) if c != 'NT']
    syn = FIBRE_CLASSES.index('SYN')
    total = finished[:, :, textile].sum(axis=2)
    # A product with no textile classes in 2025 has nothing to shift.
    share = np.divide(finished[:, :, syn], total, out=np.zeros_like(total), where=total > 0)
    new_share = np.minimum(1.0, share + path(0.0, synthetic_shift_2035)[:, None])
    others = [i for i in textile if i != syn]
    scale = np.divide(1.0 - new_share, 1.0 - share, out=np.ones_like(share), where=share < 1.0)
    finished[:, :, others] *= scale[:, :, None]
    finished[:, :, syn] = new_share * total
    return {
        'imports_by_fibre_class': finished,
        'intermediate_by_fibre_class': {key: held(kg) for key, kg in
                                        preloaded_data['intermediate_by_fibre_class'].items()},
    }


def execute_future(fut, ref):
    _per_capita_flows(fut, ref)
    _manufacturing_flows(fut, ref)
    _held_flows(fut, ref)
    _online_returns(fut, ref)
    _finished_products_import(fut)
    _household_discards(fut, ref)
    _worn_residual_waste(fut, ref)
    _institutional_waste(fut, ref)
    _industrial_laundry_release(fut, ref)
    _collected_textiles(fut, ref)
    _domestic_sorting(fut, ref)
    _secondhand_sales(fut)
    _commercial_and_bulky_waste(fut, ref)
    _recycled_fibre(fut, ref)
    _export_for_recycling(fut)
    _residual_waste_treatment(fut, ref)
    _fabric_import(fut)
    _fibre_and_yarn_import(fut)


def _per_capita_flows(fut, ref):
    """
    The 2025 value per inhabitant times the population (SSB 14740, the
    scenario's alternative), for every flow in PER_CAPITA_FLOWS. Flows split
    by product also follow the scenario's consumption trend per inhabitant
    (X2 for CL+HT+FW+YA, X3 for the other goods; 0 in the reference path),
    compounded to 2035 and held after.
    """
    for code in PER_CAPITA_FLOWS:
        fut.flows[code].values[...] = ref.per_capita(code, fut.flows[code].dims.letters)


def _manufacturing_flows(fut, ref):
    """
    The 2025 value times the growth of domestic finished products (all
    products), for every flow in MANUFACTURING_FLOWS: yarn, fabric export
    and production waste follow what MA.TX makes, so MA.TX keeps its 2025
    balance per material and fabric import (the balance) does not turn
    negative when consumption falls.
    """
    growth = fut.flows[DOMESTIC_GOODS].values.sum(axis=1) / ref.base(DOMESTIC_GOODS).sum()
    for code in MANUFACTURING_FLOWS:
        fut.flows[code].values[...] = growth * ref.base(code)


def _held_flows(fut, ref):
    """The 2025 value in every future year, for every flow in HELD_FLOWS."""
    for code in HELD_FLOWS:
        fut.flows[code].values[...] = ref.held(code)


def _online_returns(fut, ref):
    """Direct online imports times the return share of iteration 0 (D38), as in the history."""
    fut.flows['US.HH-RW.RW-Returns of direct online purchases-TOT'].values[...] = (
        fut.flows[ONLINE].values * ref.current_params['online_return_share'])


def _finished_products_import(fut):
    """
    The balance of DI.RT per product: what leaves retail minus what comes
    from domestic manufacturing. Import is what the market does not get
    from Norway, so it is the flow that adjusts. A negative value is not
    physical and is clipped at 0.
    """
    out = sum(fut.flows[code].values for code in (
        SALES_HH, SALES_IC, 'DI.RT-RW.RW-Export of finished textile products-TOT',
        'DI.RT-WM.RS-Unsold goods discarded-TOT', 'DI.RT-CO.CO-Unsold goods donated-TOT'))
    domestic = (fut.flows['MA.TX-DI.RT-Domestic finished products-TOT'].values
                + fut.flows['MA.FI-DI.RT-Domestic hand knitting yarn-TOT'].values)
    clip_negative(fut, 'RW.RW-DI.RT-Finished textile products import-TOT', out - domestic)


def household_cohorts(hist, fut, current_params, lifetime_factor):
    """
    Cohort model of the CORE group in US.HH over the historical and the
    future years: new goods entering the households from 1988 (iteration 0)
    and from 2026 (this module), with the spin-up from 1950, the lifetimes
    in current_params and lifetime_factor per cohort (array (year,
    product)). Returns the use_cohorts result over YEARS + FUTURE_YEARS,
    summed over the products, as arrays (year,).
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    inflow = np.concatenate([new_goods_to_households(hist.flows), new_goods_to_households(fut.flows)])[:, core]
    cohorts = use_cohorts(inflow[:, :, None], CORE_GROUP_PRODUCTS, current_params, cohort_factor=lifetime_factor)
    return {'outflow': cohorts['outflow'][:, :, 0].sum(axis=1), 'stock': cohorts['stock'][:, :, 0].sum(axis=1),
            'stock_1987': cohorts['stock_1987'][:, 0].sum()}


def _household_discards(fut, ref):
    """
    CORE discards from households: the outflow of the cohort model of the
    stock in use, scaled so that it equals the statistics in 2025
    (separate collection plus reusable and worn textiles in residual
    waste), times the scenario's discard level (X6, the uncertainty of the
    2025 statistics; 1 in the reference path). The scale factor s (about
    0.89) is held. The gap between the cohort model and the statistics in
    2018-2025 (10-27 kt per year, D40) is not carried on as a growing
    stock: most of it is discards that the statistics do not capture
    (D42), see _commercial_and_bulky_waste.

    Lifetimes: the CORE lifetimes are multiplied by the scenario's level
    (X4, 1-1.75, the span of the stock diagnosis, for the whole period, so
    s is computed again) and the lifetime of cohorts entering from 2026 by
    a factor reaching X4b in 2035 (0.75-1: shorter with ultra fast fashion;
    longer lifetimes are the durability measure of step 3).

    Separate collection is the scenario's share of the scaled discards (X7,
    the 2025 share in the reference path, about 45 %), held: any increase
    comes from measures in step 3. The rest is split between reusable and
    worn textiles in residual waste by their 2025 ratio.
    """
    cohorts = household_cohorts(ref.hist, fut, ref.current_params, ref.household_lifetime_factor)
    recorded = {code: ref.base(code)[CORE] for code in (COLLECTION, REUSABLE, WORN)}
    statistics = sum(recorded.values())
    ref.scale = statistics / cohorts['outflow'][BASE] * ref.scenario.discard_level
    ref.cohorts = cohorts
    discards = ref.scale * cohorts['outflow'][len(YEARS):]
    ref.core_discards = discards
    collected = ref.scenario.collection_share
    ref.reusable_share = (1.0 - collected) * recorded[REUSABLE] / (recorded[REUSABLE] + recorded[WORN])
    fut.flows[COLLECTION].values[...] = core_group_only(discards * collected)
    fut.flows[REUSABLE].values[...] = core_group_only(discards * ref.reusable_share)


def _worn_residual_waste(fut, ref):
    """
    CORE: the rest of the scaled cohort discards after separate collection
    and reusable textiles (_household_discards). CA, TA and OM: the outflow
    of the cohort model of the goods sold to households, with sales from
    1988 to 2050, as in the history (an exception to D8). Sacks are not used
    by households (D13).
    """
    worn_share = 1.0 - ref.scenario.collection_share - ref.reusable_share
    flow = fut.flows[WORN]
    flow.values[...] = core_group_only(ref.core_discards * worn_share)
    sales = np.concatenate([ref.hist.flows[SALES_HH].values, fut.flows[SALES_HH].values])
    inflow = sales[:, [PRODUCTS.index(p) for p in OTHER_HOUSEHOLD_GOODS], None]
    outflow = use_cohorts(inflow, OTHER_HOUSEHOLD_GOODS, ref.current_params)['outflow'][len(YEARS):, :, 0]
    for j, product in enumerate(OTHER_HOUSEHOLD_GOODS):
        flow.values[:, PRODUCT_GROUPS.index(product)] = outflow[:, j]


def _institutional_cohorts(fut, ref):
    sales = np.concatenate([ref.hist.flows[SALES_IC].values, fut.flows[SALES_IC].values])
    cohort = [PRODUCTS.index(p) for p in INSTITUTIONAL_COHORT_PRODUCTS]
    return sales, cohort, use_cohorts(sales[:, cohort, None], INSTITUTIONAL_COHORT_PRODUCTS, ref.current_params,
                                      stock='US.IC')


def _institutional_waste(fut, ref):
    """
    Goods discarded by institutions and businesses: the outflow of the
    cohort model of the goods sold to them, with sales from 1988 to 2050,
    as in the history. Sacks (SA) are discarded in the year they are
    supplied (D13). Textiles recycled at Norsk Tekstilgjenvinning (held at
    2025) are subtracted; a negative value is not physical and is clipped
    at 0.
    """
    sales, cohort, cohorts = _institutional_cohorts(fut, ref)
    discarded = sales[len(YEARS):].copy()
    discarded[:, cohort] = cohorts['outflow'][len(YEARS):, :, 0]
    clip_negative(fut, 'US.IC-WM.RS-Institutional textile waste-TOT',
                  discarded - fut.flows[INSTITUTIONAL_RECYCLING].values)


def _industrial_laundry_release(fut, ref):
    """
    Fibres released in industrial laundry: the 2025 release per kt of goods
    in the US.IC cohort model, per product, times the future stock. In the
    history the release per kt is that of household laundry; holding the
    2025 ratio keeps it.
    """
    _, cohort, cohorts = _institutional_cohorts(fut, ref)
    stock = cohorts['stock'][:, :, 0]
    per_kt = ref.base(INSTITUTIONAL_RELEASE)[cohort] / stock[BASE]
    flow = fut.flows[INSTITUTIONAL_RELEASE]
    flow.values[...] = 0.0
    flow.values[:, cohort] = per_kt * stock[len(YEARS):]


def _process_inflow(mfa, process, letters):
    return sum(to_dims(f, letters).values for f in mfa.flows.values() if f.to_process.name == process)


def _collected_textiles(fut, ref):
    """
    What is collected (from households and unsold goods donated by
    retailers) is sorted in Norway at the scenario's share (X8, 5.5 % in
    2025, moving to its 2035 value) and the rest exported unsorted. The
    collected textiles are all in the CORE group, so the other groups are
    0. Sorting before export (WSR, 2027) is a measure in step 3.
    """
    collected = _process_inflow(fut, 'CO.CO', ('t', 'g'))[:, CORE]
    base_share = ref.base(TO_DOMESTIC_SORTING)[CORE] / _process_inflow(ref.hist, 'CO.CO', ('t', 'g'))[BASE, CORE]
    share = path(base_share, ref.scenario.domestic_sorting_share_2035)
    fut.flows[TO_DOMESTIC_SORTING].values[...] = core_group_only(collected * share)
    fut.flows[UNSORTED_EXPORT].values[...] = core_group_only(collected * (1.0 - share))


def _domestic_sorting(fut, ref):
    """
    What is sorted in Norway (collected textiles and imported used
    textiles) goes to second-hand sale in Norway, to recycling and to
    residues by the scenario's shares (X9, a truncated flat Dirichlet;
    about 37, 6 and 57 % in 2025), moving from the 2025 shares to their
    2035 values.
    """
    sorted_in = _process_inflow(fut, 'CO.SO', ('t', 'g'))[:, CORE]
    base_in = _process_inflow(ref.hist, 'CO.SO', ('t', 'g'))[BASE, CORE]
    for code, target in zip(SORTING_OUTCOMES, ref.scenario.sorting_outcome_2035):
        share = path(ref.base(code)[CORE] / base_in, target)
        fut.flows[code].values[...] = core_group_only(sorted_in * share)


def _secondhand_sales(fut):
    """Everything sorted for second-hand sale in Norway is sold to households (CO.RE has no stock)."""
    fut.flows[SECONDHAND_SALES].values[...] = fut.flows[SORTED_REUSE].values


def _commercial_and_bulky_waste(fut, ref):
    """
    CL+HT+FW from households that leave as commercial or bulky waste
    outside the pick analyses (D42): the balance of the CORE group in US.HH
    after a realistic growth of the stock in use (X5, 0.3-1 kg per
    inhabitant per year, 0.5 in the reference path; a wardrobe of 50-100
    kg growing 0.5-1 % a year, cf. Watson et al. 2018). Without it the
    residual stock would grow by 12-14 kt a year to 2050, which the
    wardrobe studies do not support; in Denmark the same gap was judged to
    be mostly discards that are not measured (Watson et al. 2018). A
    negative value (supply below discards plus growth) is not physical and
    is clipped at 0.
    """
    core = ('t', 'g')
    inflow = sum(to_dims(f, core).values for f in fut.flows.values() if f.to_process.name == 'US.HH')
    outflow = sum(to_dims(f, core).values for code, f in fut.flows.items()
                  if f.from_process.name == 'US.HH' and code != COMMERCIAL_BULKY)
    growth = ref.current_params['future_stock_growth_kg_per_capita'] * ref.population / 1e6
    clip_negative(fut, COMMERCIAL_BULKY, core_group_only(inflow[:, CORE] - outflow[:, CORE] - growth))


def _recycled_fibre(fut, ref):
    """
    Recycled fibre spun in Norway: the capacity of the scenario (X10,
    0.19 kt in 2025, moving to its 2035 value), but no more than what
    reaches material recycling (WM.RC) and no more than Norwegian spinning
    uses beyond Norwegian wool (the outflows of MA.FI minus raw wool), so
    that fibre import does not turn negative. What is recycled beyond that
    is exported for recycling.
    """
    capacity = path(ref.base(RECYCLED_FIBRE), ref.scenario.recycled_fibre_capacity_2035)
    spinning = sum(to_dims(f, ('t',)).values for f in fut.flows.values()
                   if f.from_process.name == 'MA.FI') - fut.flows[RAW_WOOL].values
    fut.flows[RECYCLED_FIBRE].values[...] = np.minimum.reduce(
        [capacity, _process_inflow(fut, 'WM.RC', ('t',)), spinning])


def _export_for_recycling(fut):
    """
    The balance of WM.RC: what is recycled minus the recycled fibre spun in
    Norway. A negative value is not physical and is clipped at 0.
    """
    clip_negative(fut, 'WM.RC-RW.RW-Export for recycling-TOT',
                  _process_inflow(fut, 'WM.RC', ('t',)) - fut.flows[RECYCLED_FIBRE].values)


def _residual_waste_treatment(fut, ref):
    """
    Everything entering WM.RS is incinerated, abroad at the scenario's share
    (X11, 11.5 % in 2025, moving to its 2035 value; SSB 13035 gave 10-16 %
    in 2015-2025) and the rest in Norway. Landfill keeps its 2025 share,
    which is 0 under the 2009 ban.
    """
    inflow = _process_inflow(fut, 'WM.RS', ('t',))
    base_in = _process_inflow(ref.hist, 'WM.RS', ('t',))[BASE]
    export = path(ref.base(RESIDUAL_EXPORT) / base_in, ref.scenario.residual_export_share_2035)
    landfill = ref.base(LANDFILL) / base_in
    fut.flows[RESIDUAL_EXPORT].values[...] = inflow * export
    fut.flows[LANDFILL].values[...] = inflow * landfill
    fut.flows[INCINERATION].values[...] = inflow * (1.0 - export - landfill)


def _fabric_import(fut):
    """
    The balance of MA.TX: its outflows minus the yarn from MA.FI. A
    negative value is not physical and is clipped at 0.
    """
    out = sum(to_dims(f, ('t',)).values for f in fut.flows.values() if f.from_process.name == 'MA.TX')
    clip_negative(fut, 'RW.RW-MA.TX-Fabric import-TOT',
                  out - fut.flows['MA.FI-MA.TX-Yarn to textile manufacturing-TOT'].values)


def _fibre_and_yarn_import(fut):
    """
    The balance of MA.FI: its outflows minus Norwegian wool and recycled
    fibre. A negative value is not physical and is clipped at 0.
    """
    out = sum(to_dims(f, ('t',)).values for f in fut.flows.values() if f.from_process.name == 'MA.FI')
    own = fut.flows['PS.WO-MA.FI-Norwegian raw wool-TOT'].values + fut.flows[RECYCLED_FIBRE].values
    clip_negative(fut, 'RW.RW-MA.FI-Fibre and yarn import-TOT', out - own)
