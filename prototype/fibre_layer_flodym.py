#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prototype of the fibre layer (proposal D19) built with flodym, for the
household system of the core products (CL, HT, FW). It does not change the
model: it runs the deterministic baseline (iteration 0) of the pools, takes
the TOT flows as given, and distributes them over main fibres.

  * Supply (imports, sales, private and online imports) gets the main-fibre
    composition of registered finished imports per product and year
    (SSB 08801 via parameters/hs_main_fibre.csv).
  * Discards keep their TOT mass from the statistics (D8). Their fibre
    composition comes from a parallel inflow-driven cohort model of US.HH,
    so it reflects what was bought in earlier years, not this year's supply.
  * Everything downstream of US.HH inherits the composition of discards.
  * The US.HH stock change is the residual per fibre, and flodym checks the
    mass balance of every process on the dimensions its flows share.

Lifetimes in parameters/lifetimes.csv are not set yet, so the cohort model
runs over the explicit scenarios in LIFETIME_SCENARIOS. They bracket the
range in the literature note (about 4 years with the first user, longer with
informal reuse, D9) and are not parameter values.

Simplifications that belong to the prototype only:
  * Exports and sales to institutions leave DI.RT as one flow with the
    composition of imports.
  * Collection and residual waste get the same composition.
  * Second-hand purchases are left out of the cohort model's inflow (about
    1-2 kt/yr against 80-100 kt/yr of new goods).
  * All treatment of residual waste is one flow from WM.RS to sysenv.

Usage (from the repository root):
    python -m prototype.fibre_layer_flodym
