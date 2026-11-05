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

A Scenario holds every uncertain factor (X) of step 2 and a Policy the
measures (L) of step 3 with their drawn effects. The reference path
(Scenario.reference with Policy.none) carries the 2025 values on and has
today's policy only: the ban on destroying unsold goods (2026), EPR (2027),
sorting before export, durability requirements and a tax on new textiles
are measures, so that their effect is measured against the same
scenarios. Factors that change over time move
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

from calculations.categories import (CATEGORIES, PRODUCT_OF_UNIT, TECHNICAL_SHAPE, UNITS, household_core_cohorts,
                                     policy_sensitivity, unit_lifetimes, unit_shares, unit_survival)
from calculations.cohorts import N_SPINUP, use_cohorts
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
SORTED_REUSE_EXPORT = 'CO.SO-RW.RW-Export of sorted textiles for reuse-TOT'
UNSOLD_DISCARDED = 'DI.RT-WM.RS-Unsold goods discarded-TOT'
UNSOLD_DONATED = 'DI.RT-CO.CO-Unsold goods donated-TOT'
# Products taxed by L5 and covered by the first durability act (L3: clothing).
TAXED_PRODUCTS = ['CL', 'HT', 'FW']
DURABLE_PRODUCTS = ['CL']
# Clothing is what is rented or shared (L8).
SHARED_PRODUCTS = ['CL']
# Function categories whose perceived lifetime shortens with ultra fast
# fashion (X4b): tops, bottoms and dresses, sports footwear.
FAST_FASHION_UNITS = ['K2', 'K3', 'S1']
# Categories reached by repair (L7): clothing and footwear.
REPAIRED_UNITS = CATEGORIES['CL'] + CATEGORIES['FW']
PRIVATE_IMPORTS = 'RW.RW-US.HH-Private imports-TOT'
ONLINE_RETURNS = 'US.HH-RW.RW-Returns of direct online purchases-TOT'
HAND_YARN = 'MA.FI-DI.RT-Domestic hand knitting yarn-TOT'
FINISHED_EXPORT = 'DI.RT-RW.RW-Export of finished textile products-TOT'
# Demand of CL+HT+FW in households (step 4): 'supply' holds the 2025 supply
# per inhabitant (steps 1-3), 'stock' derives purchases from the stock in
# use that households need (stock-driven).
DEMAND_MODES = ('supply', 'stock')
# Flows that make up the household market for new goods; in the
# stock-driven demand their CORE products follow the purchases. Exports and
# unsold goods keep their ratio to the market and domestic manufacturing its
# share of it (institutions buy a small part of the market, which this
# approximation scales too).
HOUSEHOLD_MARKET_FLOWS = [SALES_HH, ONLINE, PRIVATE_IMPORTS, FINISHED_EXPORT, UNSOLD_DISCARDED, UNSOLD_DONATED,
                          'MA.TX-DI.RT-Domestic finished products-TOT', HAND_YARN]

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
    reuse_market_2035: float        # X13: second-hand sales in Norway of textiles sorted here, kt
    # Step 4 (stock-driven demand). The desired stock in 2025 (X14) is the
    # stock of the cohort model in 2025, so it follows the lifetime level X4.
    desired_stock_trend: float      # X15: change per year to 2035 of the desired stock per inhabitant
    displacement: float             # X16: new purchases replaced per kg bought second-hand
    rebound: float                  # X17: share of a reduction in purchases that comes back
    # Parameters of the function categories (calculations/categories.py) as
    # (parameter_id, value) pairs that override those of iteration 0; empty
    # keeps them. X18 (share of durability used) follows from them.
    category_params: tuple = ()

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
            # No limit: second-hand sales in Norway follow what is sorted
            # for reuse, as in 2025.
            reuse_market_2035=float('inf'),
            # The middle of the spans of step 4.
            desired_stock_trend=0.0, displacement=0.475, rebound=0.5,
        )


