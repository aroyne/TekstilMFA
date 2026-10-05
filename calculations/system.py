#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the flodym MFA system from the register (system/processes.csv and
system/flows.csv) and closes it after the pools have assigned every flow.

Only flows whose status starts with 'implemented' are part of the system;
their dimensions come from the 'dims' column. Boundary processes (RW.RW,
PS.WO) are flodym's 'sysenv'. Every process with 'stock_dims' gets a
flow-driven stock whose change is inflows minus outflows: for the use
processes this is the stock change as residual of the balance (D8), for
sinks the mass that leaves the material cycle.
"""
import flodym as fd
import numpy as np
import pandas as pd

from calculations.utils import GROUP_OF_PRODUCT, PRODUCT_GROUPS, PRODUCTS, YEARS

PROCESSES_CSV = 'system/processes.csv'
FLOWS_CSV = 'system/flows.csv'

DIMENSIONS = fd.DimensionSet(dim_list=[
    fd.Dimension(letter='t', name='Time', dtype=int, items=YEARS),
    fd.Dimension(letter='p', name='Product', dtype=str, items=PRODUCTS),
    fd.Dimension(letter='g', name='Product group', dtype=str, items=PRODUCT_GROUPS),
])

PRODUCT_TO_GROUP = fd.Parameter(
    dims=DIMENSIONS[('p', 'g')],
    values=np.array([[float(GROUP_OF_PRODUCT[p] == g) for g in PRODUCT_GROUPS] for p in PRODUCTS]),
)


def _letters(dims):
    return tuple(dims.split(','))


def load_register():
    processes = pd.read_csv(PROCESSES_CSV)
    flows = pd.read_csv(FLOWS_CSV)
    return processes, flows[flows['status'].str.startswith('implemented')]


def make_system():
    """An MFASystem with every implemented flow and all stocks, values unset."""
    processes, flows = load_register()
    boundary = set(processes.loc[processes['type'] == 'boundary', 'code'])
    connected = (set(flows['source']) | set(flows['target'])) - boundary
    codes = [c for c in processes['code'] if c in connected]

    def node(code):
        return 'sysenv' if code in boundary else code

    fd_processes = fd.make_processes(['sysenv'] + codes)
    fd_flows = fd.make_empty_flows(
        processes=fd_processes, dims=DIMENSIONS,
        flow_definitions=[
            fd.FlowDefinition(from_process_name=node(r['source']), to_process_name=node(r['target']),
                              dim_letters=_letters(r['dims']), name_override=r['flow_code'])
            for _, r in flows.iterrows()
        ])
    with_stock = processes[processes['code'].isin(codes) & processes['stock_dims'].notna()]
    fd_stocks = fd.make_empty_stocks(
        processes=fd_processes, dims=DIMENSIONS,
        stock_definitions=[
            fd.StockDefinition(name=r['code'], process=r['code'], dim_letters=_letters(r['stock_dims']),
                               subclass=fd.SimpleFlowDrivenStock)
            for _, r in with_stock.iterrows()
        ])
    return fd.MFASystem(dims=DIMENSIONS, parameters={}, processes=fd_processes, flows=fd_flows, stocks=fd_stocks)


def reset(mfa):
    """Sets every flow and stock to NaN, so a flow no pool assigns fails close()."""
    for flow in mfa.flows.values():
        flow.values[...] = np.nan
    for stock in mfa.stocks.values():
        for arr in (stock.stock, stock.inflow, stock.outflow):
            arr.values[...] = np.nan


def to_dims(arr, letters):
    """Sums a flow to the given dimensions, mapping products to product groups where needed."""
    if 'g' in letters and 'p' in arr.dims.letters:
        arr = arr * PRODUCT_TO_GROUP
    return arr.sum_to(letters)


def close(mfa):
    """
    Checks that every flow is set and non-negative, computes the stocks from
    the flows, and checks the mass balance of every process. Raises
    ValueError on any failure.
    """
    mfa.check_flows(raise_error=True)
    for name, stock in mfa.stocks.items():
        letters = stock.dims.letters
        stock.inflow.values[...] = 0.0
        stock.outflow.values[...] = 0.0
        for flow in mfa.flows.values():
            if flow.to_process.name == name:
                stock.inflow.values[...] += to_dims(flow, letters).values
            if flow.from_process.name == name:
                stock.outflow.values[...] += to_dims(flow, letters).values
        stock.compute()
    mfa.check_mass_balance(raise_error=True)


def stock_change(mfa, code):
    stock = mfa.stocks[code]
    return stock.inflow - stock.outflow
