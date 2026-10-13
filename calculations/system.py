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

Negative flows are not physical and are clipped at 0 (clip_negative); the
clipped mass is recorded per flow in mfa.clipped. Processes with a balance
flow that can be clipped have a clipping stock (has_stock 'clipping'): its
change is the mass created by the clipping, so flodym's mass balance holds,
and close() checks that it equals the recorded clipped mass and nothing
else.
"""
import flodym as fd
import numpy as np
import pandas as pd

from calculations.utils import GROUP_OF_PRODUCT, MATERIALS, PRODUCT_GROUPS, PRODUCTS, YEARS

PROCESSES_CSV = 'system/processes.csv'
FLOWS_CSV = 'system/flows.csv'

DIMENSIONS = fd.DimensionSet(dim_list=[
    fd.Dimension(letter='t', name='Time', dtype=int, items=YEARS),
    fd.Dimension(letter='p', name='Product', dtype=str, items=PRODUCTS),
    fd.Dimension(letter='g', name='Product group', dtype=str, items=PRODUCT_GROUPS),
    fd.Dimension(letter='m', name='Material', dtype=str, items=MATERIALS),
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


def make_system(fibre=False):
    """
    An MFASystem with every implemented flow and all stocks, values unset.
    With fibre=True every flow and stock also has the material dimension 'm'
    (the fibre layer, D19).
    """
    extra = ('m',) if fibre else ()
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
                              dim_letters=_letters(r['dims']) + extra, name_override=r['flow_code'])
            for _, r in flows.iterrows()
        ])
    with_stock = processes[processes['code'].isin(codes) & processes['stock_dims'].notna()]
    fd_stocks = fd.make_empty_stocks(
        processes=fd_processes, dims=DIMENSIONS,
        stock_definitions=[
            fd.StockDefinition(name=r['code'], process=r['code'], dim_letters=_letters(r['stock_dims']) + extra,
                               subclass=fd.SimpleFlowDrivenStock)
            for _, r in with_stock.iterrows()
        ])
    mfa = fd.MFASystem(dims=DIMENSIONS, parameters={}, processes=fd_processes, flows=fd_flows, stocks=fd_stocks)
    mfa.clipped = {}
    mfa.clipped_inflows = set()
    return mfa


def reset(mfa):
    """Sets every flow and stock to NaN, so a flow no pool assigns fails close()."""
    for flow in mfa.flows.values():
        flow.values[...] = np.nan
    for stock in mfa.stocks.values():
        for arr in (stock.stock, stock.inflow, stock.outflow):
            arr.values[...] = np.nan
    mfa.clipped = {}
    mfa.clipped_inflows = set()


def clip_negative(mfa, code, values):
    """
    Sets the flow to values clipped at 0 and records the clipped mass
    (FlodymArray like the flow, >= 0) in mfa.clipped[code]. Every flow that
    can be clipped is recorded in every iteration, also when nothing is
    clipped.
    """
    flow = mfa.flows[code]
    flow.values[...] = np.clip(values, 0.0, None)
    mfa.clipped[code] = fd.FlodymArray(dims=flow.dims, values=np.clip(-values, 0.0, None))


def to_dims(arr, letters):
    """Sums a flow to the given dimensions, mapping products to product groups where needed."""
    if 'g' in letters and 'p' in arr.dims.letters:
        arr = arr * PRODUCT_TO_GROUP
    return arr.sum_to(letters)


def close(mfa):
    """
    Checks that every flow is set and non-negative, computes the stocks from
    the flows, checks the mass balance of every process, and checks that
    every clipping stock changes by exactly the mass clipped from the flows
    leaving it. Raises ValueError on any failure.
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
    _check_clipping_stocks(mfa)


def clipping_stocks():
    processes, _ = load_register()
    return list(processes.loc[processes['has_stock'] == 'clipping', 'code'])


def _check_clipping_stocks(mfa):
    # The clipped mass may have fewer dimensions than the stock (in the fibre
    # system, clipping inherited from TOT has no material), so both sides are
    # compared on the dimensions they share. A flow in mfa.clipped_inflows
    # is larger than the flows its target process passes on (they are not
    # computed from it), so its clipped mass also stays in the target.
    tolerance = 100 * mfa._absolute_float_precision
    for code in clipping_stocks():
        if code not in mfa.stocks:
            continue
        change = stock_change(mfa, code)
        leaving = [d for c, d in mfa.clipped.items() if mfa.flows[c].from_process.name == code]
        entering = [d for c, d in mfa.clipped.items()
                    if c in mfa.clipped_inflows and mfa.flows[c].to_process.name == code]
        clipped = leaving + entering
        common = tuple(l for l in change.dims.letters if all(l in d.dims.letters for d in clipped))
        error = (change.sum_to(common).values + sum(d.sum_to(common).values for d in leaving)
                 - sum(d.sum_to(common).values for d in entering))
        if np.abs(error).max() > tolerance:
            raise ValueError(f"Clipping stock {code} changes by more than the clipped mass "
                             f"(max {np.abs(error).max():.3g} kt)")


def stock_change(mfa, code):
    stock = mfa.stocks[code]
    return stock.inflow - stock.outflow