@dataclasses.dataclass(frozen=True)
class Policy:
    """
    The measures (L) of one alternative in step 3
    (claude_tekst/2026-11-05_D3_tiltak_forslag.md), with their effects, which
    are uncertain factors drawn per scenario. Policy.none() is L0.
    """
    name: str
    collection_increase: float      # L1: share points added to separate collection, full in 2032
    collection_from_reusable: float  # L1: part of the increase taken from reusable residual textiles
    domestic_sorting: bool          # L2: everything collected is sorted in Norway from 2032
    durability_increase: float      # L3: longer lifetime of clothing cohorts from 2029
    destruction_ban: bool           # L4: unsold goods are donated instead of discarded
    destruction_ban_share_2027: float  # L4: share of unsold goods covered in 2027, all from 2030
    consumption_reduction: float    # L5: lower consumption per inhabitant of CL+HT+FW, full in 2030
    reuse_market_increase: float    # L6: factor on the Norwegian second-hand market, full in 2032
    repair_increase: float          # L7: share of repairable technical failures that are repaired, full in 2032
    sharing_reduction: float        # L8: lower need for clothing through rental and sharing, full in 2030
    recycled_content_2035: float    # L9: recycled share of the fibre in new goods (metric only)

    @classmethod
    def none(cls):
        return cls(name='L0', collection_increase=0.0, collection_from_reusable=0.0, domestic_sorting=False,
                   durability_increase=0.0, destruction_ban=False, destruction_ban_share_2027=0.0,
                   consumption_reduction=0.0, reuse_market_increase=1.0, repair_increase=0.0,
                   sharing_reduction=0.0, recycled_content_2035=0.0)


def ramp(start, end, years=FUTURE_YEARS):
    """0 up to start, linear to 1 in end, 1 after; array (year,)."""
    return np.clip((np.array(years) - start) / (end - start), 0.0, 1.0)


def path(start, end, years=FUTURE_YEARS):
    """Linear from start in BASE_YEAR to end in TARGET_YEAR, held after; array (year,)."""
    weight = np.minimum(np.array(years) - BASE_YEAR, TARGET_YEAR - BASE_YEAR) / (TARGET_YEAR - BASE_YEAR)
    return start + (end - start) * weight


