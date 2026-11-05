#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Future module (phase D, D12): the reference path 2026-2050 on the same
register as the historical model, in its own flodym system.

There are no statistics for the future, so the model is turned around
(design note 2026-11-02): supply is the 2025 level per inhabitant times
SSB's population projection, household discards come from the cohort
model of the stock in use, and the flows after discarding keep their 2025
shares. The reference path has today's policy only: the ban on destroying
unsold goods (2026), EPR (2027) and the waste shipment rules (2027) are
measures for steps 2 and 3, so that their effect is measured against one
reference.

The starting point is the deterministic run (iteration 0) of the
historical model, which is a closed system; medians per flow are not
(D12, decision 2026-11-05). The base year is 2025 alone: it is where the
data end and where the cohort model is scaled to the statistics.

Every function sets one flow, or the outflows of one process that are
split by their 2025 shares, in the order the flows depend on each other.
"""
import numpy as np

from calculations.cohorts import use_cohorts
from calculations.fibre_layer import INSTITUTIONAL_COHORT_PRODUCTS, OTHER_HOUSEHOLD_GOODS, new_goods_to_households
from calculations.system import clip_negative, to_dims
from calculations.utils import CORE_GROUP_PRODUCTS, END_YEAR, PRODUCT_GROUPS, PRODUCTS, YEARS, core_group_only

BASE_YEAR = END_YEAR
HORIZON = 2050
FUTURE_YEARS = list(range(BASE_YEAR + 1, HORIZON + 1))
BASE = YEARS.index(BASE_YEAR)
CORE = PRODUCT_GROUPS.index('CORE')

SALES_HH = 'DI.RT-US.HH-Sales to households-TOT'
SALES_IC = 'DI.RT-US.IC-Sales to institutions and businesses-TOT'
ONLINE = 'RW.RW-US.HH-Direct online imports-TOT'
COLLECTION = 'US.HH-CO.CO-Separate collection from households-TOT'
REUSABLE = 'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'
WORN = 'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT'
INSTITUTIONAL_RECYCLING = 'US.IC-WM.RC-Institutional textiles to recycling-TOT'
INSTITUTIONAL_RELEASE = 'US.IC-EN.WA-Fibre release in industrial laundry-TOT'
RECYCLED_FIBRE = 'WM.RC-MA.FI-Recycled fibre to domestic spinning-TOT'

# Flows that follow the population: the 2025 value per inhabitant is held.
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
    'MA.TX-DI.RT-Domestic finished products-TOT',
    'MA.FI-DI.RT-Domestic hand knitting yarn-TOT',
    'MA.FI-MA.TX-Yarn to textile manufacturing-TOT',
    'MA.TX-RW.RW-Textile export-TOT',
    'MA.TX-WM.RS-Preconsumer production waste-TOT',
    'MA.TX-WM.RC-Production waste to recycling-TOT',
    # Imported used textiles sorted in Norway.
    'RW.RW-CO.SO-Used textile import-TOT',
    # The laundry washed follows the population, not the textile stock (D37),
    # and the other household releases are tied to it.
    'US.HH-EN.WA-Fibre release in laundry-TOT',
    'US.HH-EN.AI-Fibre release to air and dust-TOT',
    'US.HH-WM.RS-Tumble dryer lint-TOT',
    'US.HH-WM.RS-Household dust fibres-TOT',
]

# Flows held at their 2025 value: they are set by capacity or by sheep
# numbers, not by the population.
HELD_FLOWS = [
    'PS.WO-MA.FI-Norwegian raw wool-TOT',
    'MA.FI-EN.WA-Wool scouring loss-TOT',
    # Mostly Norwegian wool, so it follows the wool, not the population.
    'MA.FI-RW.RW-Fibre and yarn export-TOT',
    # Norsk Tekstilgjenvinning at its 2025 capacity.
    INSTITUTIONAL_RECYCLING,
    RECYCLED_FIBRE,
]

# Processes whose outflows keep their 2025 shares of the inflow, with the
# dimensions the shares are taken on.
SPLIT_BY_2025_SHARES = {
    'CO.CO': ('t', 'g'),
    'CO.SO': ('t', 'g'),
    'CO.RE': ('t', 'g'),
    'WM.RS': ('t',),
}


class Reference:
    """
    The closed historical system (iteration 0), the population growth
    relative to 2025 and the parameters of iteration 0, shared by the
    flow functions. The cohort models are run once and kept here.
    """

    def __init__(self, hist, population, current_params):
        """population: {year: mean population} for 2025 and FUTURE_YEARS."""
        self.hist = hist
        self.current_params = current_params
        self.growth = np.array([population[year] / population[BASE_YEAR] for year in FUTURE_YEARS])

    def base(self, code):
        return self.hist.flows[code].values[BASE]

    def per_capita(self, code):
        base = self.base(code)
        return self.growth.reshape((-1,) + (1,) * base.ndim) * base

    def held(self, code):
        return np.repeat(self.base(code)[None], len(FUTURE_YEARS), axis=0)


def future_composition_data(preloaded_data):
    """
    Trade by fibre class for the fibre layer of the future years
    (compute_fibre_layer): the 2025 mass per fibre class of each product
    in every future year, so that goods supplied keep the 2025
    composition. The composition of discards still changes, because it
    comes from the cohort models, which carry the older cohorts on.
    """
    # 'imports_by_fibre_class' and 'intermediate_by_fibre_class' <-
    # data_files/Tab_08801_textiles.csv (SSB 08801) and
    # parameters/hs_main_fibre.csv, summed when the data is loaded
    def held(kg):
        return np.repeat(kg[BASE][None], len(FUTURE_YEARS), axis=0)
    return {
        'imports_by_fibre_class': held(preloaded_data['imports_by_fibre_class']),
        'intermediate_by_fibre_class': {key: held(kg) for key, kg in
                                        preloaded_data['intermediate_by_fibre_class'].items()},
    }


def execute_reference(fut, ref):
    _per_capita_flows(fut, ref)
    _held_flows(fut, ref)
    _online_returns(fut, ref)
    _finished_products_import(fut)
    _household_discards(fut, ref)
    _worn_residual_waste(fut, ref)
    _institutional_waste(fut, ref)
    _industrial_laundry_release(fut, ref)
    for process in ('CO.CO', 'CO.SO', 'CO.RE'):
        _split_by_2025_shares(fut, ref, process)
    _export_for_recycling(fut)
    _split_by_2025_shares(fut, ref, 'WM.RS')
    _fabric_import(fut)
    _fibre_and_yarn_import(fut)


def _per_capita_flows(fut, ref):
    """
    The 2025 value per inhabitant times the population (SSB 14740, main
    alternative MMM), for every flow in PER_CAPITA_FLOWS. Consumption per
    inhabitant is flat in the reference path; the span -3 to +2 % per year
    is an uncertain factor in step 2.
    """
    for code in PER_CAPITA_FLOWS:
        fut.flows[code].values[...] = ref.per_capita(code)


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


def household_cohorts(hist, fut, current_params):
    """
    Cohort model of the CORE group in US.HH over the historical and the
    future years: new goods entering the households from 1988 (iteration 0)
    and from 2026 (this module), with the spin-up from 1950 and the
    lifetimes of the historical model. Returns the use_cohorts result over
    YEARS + FUTURE_YEARS, summed over the products, as arrays (year,).
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    inflow = np.concatenate([new_goods_to_households(hist.flows), new_goods_to_households(fut.flows)])[:, core]
    cohorts = use_cohorts(inflow[:, :, None], CORE_GROUP_PRODUCTS, current_params)
    return {'outflow': cohorts['outflow'][:, :, 0].sum(axis=1), 'stock': cohorts['stock'][:, :, 0].sum(axis=1),
            'stock_1987': cohorts['stock_1987'][:, 0].sum()}


