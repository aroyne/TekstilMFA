#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fibre layer (D19). After the TOT system is closed, every TOT flow is
distributed over the materials 'm' (fibre groups SYN, CO, WO, CV, OTH and
non-textile material NT) in a second flodym system with the same processes
and flows. The TOT masses are never changed: they come from the statistics
(D8), and the layer only says what they are made of.

  supply    Imports, sales, private and online imports, exports and
            institutional waste get the composition of registered imports of
            the product in that year: the main fibre stated by the HS code
            (parameters/hs_main_fibre.csv), with codes that state none
            distributed by parameters/fibre_composition.csv, scaled to the
            textile part (1 - nontextile_share). Exports are mostly re-export
            (D6), so they share the import composition.
  discards  Flows out of US.HH and through CO: CL+HT+FW get the composition
            of the outflow of an inflow-driven cohort model of US.HH, so it
            reflects what was bought earlier. CA, TA and OM are discarded in
            the year supplied, so they keep the supply composition.
            Reusable and worn residual textiles share one composition.
  mixed     Flows out of WM.RS get the composition of everything entering
            WM.RS that year.

The main fibre is taken as the whole textile part of a good (a garment
classified as cotton counts as 100 % cotton); a main fibre to fibre shares
matrix is not yet part of the layer.
"""
import math

import flodym as fd
import numpy as np
import pandas as pd

from calculations.system import close, reset, to_dims
from calculations.utils import (CORE_PRODUCTS, FIBRE_GROUPS, MATERIALS, PRODUCT_GROUPS, PRODUCTS, START_YEAR,
                                YEARS)

# Main fibre classes in parameters/hs_main_fibre.csv.
FIBRE_CLASSES = ['CO', 'WO', 'SYN', 'ART', 'MMF', 'OTH', 'RES', 'UNK']
DIRECT_CLASSES = {'CO': 'CO', 'WO': 'WO', 'SYN': 'SYN', 'ART': 'CV', 'OTH': 'OTH'}

# Inflow before 1988 is held at the 1988 level and composition (D2).
SPINUP_START = 1950
DSM_YEARS = list(range(SPINUP_START, YEARS[-1] + 1))

NEW_GOODS_TO_HOUSEHOLDS = [
    'DI.RT-US.HH-Sales to households-TOT',
    'RW.RW-US.HH-Private imports-TOT',
    'RW.RW-US.HH-Direct online imports-TOT',
]
SUPPLY_FLOWS = [
    'RW.RW-DI.RT-Finished textile products import-TOT',
    'DI.RT-RW.RW-Export of finished textile products-TOT',
    'DI.RT-US.IC-Sales to institutions and businesses-TOT',
    'US.IC-WM.RS-Institutional textile waste-TOT',
] + NEW_GOODS_TO_HOUSEHOLDS
DISCARD_FLOWS = [
    'US.HH-CO.CO-Separate collection from households-TOT',
    'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
    'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT',
    'CO.CO-RW.RW-Export of unsorted collected textiles-TOT',
    'CO.CO-CO.SO-Collected textiles to domestic sorting-TOT',
    'CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT',
    'CO.SO-WM.RS-Sorting residues-TOT',
    'CO.RE-US.HH-Secondhand sales to households-TOT',
]
MIXED_FLOWS = [
    'WM.RS-WM.IN-Domestic incineration-TOT',
    'WM.RS-RW.RW-Residual waste export for incineration-TOT',
    'WM.RS-WM.LF-Landfilling of textiles-TOT',
]
MIXED_SOURCE = 'WM.RS'
TOLERANCE_KT = 1e-9


def aggregate_imports_by_fibre_class(trade, hs_main_fibre):
    """
    Net weight (kg) of in-scope finished imports, array (year, product,
    fibre class). Summed once before the MC loop; the 08801 noise factor
    cancels out in the shares.
    """
    sel = trade[(trade['impeks'] == 1) & (trade['category'] == 'finished') & (trade['in_scope'] == 'yes')]
    fibre_class = sel['HS_code'].str.strip().map(hs_main_fibre.set_index('HS_code')['main_fibre'])
    if fibre_class.isna().any():
        missing = sel.loc[fibre_class.isna(), 'HS_code'].unique()[:10]
        raise KeyError(f"HS codes missing from parameters/hs_main_fibre.csv: {list(missing)}")
    kg = sel.groupby([sel['year'], sel['product'], fibre_class])['amount'].sum()
    # A fibre class that a product does not import in a year is 0 kg.
    index = pd.MultiIndex.from_product([YEARS, PRODUCTS, FIBRE_CLASSES])
    return kg.reindex(index, fill_value=0.0).to_numpy().reshape(len(YEARS), len(PRODUCTS), len(FIBRE_CLASSES))


def _fallback_composition(fibre_composition, product):
    """
    Row of parameters/fibre_composition.csv. The shares are rounded to four
    decimals in the file, so they are rescaled to sum to exactly 1; a larger
    deviation is an error in the table.
    """
    row = fibre_composition.loc[product, FIBRE_GROUPS].to_numpy(dtype=float)
    if abs(row.sum() - 1.0) > 1e-3:
        raise ValueError(f"fibre_composition.csv: {product} sums to {row.sum():.4f}, not 1")
    return row / row.sum()


def supply_composition(preloaded_data, current_params, fibre_composition):
    """Material shares of goods supplied, array (year, product, material)."""
    # 'imports_by_fibre_class' <- data_files/Tab_08801_textiles.csv (SSB 08801,
    # HS 50-64) and parameters/hs_main_fibre.csv, summed when the data is loaded
    kg = preloaded_data['imports_by_fibre_class']
    class_shares = kg / kg.sum(axis=2, keepdims=True)

    synthetic = current_params['mmf_synthetic_share']
    to_group = np.zeros((len(PRODUCTS), len(FIBRE_CLASSES), len(FIBRE_GROUPS)))
    for p, product in enumerate(PRODUCTS):
        for c, fibre_class in enumerate(FIBRE_CLASSES):
            if fibre_class in DIRECT_CLASSES:
                to_group[p, c, FIBRE_GROUPS.index(DIRECT_CLASSES[fibre_class])] = 1.0
            elif fibre_class == 'MMF':
                to_group[p, c, FIBRE_GROUPS.index('SYN')] = synthetic
                to_group[p, c, FIBRE_GROUPS.index('CV')] = 1.0 - synthetic
            else:  # RES, UNK: no fibre stated
                to_group[p, c, :] = _fallback_composition(fibre_composition, product)
    textile = np.einsum('tpc,pcg->tpg', class_shares, to_group)

    nontextile = np.array([current_params[f'nontextile_share_{p}'] for p in PRODUCTS])
    return np.concatenate([textile * (1.0 - nontextile)[None, :, None],
                           np.broadcast_to(nontextile[None, :, None], textile.shape[:2] + (1,))], axis=2)


def household_discard_composition(tot, supply, current_params):
    """
    Material shares of household discards, array (year, product group,
    material). CORE: outflow of an inflow-driven cohort model of the new
    goods entering US.HH (second-hand purchases, 1-2 % of the inflow, are
    left out). Other groups: discarded in the year supplied.
    """
    core = [PRODUCTS.index(p) for p in CORE_PRODUCTS]
    new_goods = sum(tot.flows[code].values for code in NEW_GOODS_TO_HOUSEHOLDS)[:, core]
    inflow = new_goods[:, :, None] * supply[:, core, :]
    n_spinup = START_YEAR - SPINUP_START
    inflow = np.concatenate([np.repeat(inflow[:1], n_spinup, axis=0), inflow], axis=0)

    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=DSM_YEARS),
        fd.Dimension(letter='p', name='Product', dtype=str, items=CORE_PRODUCTS),
        fd.Dimension(letter='m', name='Material', dtype=str, items=MATERIALS),
    ])
    shape = np.array([current_params[f'lifetime_shape_US.HH_{p}'] for p in CORE_PRODUCTS])
    mean = np.array([current_params[f'lifetime_mean_US.HH_{p}'] for p in CORE_PRODUCTS])
    scale = mean / np.array([math.gamma(1.0 + 1.0 / k) for k in shape])
    lifetime = fd.WeibullLifetime(
        dims=dims,
        weibull_shape=fd.Parameter(dims=dims[('p',)], values=shape),
        weibull_scale=fd.Parameter(dims=dims[('p',)], values=scale),
    )
    dsm = fd.InflowDrivenDSM(name='US.HH cohorts', dims=dims, lifetime_model=lifetime,
                             inflow=fd.StockArray(dims=dims, values=inflow))
    dsm.compute()
    outflow = dsm.outflow.values.sum(axis=1)[n_spinup:]

    composition = np.empty((len(YEARS), len(PRODUCT_GROUPS), len(MATERIALS)))
    for g, group in enumerate(PRODUCT_GROUPS):
        if group == 'CORE':
            composition[:, g, :] = outflow / outflow.sum(axis=1, keepdims=True)
        else:
            composition[:, g, :] = supply[:, PRODUCTS.index(group), :]
    return composition


def compute_fibre_layer(fibre, tot, preloaded_data, current_params, fibre_composition):
    """Fills the fibre system from the closed TOT system and closes it."""
    unassigned = set(tot.flows) - set(SUPPLY_FLOWS + DISCARD_FLOWS + MIXED_FLOWS)
    if unassigned:
        raise KeyError(f"Flows without a fibre layer rule: {sorted(unassigned)}")

    reset(fibre)
    supply = supply_composition(preloaded_data, current_params, fibre_composition)
    for code in SUPPLY_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * supply
    discards = household_discard_composition(tot, supply, current_params)
    for code in DISCARD_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * discards

    mix = sum(to_dims(f, ('t', 'm')).values for f in fibre.flows.values() if f.to_process.name == MIXED_SOURCE)
    mix_shares = mix / mix.sum(axis=1, keepdims=True)
    for code in MIXED_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * mix_shares

    close(fibre)
    for code, flow in tot.flows.items():
        gap = np.abs(fibre.flows[code].values.sum(axis=-1) - flow.values).max()
        if gap > TOLERANCE_KT:
            raise ValueError(f"Fibre layer of {code} does not add up to TOT (max gap {gap:.2e} kt)")