class Reference:
    """
    The closed historical system (iteration 0), the scenario, the
    measures, the population and the parameters of iteration 0 with the
    scenario's lifetimes and stock growth, shared by the flow functions.
    The cohort models are run once and kept here.
    """

    def __init__(self, hist, population, current_params, scenario, policy, category_shares, demand='supply',
                 baseline_purchases=None):
        """
        population: {year: mean population} for 2025 and FUTURE_YEARS, in
        the scenario's alternative. category_shares: import mass shares of
        the function categories of CL and FW per historical year. demand:
        one of DEMAND_MODES. baseline_purchases: the stock-driven purchases
        of the same scenario without measures, array (year, unit), for the
        rebound.
        """
        if demand not in DEMAND_MODES:
            raise ValueError(f"Unknown demand {demand!r}")
        self.hist = hist
        self.scenario = scenario
        self.policy = policy
        self.demand = demand
        self.baseline_purchases = baseline_purchases
        self.purchases = None
        self.current_params = dict(current_params)
        for product in CORE_GROUP_PRODUCTS:
            self.current_params[f'lifetime_mean_US.HH_{product}'] *= scenario.lifetime_level
        self.current_params['future_stock_growth_kg_per_capita'] = scenario.stock_growth
        for name, value in scenario.category_params:
            if name not in self.current_params:
                raise KeyError(f"Unknown category parameter {name}")
            self.current_params[name] = value
        self.population = np.array([population[year] for year in FUTURE_YEARS])
        self.growth = self.population / population[BASE_YEAR]
        years = np.minimum(np.array(FUTURE_YEARS) - BASE_YEAR, TARGET_YEAR - BASE_YEAR)
        rate = np.array([scenario.consumption_trend_core if p in CORE_GROUP_PRODUCTS
                         else scenario.consumption_trend_other for p in PRODUCTS])
        self.consumption_trend = (1.0 + rate[None, :]) ** years[:, None]
        # Function categories of clothing and footwear (calculations/categories.py).
        self.history_unit_shares = unit_shares(category_shares)
        self.shares_2025 = {p: shares[-1] for p, shares in category_shares.items()}
        base_units = self.history_unit_shares[-1]
        # L5 (a tax on new textiles or measures against ultra fast fashion)
        # and L8 (rental and sharing), phased in from 2028 to 2030, act on
        # each category by its sensitivity (mean 1 over the 2025 mix): lower
        # purchases under the supply-driven demand, a lower desired stock
        # under the stock-driven demand.
        taxed = np.array([PRODUCT_OF_UNIT[u] in TAXED_PRODUCTS for u in UNITS], dtype=float)
        shared = np.array([PRODUCT_OF_UNIT[u] in SHARED_PRODUCTS for u in UNITS], dtype=float)
        sensitivity = policy_sensitivity(self.current_params, self.shares_2025)
        self.unit_policy = 1.0 - ramp(2027, 2030)[:, None] * sensitivity[None, :] * (
            policy.consumption_reduction * taxed[None, :] + policy.sharing_reduction * shared[None, :])
        self.policy_consumption = np.ones((len(FUTURE_YEARS), len(PRODUCTS)))
        product_policy = np.ones((len(FUTURE_YEARS), len(UNITS)))
        for product in CORE_GROUP_PRODUCTS:
            in_product = [i for i, u in enumerate(UNITS) if PRODUCT_OF_UNIT[u] == product]
            value = (base_units[in_product][None, :] * self.unit_policy[:, in_product]).sum(axis=1)
            self.policy_consumption[:, PRODUCTS.index(product)] = value
            product_policy[:, in_product] = value[:, None]
        self.future_unit_shares = base_units[None, :] * self.unit_policy / product_policy
        self.base_unit_shares = np.repeat(base_units[None, :], len(FUTURE_YEARS), axis=0)
        self.stock_unit_shares = None
        if demand == 'supply':
            self.consumption_trend = self.consumption_trend * self.policy_consumption
        # The household market follows the consumption trend; under the
        # stock-driven demand its CORE products are set to the purchases
        # (set_purchases).
        self.market_factor = self.consumption_trend.copy()
        self.desired_stock_trend = (1.0 + scenario.desired_stock_trend) ** years
        # Lifetime factors of the future cohorts by unit. L3 durability
        # (clothing from 2029) lengthens the technical lifetime; how much of
        # it is used follows from the share of discards due to wear in each
        # category. X4b (ultra fast fashion) shortens the perceived lifetime
        # of tops, bottoms and sports footwear. L7 repair lowers the technical
        # hazard of all clothing and footwear in use by the share of
        # repairable failures that are repaired (uptake times repairable
        # share), phased in 2027-2032: a period effect, so goods bought
        # before 2027 are reached too.
        future_years = np.array(FUTURE_YEARS)
        durable = np.array([u in CATEGORIES['CL'] for u in UNITS], dtype=float)
        fast = np.array([u in FAST_FASHION_UNITS for u in UNITS])
        self.technical_factor = 1.0 + policy.durability_increase * (future_years >= 2029)[:, None] * durable[None, :]
        self.perceived_factor = np.where(fast[None, :], path(1.0, scenario.lifetime_new_cohorts_2035)[:, None], 1.0)
        self.period_factor = None
        if policy.repair_increase > 0.0:
            _, _, repairable = unit_lifetimes(self.current_params, self.shares_2025)
            reached = np.array([u in REPAIRED_UNITS for u in UNITS], dtype=float)
            repaired = policy.repair_increase * ramp(2026, 2032)[:, None] * (repairable * reached)[None, :]
            self.period_factor = (1.0 - repaired) ** (-1.0 / TECHNICAL_SHAPE)

    def units(self, with_policy=True):
        """
        Unit setup of the household cohort model over YEARS + FUTURE_YEARS
        (calculations/categories.household_core_cohorts). Without the
        measures the 2025 category mix is held and only the scenario's
        lifetime factor (X4b) applies.
        """
        if not with_policy:
            shares = self.base_unit_shares
        elif self.stock_unit_shares is not None:
            shares = self.stock_unit_shares
        else:
            shares = self.future_unit_shares
        ones = np.ones((len(YEARS), len(UNITS)))
        return {
            'shares': np.concatenate([self.history_unit_shares, shares]),
            'shares_2025': self.shares_2025,
            'technical_factor': np.concatenate([ones, self.technical_factor if with_policy
                                                else np.ones_like(self.technical_factor)]),
            'perceived_factor': np.concatenate([ones, self.perceived_factor]),
            'period_factor': (np.concatenate([ones, self.period_factor])
                              if with_policy and self.period_factor is not None else None),
        }

    def base(self, code):
        return self.hist.flows[code].values[BASE]

    def per_capita(self, code, letters):
        base = self.base(code)
        values = self.growth.reshape((-1,) + (1,) * base.ndim) * base
        if code in HOUSEHOLD_MARKET_FLOWS:
            values = values * self.market_factor
        elif 'p' in letters:
            values = values * self.consumption_trend
        return values

    def base_new_goods(self):
        """New goods entering US.HH in 2025, array (CORE product,)."""
        core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
        return new_goods_to_households(self.hist.flows)[BASE, core]

    def set_purchases(self, purchases):
        """
        Sets the CORE household market and its category mix to the
        stock-driven purchases, array (year, unit).
        """
        self.purchases = purchases
        core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
        by_product = np.stack([purchases[:, [i for i, u in enumerate(UNITS) if PRODUCT_OF_UNIT[u] == p]].sum(axis=1)
                               for p in CORE_GROUP_PRODUCTS], axis=1)
        self.market_factor[:, core] = by_product / (self.base_new_goods()[None, :] * self.growth[:, None])
        product_of = [CORE_GROUP_PRODUCTS.index(PRODUCT_OF_UNIT[u]) for u in UNITS]
        self.stock_unit_shares = purchases / by_product[:, product_of]

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
    _destruction_ban(fut, ref)
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
    compounded to 2035 and held after, and the reduction of L5 for CL+HT+FW
    (-10 to -30 %, phased in 2028-2030; a tax on new textiles as the expert
    group recommends, Ikke rett fram 2025, or measures against ultra fast
    fashion as in France, law 2026-602; the effect is an assumption).
    """
    for code in PER_CAPITA_FLOWS:
        fut.flows[code].values[...] = ref.per_capita(code, fut.flows[code].dims.letters)


def _destruction_ban(fut, ref):
    """
    Under L4 (ban on destroying unsold clothing and footwear, ESPR art. 25:
    large firms from 19 July 2026, medium-sized from 2030) unsold goods that
    would be discarded are donated instead: the share covered is half of
    the 2027 share in 2026, the drawn share (50-90 %) in 2027 and all of
    them from 2030. Without L4 both flows keep their 2025 ratio to the
    market (_per_capita_flows).
    """
    if ref.policy.destruction_ban:
        years = np.array(FUTURE_YEARS)
        share_2027 = ref.policy.destruction_ban_share_2027
        covered = np.where(years == 2026, share_2027 / 2,
                           share_2027 + (1.0 - share_2027) * ramp(2027, 2030))
        moved = fut.flows[UNSOLD_DISCARDED].values * covered[:, None]
        fut.flows[UNSOLD_DISCARDED].values[...] -= moved
        fut.flows[UNSOLD_DONATED].values[...] += moved


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


def household_cohorts(fut, ref, with_policy=True, secondhand=None, inflow_divisor=None):
    """
    Cohort model of the CORE group in US.HH over the historical and the
    future years by unit (function categories of clothing and footwear,
    calculations/categories.py): new goods entering the households from
    1988 (iteration 0) and from 2026 (this module), with the spin-up from
    1950 and the unit setup of the Reference. secondhand (array (future
    year, unit)) is added to the future inflow under the stock-driven
    demand, where second-hand goods are part of the stock households hold.
    inflow_divisor (array (future year, CORE product)) divides the future
    new goods (to remove the effect of L5 and L8). Returns over YEARS +
    FUTURE_YEARS, summed over the products, 'outflow', 'stock' and 'broken'
    (discards damaged beyond easy repair) as arrays (year,), and
    'stock_1987'.
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    future = new_goods_to_households(fut.flows)[:, core]
    if inflow_divisor is not None:
        future = future / inflow_divisor
    new_goods = np.concatenate([new_goods_to_households(ref.hist.flows)[:, core], future])[:, :, None]
    extra = None
    if secondhand is not None:
        extra = np.concatenate([np.zeros((len(YEARS), len(UNITS))), secondhand])[:, :, None]
    cohorts = household_core_cohorts(new_goods, ref.units(with_policy), ref.current_params, extra)
    return {'outflow': cohorts['outflow'][:, :, 0].sum(axis=1), 'stock': cohorts['stock'][:, :, 0].sum(axis=1),
            'broken': cohorts['broken'][:, :, 0].sum(axis=1), 'stock_1987': cohorts['stock_1987'][:, 0].sum()}