def _household_discards(fut, ref):
    """
    CORE discards from households: the outflow of the cohort model of the
    stock in use, scaled so that it equals the statistics in 2025
    (separate collection plus reusable and worn textiles in residual
    waste). The scale factor s (about 0.87) is held: the gap between the
    cohort model and the statistics in 2018-2025 (10-27 kt per year, D40)
    is carried on as growth of the stock that is the residual of the
    balance, as in the history (D8). Where the gap goes is an uncertain
    factor in step 2.

    The discards are split between separate collection, reusable and worn
    textiles in residual waste by their 2025 shares (collection rate about
    45 %); collection targets under EPR are a measure in step 3.
    """
    cohorts = household_cohorts(ref.hist, fut, ref.current_params)
    shares = {code: ref.base(code)[CORE] for code in (COLLECTION, REUSABLE, WORN)}
    statistics = sum(shares.values())
    ref.scale = statistics / cohorts['outflow'][BASE]
    ref.cohorts = cohorts
    discards = ref.scale * cohorts['outflow'][len(YEARS):]
    ref.core_discards = discards
    fut.flows[COLLECTION].values[...] = core_group_only(discards * shares[COLLECTION] / statistics)
    fut.flows[REUSABLE].values[...] = core_group_only(discards * shares[REUSABLE] / statistics)


def _worn_residual_waste(fut, ref):
    """
    CORE: the share of the scaled cohort discards that is worn
    (_household_discards). CA, TA and OM: the outflow of the cohort model of
    the goods sold to households, with sales from 1988 to 2050, as in the
    history (an exception to D8). Sacks are not used by households (D13).
    """
    worn_share = ref.base(WORN)[CORE] / sum(ref.base(c)[CORE] for c in (COLLECTION, REUSABLE, WORN))
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


def _split_by_2025_shares(fut, ref, process):
    """
    Every outflow of the process is its 2025 share of the inflow, on the
    dimensions in SPLIT_BY_2025_SHARES: CO.CO (export of unsorted textiles
    and domestic sorting), CO.SO (second-hand sales, recycling, sorting
    residues), CO.RE (second-hand sales) and WM.RS (incineration in Norway
    and abroad; landfill stays 0 under the 2009 ban). The collected
    textiles are all in the CORE group, so the CO shares are taken there
    and the other groups are 0. Sorting before export (WSR, 2027) is a
    measure in step 3.
    """
    letters = SPLIT_BY_2025_SHARES[process]
    inflow = _process_inflow(fut, process, letters)
    base_inflow = _process_inflow(ref.hist, process, letters)[BASE]
    for code, flow in fut.flows.items():
        if flow.from_process.name != process:
            continue
        if letters == ('t', 'g'):
            share = ref.base(code)[CORE] / base_inflow[CORE]
            flow.values[...] = core_group_only(inflow[:, CORE] * share)
        else:
            flow.values[...] = inflow * ref.base(code) / base_inflow


def _export_for_recycling(fut):
    """
    The balance of WM.RC: what is recycled minus the recycled fibre spun in
    Norway (held at 2025). A negative value is not physical and is clipped
    at 0.
    """
    clip_negative(fut, 'WM.RC-RW.RW-Export for recycling-TOT',
                  _process_inflow(fut, 'WM.RC', ('t',)) - fut.flows[RECYCLED_FIBRE].values)


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