"""
import math

import flodym as fd
import numpy as np
import pandas as pd

from calculations.params import Parameters
from calculations.system import close, make_system
from calculations.utils import CORE_PRODUCTS, END_YEAR, PRODUCT_GROUPS, PRODUCTS, START_YEAR
from data_loader import load_all_data
from main_mc import ALL_POOLS, run_pools

HS_MAIN_FIBRE = 'parameters/hs_main_fibre.csv'
OUTPUT = 'output_files/prototype_fibre_shares.csv'

# Inflow before 1988 is held at the 1988 level and composition (D2).
SPINUP_START = 1950
YEARS = list(range(START_YEAR, END_YEAR + 1))
DSM_YEARS = list(range(SPINUP_START, END_YEAR + 1))

# Main fibre classes from the HS texts (see scripts/build_hs_main_fibre.py).
FIBRES = ['CO', 'WO', 'SYN', 'ART', 'MMF', 'OTH', 'RES', 'UNK']
MAN_MADE = ['SYN', 'ART', 'MMF']

# Mean lifetime in US.HH (years), Weibull with WEIBULL_SHAPE.
LIFETIME_SCENARIOS = {
    'short': {'CL': 3.0, 'HT': 5.0, 'FW': 2.0},
    'medium': {'CL': 5.0, 'HT': 8.0, 'FW': 3.0},
    'long': {'CL': 8.0, 'HT': 12.0, 'FW': 5.0},
}
WEIBULL_SHAPE = 2.0

F_IMPORT = 'RW.RW-DI.RT-Finished textile products import'
F_DI_OUT = 'DI.RT-RW.RW-Export and sales to institutions'
F_SALES = 'DI.RT-US.HH-Sales to households'
F_PRIVATE = 'RW.RW-US.HH-Private imports'
F_ONLINE = 'RW.RW-US.HH-Direct online imports'
F_SECONDHAND = 'CO.RE-US.HH-Secondhand sales to households'
F_COLLECT = 'US.HH-CO.CO-Separate collection from households'
F_RESIDUAL = 'US.HH-WM.RS-Textiles in residual and bulky waste'
F_EXPORT_UNSORTED = 'CO.CO-RW.RW-Export of unsorted collected textiles'
F_TO_SORTING = 'CO.CO-CO.SO-Collected textiles to domestic sorting'
F_REUSE = 'CO.SO-CO.RE-Sorted for domestic secondhand sales'
F_SORT_RESIDUES = 'CO.SO-WM.RS-Sorting residues'
F_TREATMENT = 'WM.RS-RW.RW-Treatment of residual waste'

# (name, from, to, dims). sysenv stands for RW.RW and for every process
# the prototype does not model.
FLOWS = [
    (F_IMPORT, 'sysenv', 'DI.RT', ('t', 'p', 'm')),
    (F_DI_OUT, 'DI.RT', 'sysenv', ('t', 'p', 'm')),
    (F_SALES, 'DI.RT', 'US.HH', ('t', 'p', 'm')),
    (F_PRIVATE, 'sysenv', 'US.HH', ('t', 'p', 'm')),
    (F_ONLINE, 'sysenv', 'US.HH', ('t', 'p', 'm')),
    (F_SECONDHAND, 'CO.RE', 'US.HH', ('t', 'm')),
    (F_COLLECT, 'US.HH', 'CO.CO', ('t', 'm')),
    (F_RESIDUAL, 'US.HH', 'WM.RS', ('t', 'm')),
    (F_EXPORT_UNSORTED, 'CO.CO', 'sysenv', ('t', 'm')),
    (F_TO_SORTING, 'CO.CO', 'CO.SO', ('t', 'm')),
    (F_REUSE, 'CO.SO', 'CO.RE', ('t', 'm')),
    (F_SORT_RESIDUES, 'CO.SO', 'WM.RS', ('t', 'm')),
    (F_TREATMENT, 'WM.RS', 'sysenv', ('t', 'm')),
]
PROCESSES = ['sysenv', 'DI.RT', 'US.HH', 'CO.CO', 'CO.SO', 'CO.RE', 'WM.RS']


def run_tot_baseline():
    """Deterministic iteration 0 of all pools, as in main_mc.py."""
    params = Parameters()
    preloaded_data = load_all_data(ALL_POOLS, params)
    current_params, dataset_noise, anchors = params.draw(np.random.default_rng(0), deterministic=True)
    tot = make_system()
    run_pools(tot, ALL_POOLS, preloaded_data, current_params, dataset_noise, anchors)
    close(tot)
    return tot, preloaded_data


def import_fibre_shares(preloaded_data):
    """Main-fibre shares of registered finished imports, array (t, p, m)."""
    # 'trade_textiles' <- data_files/Tab_08801_textiles.csv (SSB 08801, HS 50-64)
    trade = preloaded_data['trade_textiles']
    mapping = pd.read_csv(HS_MAIN_FIBRE, dtype=str)
    sel = trade[(trade['impeks'] == 1) & (trade['category'] == 'finished')
                & trade['product'].isin(CORE_PRODUCTS) & trade['year'].isin(YEARS)].copy()
    sel['HS_code'] = sel['HS_code'].str.strip()
    sel = sel.merge(mapping[['HS_code', 'main_fibre']], on='HS_code', how='left', validate='many_to_one')
    unmatched = sel.loc[sel['main_fibre'].isna(), 'HS_code'].unique()
    if len(unmatched):
        raise KeyError(f"HS codes missing from {HS_MAIN_FIBRE}: {list(unmatched)[:10]}")

    kg = (sel.groupby(['year', 'product', 'main_fibre'])['amount'].sum()
          .reindex(pd.MultiIndex.from_product([YEARS, CORE_PRODUCTS, FIBRES]), fill_value=0.0))
    arr = kg.to_numpy().reshape(len(YEARS), len(CORE_PRODUCTS), len(FIBRES))
    return arr / arr.sum(axis=2, keepdims=True)


def tot_by_product(tot, code):
    """TOT flow of the core products, array (t, p)."""
    return tot.flows[code].values[:, [PRODUCTS.index(p) for p in CORE_PRODUCTS]]


def tot_core(tot, code):
    """TOT flow of the CORE product group, array (t,)."""
    return tot.flows[code].values[:, PRODUCT_GROUPS.index('CORE')]


def discard_fibre_shares(new_goods, lifetimes):
    """
    Fibre shares of the outflow of an inflow-driven cohort model of US.HH,
    array (t, m) over the model years. new_goods is (t, p, m) over YEARS.
    """
    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=DSM_YEARS),
        fd.Dimension(letter='p', name='Product', dtype=str, items=CORE_PRODUCTS),
        fd.Dimension(letter='m', name='Fibre', dtype=str, items=FIBRES),
    ])
    n_spinup = START_YEAR - SPINUP_START
    inflow = np.concatenate([np.repeat(new_goods[:1], n_spinup, axis=0), new_goods], axis=0)

    mean = np.array([lifetimes[p] for p in CORE_PRODUCTS])
    scale = mean / math.gamma(1.0 + 1.0 / WEIBULL_SHAPE)
    lifetime_model = fd.WeibullLifetime(
        dims=dims,
        weibull_shape=fd.Parameter(dims=dims[('p',)], values=np.full(len(CORE_PRODUCTS), WEIBULL_SHAPE)),
        weibull_scale=fd.Parameter(dims=dims[('p',)], values=scale),
    )
    dsm = fd.InflowDrivenDSM(
        name='US.HH cohorts', dims=dims, lifetime_model=lifetime_model,
        inflow=fd.StockArray(dims=dims, values=inflow),
    )
    dsm.compute()
    outflow = dsm.outflow.values.sum(axis=1)[n_spinup:]
    return outflow / outflow.sum(axis=1, keepdims=True)


def build_system(tot, supply_shares, discard_shares):
    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=YEARS),
        fd.Dimension(letter='p', name='Product', dtype=str, items=CORE_PRODUCTS),
        fd.Dimension(letter='m', name='Fibre', dtype=str, items=FIBRES),
    ])
    processes = fd.make_processes(PROCESSES)
    flows = fd.make_empty_flows(
        processes=processes, dims=dims,
        flow_definitions=[fd.FlowDefinition(from_process_name=src, to_process_name=dst,
                                            dim_letters=d, name_override=name)
                          for name, src, dst, d in FLOWS])
    stocks = fd.make_empty_stocks(
        processes=processes, dims=dims,
        stock_definitions=[fd.StockDefinition(name='US.HH', process='US.HH', dim_letters=('t', 'm'),
                                              subclass=fd.SimpleFlowDrivenStock)])
    mfa = fd.MFASystem(dims=dims, parameters={}, processes=processes, flows=flows, stocks=stocks)

    def by_supply(tp):
        return tp[:, :, None] * supply_shares

    def by_discards(t):
        return t[:, None] * discard_shares

    imports = tot_by_product(tot, 'RW.RW-DI.RT-Finished textile products import-TOT')
    sales = tot_by_product(tot, 'DI.RT-US.HH-Sales to households-TOT')
    mfa.flows[F_IMPORT].values[...] = by_supply(imports)
    mfa.flows[F_SALES].values[...] = by_supply(sales)
    mfa.flows[F_DI_OUT].values[...] = by_supply(imports - sales)
    mfa.flows[F_PRIVATE].values[...] = by_supply(
        tot_by_product(tot, 'RW.RW-US.HH-Private imports-TOT'))
    mfa.flows[F_ONLINE].values[...] = by_supply(
        tot_by_product(tot, 'RW.RW-US.HH-Direct online imports-TOT'))

    for name in (F_SECONDHAND, F_COLLECT, F_EXPORT_UNSORTED, F_TO_SORTING, F_REUSE, F_SORT_RESIDUES):
        mfa.flows[name].values[...] = by_discards(tot_core(tot, name + '-TOT'))
    mfa.flows[F_RESIDUAL].values[...] = by_discards(tot_core(tot, F_RESIDUAL + '-TOT'))
    mfa.flows[F_TREATMENT].values[...] = (mfa.flows[F_RESIDUAL].values
                                          + mfa.flows[F_SORT_RESIDUES].values)

    stock = mfa.stocks['US.HH']
    stock.inflow[...] = (mfa.flows[F_SALES] + mfa.flows[F_PRIVATE] + mfa.flows[F_ONLINE]
                         + mfa.flows[F_SECONDHAND])
    stock.outflow[...] = mfa.flows[F_COLLECT] + mfa.flows[F_RESIDUAL]
    stock.compute()

    mfa.check_mass_balance()
    return mfa


def summarise(mfa, scenario):
    supply = (mfa.flows[F_SALES] + mfa.flows[F_PRIVATE] + mfa.flows[F_ONLINE]).sum_values_to(('t', 'm'))
    discards = (mfa.flows[F_COLLECT] + mfa.flows[F_RESIDUAL]).values
    stock_change = supply + mfa.flows[F_SECONDHAND].values - discards
    rows = []
    for i, year in enumerate(YEARS):
        for j, fibre in enumerate(FIBRES):
            rows.append({'scenario': scenario, 'year': year, 'fibre': fibre,
                         'supply_kt': supply[i, j], 'discards_kt': discards[i, j],
                         'stock_change_kt': stock_change[i, j]})
    return rows


def main():
    tot, preloaded_data = run_tot_baseline()
    supply_shares = import_fibre_shares(preloaded_data)

    new_goods = np.zeros((len(YEARS), len(CORE_PRODUCTS), len(FIBRES)))
    for code in ('DI.RT-US.HH-Sales to households-TOT', 'RW.RW-US.HH-Private imports-TOT',
                 'RW.RW-US.HH-Direct online imports-TOT'):
        new_goods += tot_by_product(tot, code)[:, :, None] * supply_shares

    rows = []
    for scenario, lifetimes in LIFETIME_SCENARIOS.items():
        mfa = build_system(tot, supply_shares, discard_fibre_shares(new_goods, lifetimes))
        rows.extend(summarise(mfa, scenario))
    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT, index=False)
    print(f"[INFO] Wrote {OUTPUT}")

    for year in (1990, 2005, 2021, 2025):
        sub = df[df['year'] == year]
        for scenario in LIFETIME_SCENARIOS:
            s = sub[sub['scenario'] == scenario].set_index('fibre')
            sup = s['supply_kt'] / s['supply_kt'].sum() * 100
            dis = s['discards_kt'] / s['discards_kt'].sum() * 100
            print(f"{year} {scenario:6s}  supply: CO {sup['CO']:4.1f}  man-made {sup[MAN_MADE].sum():4.1f}  "
                  f"WO {sup['WO']:3.1f}  RES+UNK {sup[['RES', 'UNK']].sum():4.1f}   |  "
                  f"discards: CO {dis['CO']:4.1f}  man-made {dis[MAN_MADE].sum():4.1f}  "
                  f"WO {dis['WO']:3.1f}  RES+UNK {dis[['RES', 'UNK']].sum():4.1f}")


if __name__ == '__main__':
    main()