def secondhand_by_unit(fut, ref):
    """
    Second-hand sales to households split over the CORE units by their
    shares of new goods in 2025, array (future year, unit). In the first
    pass of the stock-driven demand the flow is not set yet; the 2025 value
    per inhabitant is used then.
    """
    values = fut.flows[SECONDHAND_SALES].values[:, CORE]
    if np.isnan(values).any():
        values = ref.base(SECONDHAND_SALES)[CORE] * ref.growth
    product_split = ref.base_new_goods() / ref.base_new_goods().sum()
    split = np.array([product_split[CORE_GROUP_PRODUCTS.index(PRODUCT_OF_UNIT[u])] for u in UNITS])
    return values[:, None] * (split * ref.base_unit_shares[0])[None, :]


def stock_driven_purchases(fut, ref):
    """
    New CL+HT+FW+YA bought by households under the stock-driven demand
    (step 4), by unit (function categories of clothing and footwear), array
    (future year, unit). Households hold a desired stock in use of each
    unit: its stock in the cohort model in 2025 per inhabitant (which
    follows the lifetime level X4), times the population, the trend of the
    scenario (X15) and the measures that lower the need (L5, L8, by the
    sensitivity of the category). In each year they buy what is needed to
    reach it, given what survives of earlier cohorts (technical and
    perceived lifetimes with X4b, L3 and L7), minus the new goods that
    second-hand purchases replace (displacement X16, 0.1-0.85: Farrant et
    al. 2010 estimate 60-85 %, consumer surveys 10-60 %). What second-hand
    purchases do not replace adds to the stock. A share X17 of the
    reduction relative to the same scenario without measures comes back as
    purchases (rebound). Purchases cannot be negative.

    The cohort model's stock was shrinking slightly in 2025 (supply below its
    outflow), so holding the desired stock would make purchases jump in
    2026. The need is therefore multiplied by a factor per unit that makes
    2026 purchases equal the 2025 level per inhabitant, as the
    supply-driven demand does. In 2026 no measure acts yet, so the factor is
    the same with and without measures.
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    product_of = [CORE_GROUP_PRODUCTS.index(PRODUCT_OF_UNIT[u]) for u in UNITS]
    n_hist, n_full = len(YEARS), len(YEARS) + len(FUTURE_YEARS)
    sf, _, _ = unit_survival(ref.units(), ref.current_params, n_full)
    history = new_goods_to_households(ref.hist.flows)[:, core][:, product_of] * ref.history_unit_shares
    inflow = np.zeros((N_SPINUP + n_full, len(UNITS)))
    inflow[:N_SPINUP] = history[0] * ref.current_params['spinup_inflow_factor']
    inflow[N_SPINUP:N_SPINUP + n_hist] = history
    end_2025 = N_SPINUP + n_hist - 1
    stock_2025 = (sf[end_2025, :end_2025 + 1] * inflow[:end_2025 + 1]).sum(axis=0)
    desired = (stock_2025[None, :] * ref.growth[:, None] * ref.desired_stock_trend[:, None] * ref.unit_policy)
    secondhand = secondhand_by_unit(fut, ref)
    target_2026 = ref.base_new_goods()[product_of] * ref.base_unit_shares[0] * ref.growth[0]
    purchases = np.zeros((len(FUTURE_YEARS), len(UNITS)))
    for j in range(len(FUTURE_YEARS)):
        t = end_2025 + 1 + j
        surviving = (sf[t, :t] * inflow[:t]).sum(axis=0)
        need = (desired[j] - surviving) / sf[t, t] - ref.scenario.displacement * secondhand[j]
        if j == 0:
            calibration = target_2026 / need
        bought = np.clip(calibration * need, 0.0, None)
        if ref.baseline_purchases is not None:
            bought = bought + ref.scenario.rebound * np.clip(ref.baseline_purchases[j] - bought, 0.0, None)
        purchases[j] = bought
        inflow[t] = bought + secondhand[j]
    return purchases


def _policy_stock_change(fut, ref, cohorts):
    """
    Change of the CORE stock in use per year that the measures cause in the
    cohort model (longer lifetimes under L3 and L7 add to the stock, lower
    consumption under L5 and L8 takes from it), relative to the same
    scenario without measures, array (year,) over FUTURE_YEARS; 0 under L0.
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    without = household_cohorts(fut, ref, with_policy=False, inflow_divisor=ref.policy_consumption[:, core])
    return np.diff(cohorts['stock'] - without['stock'])[-len(FUTURE_YEARS):]


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
    s is computed again). Clothing and footwear are split into function
    categories with a technical and a perceived lifetime
    (calculations/categories.py); X4b shortens the perceived lifetime of
    tops, bottoms and sports footwear entering from 2026, and the measures
    L3 and L7 act on the technical lifetime (Reference).

    The condition of the discards follows from why they leave: goods no
    longer wanted and easily repairable damage are usable, the rest is
    broken (calibrated to Syversen et al. 2023, table 23). The usable share
    relative to 2025 scales the reusable share of residual waste.

    Separate collection is the scenario's share of the scaled discards (X7,
    the 2025 share in the reference path, about 45 %), held: any increase
    comes from measures. The rest is split between reusable and worn
    textiles in residual waste by their 2025 ratio. Under L1 (EPR with a
    collection target, WFD 2025/1892, Norwegian regulation proposed from
    2027) the share rises by the drawn increase (+10 to +35 share points,
    ambitious; Norway already collects about 45 %), phased in 2027-2032,
    taken 50-90 % from reusable textiles in residual waste and the rest from
    worn ones. Textiles in commercial and bulky waste (D42) are not reached.
    """
    cohorts = household_cohorts(fut, ref, secondhand=secondhand_by_unit(fut, ref) if ref.demand == 'stock' else None)
    if ref.demand == 'supply':
        ref.policy_stock_change = _policy_stock_change(fut, ref, cohorts)
    recorded = {code: ref.base(code)[CORE] for code in (COLLECTION, REUSABLE, WORN)}
    statistics = sum(recorded.values())
    ref.scale = statistics / cohorts['outflow'][BASE] * ref.scenario.discard_level
    ref.cohorts = cohorts
    discards = ref.scale * cohorts['outflow'][len(YEARS):]
    ref.core_discards = discards
    # Condition of the discards: the usable share (not damaged beyond easy
    # repair) in the cohort model relative to 2025 scales the reusable share
    # of residual waste and what sorting can send to reuse.
    usable = 1.0 - cohorts['broken'] / cohorts['outflow']
    ref.usable_share = usable[len(YEARS):]
    ref.usable_ratio = ref.usable_share / usable[BASE]
    base_collected = ref.scenario.collection_share
    base_reusable = ((1.0 - base_collected) * recorded[REUSABLE] / (recorded[REUSABLE] + recorded[WORN])
                     * ref.usable_ratio)
    increase = ref.policy.collection_increase * ramp(2026, 2032)
    # What L1 takes from reusable textiles cannot exceed what is there; the
    # rest of the increase comes from worn textiles.
    from_reusable = np.minimum(ref.policy.collection_from_reusable * increase, base_reusable)
    ref.collection_share = base_collected + increase
    ref.reusable_share = base_reusable - from_reusable
    if (ref.collection_share + ref.reusable_share > 1.0).any():
        raise ValueError("Collection and reusable residual textiles exceed the household discards")
    fut.flows[COLLECTION].values[...] = core_group_only(discards * ref.collection_share)
    fut.flows[REUSABLE].values[...] = core_group_only(discards * ref.reusable_share)


def _worn_residual_waste(fut, ref):
    """
    CORE: the rest of the scaled cohort discards after separate collection
    and reusable textiles (_household_discards). CA, TA and OM: the outflow
    of the cohort model of the goods sold to households, with sales from
    1988 to 2050, as in the history (an exception to D8). Sacks are not used
    by households (D13).
    """
    worn_share = 1.0 - ref.collection_share - ref.reusable_share
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
    0. Under L2 (sorting before export, WFD 2025/1892) everything collected
    is sorted in Norway by 2032, phased in from 2028. About 92 % of the
    unsorted export goes to sorters in other EU countries (SSB 08801, 2025),
    so a requirement met by sorting elsewhere in the EEA would hardly change
    the Norwegian flows; L2 is the strict variant.
    """
    collected = _process_inflow(fut, 'CO.CO', ('t', 'g'))[:, CORE]
    base_share = ref.base(TO_DOMESTIC_SORTING)[CORE] / _process_inflow(ref.hist, 'CO.CO', ('t', 'g'))[BASE, CORE]
    share = path(base_share, ref.scenario.domestic_sorting_share_2035)
    if ref.policy.domestic_sorting:
        share = share + (1.0 - share) * ramp(2027, 2032)
    fut.flows[TO_DOMESTIC_SORTING].values[...] = core_group_only(collected * share)
    fut.flows[UNSORTED_EXPORT].values[...] = core_group_only(collected * (1.0 - share))


def _domestic_sorting(fut, ref):
    """
    What is sorted in Norway (collected textiles and imported used
    textiles) goes to reuse, to recycling and to residues by the scenario's
    shares (X9, a truncated flat Dirichlet; about 37, 6 and 57 % in 2025),
    moving from the 2025 shares to their 2035 values; the reuse share moves
    with the usable share of the discards relative to 2025. What is sorted for
    reuse is sold second-hand in Norway up to the size of the market (X13,
    1.6 kt in 2025, moving to its 2035 value; L6 support for reuse
    multiplies it by 1.5-3, phased in 2027-2032), and the rest is exported
    as sorted textiles for reuse.
    """
    sorted_in = _process_inflow(fut, 'CO.SO', ('t', 'g'))[:, CORE]
    base_in = _process_inflow(ref.hist, 'CO.SO', ('t', 'g'))[BASE, CORE]
    shares = {code: path(ref.base(code)[CORE] / base_in, target)
              for code, target in zip(SORTING_OUTCOMES, ref.scenario.sorting_outcome_2035)}
    # The usable share of the discards relative to 2025 scales what can be
    # sorted for reuse; the difference moves to or from the residues.
    reuse = shares[SORTED_REUSE] * ref.usable_ratio
    shares[SORTING_RESIDUES] = shares[SORTING_RESIDUES] - (reuse - shares[SORTED_REUSE])
    shares[SORTED_REUSE] = reuse
    if (shares[SORTING_RESIDUES] < 0.0).any():
        raise ValueError("Sorting residues turn negative with the usable share of the discards")
    reuse = sorted_in * shares[SORTED_REUSE]
    market = (path(ref.base(SORTED_REUSE)[CORE], ref.scenario.reuse_market_2035)
              * (1.0 + (ref.policy.reuse_market_increase - 1.0) * ramp(2026, 2032)))
    domestic = np.minimum(reuse, market)
    fut.flows[SORTED_REUSE].values[...] = core_group_only(domestic)
    fut.flows[SORTED_REUSE_EXPORT].values[...] = core_group_only(reuse - domestic)
    for code in (SORTED_RECYCLING, SORTING_RESIDUES):
        fut.flows[code].values[...] = core_group_only(sorted_in * shares[code])


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
    be mostly discards that are not measured (Watson et al. 2018). Measures
    that change the stock in the cohort model (L3, L5) add that change to
    the growth (_policy_stock_change), so that longer lifetimes fill the
    stock and do not show up as commercial waste. A
    negative value (supply below discards plus growth) is not physical and
    is clipped at 0.

    Under the stock-driven demand (step 4) the cohort model holds the stock
    households need, so the stock grows as that model says, and this flow
    is the share of its outflow that the statistics do not see: (1 - s)
    times the outflow, with s the scaling of the cohort model to the 2025
    statistics. It is clipped at 0 where X6 makes s exceed 1.
    """
    if ref.demand == 'stock':
        # The cohort model holds the stock households need, so the share of
        # its outflow that the statistics do not see leaves here.
        clip_negative(fut, COMMERCIAL_BULKY, core_group_only((1.0 - ref.scale) * ref.cohorts['outflow'][len(YEARS):]))
        return
    core = ('t', 'g')
    inflow = sum(to_dims(f, core).values for f in fut.flows.values() if f.to_process.name == 'US.HH')
    outflow = sum(to_dims(f, core).values for code, f in fut.flows.items()
                  if f.from_process.name == 'US.HH' and code != COMMERCIAL_BULKY)
    growth = (ref.current_params['future_stock_growth_kg_per_capita'] * ref.population / 1e6
              + ref.policy_stock_change)
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
