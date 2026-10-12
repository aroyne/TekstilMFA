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
            (D6), so they share the import composition. Flows out of DI.RT
            mix in hand knitting yarn spun in Norway (WO) for retail yarn.
  discards  Flows out of US.HH and through CO: the CORE group (CL+HT+FW and
            retail yarn) gets the composition of the outflow of an
            inflow-driven cohort model of US.HH, so it
            reflects what was bought earlier. CA, TA and OM are discarded in
            the year supplied, so they keep the supply composition.
            Reusable and worn residual textiles share one composition.
  mixed     Flows out of WM.RS get the composition of everything entering
            WM.RS that year.
  manufacturing
            MA.FI: raw wool is wool, traded fibre and yarn have the main
            fibre of their HS codes, and yarn to MA.TX is the balance per
            material (see manufacturing_layer).

The main fibre is taken as the whole textile part of a good (a garment
classified as cotton counts as 100 % cotton); a main fibre to fibre shares
matrix is not yet part of the layer.
"""
import math

import flodym as fd
import numpy as np
import pandas as pd

from calculations.system import close, reset, to_dims
from calculations.utils import (CORE_GROUP_PRODUCTS, FIBRE_GROUPS, MATERIALS, PRODUCT_GROUPS, PRODUCTS, START_YEAR,
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
RAW_WOOL = 'PS.WO-MA.FI-Norwegian raw wool-TOT'
FIBRE_YARN_IMPORT = 'RW.RW-MA.FI-Fibre and yarn import-TOT'
FIBRE_YARN_EXPORT = 'MA.FI-RW.RW-Fibre and yarn export-TOT'
SCOURING_LOSS = 'MA.FI-WM.WW-Wool scouring loss-TOT'
YARN_TO_MANUFACTURING = 'MA.FI-MA.TX-Yarn to textile manufacturing-TOT'
HAND_KNITTING_YARN = 'MA.FI-DI.RT-Domestic hand knitting yarn-TOT'
MANUFACTURING_FLOWS = [RAW_WOOL, FIBRE_YARN_IMPORT, FIBRE_YARN_EXPORT, SCOURING_LOSS, HAND_KNITTING_YARN,
                       YARN_TO_MANUFACTURING]
FINISHED_IMPORT = 'RW.RW-DI.RT-Finished textile products import-TOT'
TOLERANCE_KT = 1e-9


def aggregate_by_fibre_class(trade, hs_main_fibre, impeks, category, products):
    """
    Net weight (kg) of in-scope trade in one direction (1 import, 2 export)
    and category, array (year, product, fibre class). Summed once before the
    MC loop; the 08801 noise factor cancels out in the shares.
    """
    sel = trade[(trade['impeks'] == impeks) & (trade['category'] == category) & (trade['in_scope'] == 'yes')
                & trade['product'].isin(products)]
    fibre_class = sel['HS_code'].str.strip().map(hs_main_fibre.set_index('HS_code')['main_fibre'])
    if fibre_class.isna().any():
        missing = sel.loc[fibre_class.isna(), 'HS_code'].unique()[:10]
        raise KeyError(f"HS codes missing from parameters/hs_main_fibre.csv: {list(missing)}")
    kg = sel.groupby([sel['year'], sel['product'], fibre_class])['amount'].sum()
    # A fibre class that a product does not trade in a year is 0 kg.
    index = pd.MultiIndex.from_product([YEARS, products, FIBRE_CLASSES])
    return kg.reindex(index, fill_value=0.0).to_numpy().reshape(len(YEARS), len(products), len(FIBRE_CLASSES))


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


def _class_to_group(fibre_composition, product, synthetic):
    """Matrix (fibre class, fibre group) for one product."""
    to_group = np.zeros((len(FIBRE_CLASSES), len(FIBRE_GROUPS)))
    for c, fibre_class in enumerate(FIBRE_CLASSES):
        if fibre_class in DIRECT_CLASSES:
            to_group[c, FIBRE_GROUPS.index(DIRECT_CLASSES[fibre_class])] = 1.0
        elif fibre_class == 'MMF':
            to_group[c, FIBRE_GROUPS.index('SYN')] = synthetic
            to_group[c, FIBRE_GROUPS.index('CV')] = 1.0 - synthetic
        else:  # RES, UNK: no fibre stated
            to_group[c, :] = _fallback_composition(fibre_composition, product)
    return to_group


def _fibre_group_shares(kg, products, current_params, fibre_composition):
    """Fibre group shares, array (year, product, fibre group), from kg per fibre class."""
    class_shares = kg / kg.sum(axis=2, keepdims=True)
    synthetic = current_params['mmf_synthetic_share']
    to_group = np.stack([_class_to_group(fibre_composition, p, synthetic) for p in products])
    return np.einsum('tpc,pcg->tpg', class_shares, to_group)


def supply_composition(preloaded_data, current_params, fibre_composition):
    """Material shares of goods supplied, array (year, product, material)."""
    # 'imports_by_fibre_class' <- data_files/Tab_08801_textiles.csv (SSB 08801,
    # HS 50-64) and parameters/hs_main_fibre.csv, summed when the data is loaded
    textile = _fibre_group_shares(preloaded_data['imports_by_fibre_class'], PRODUCTS, current_params,
                                  fibre_composition)
    nontextile = np.array([current_params[f'nontextile_share_{p}'] for p in PRODUCTS])
    return np.concatenate([textile * (1.0 - nontextile)[None, :, None],
                           np.broadcast_to(nontextile[None, :, None], textile.shape[:2] + (1,))], axis=2)


def fibre_yarn_composition(preloaded_data, current_params, fibre_composition, impeks):
    """
    Material shares of traded fibre and yarn (1 import, 2 export), array
    (year, material): the main fibre stated by the HS code, no non-textile
    part.
    """
    # 'fibre_yarn_by_fibre_class' <- data_files/Tab_08801_textiles.csv (SSB
    # 08801, HS 50-55 fibre and yarn) and parameters/hs_main_fibre.csv, summed
    # when the data is loaded
    kg = preloaded_data['fibre_yarn_by_fibre_class'][impeks]
    textile = _fibre_group_shares(kg, ['FY'], current_params, fibre_composition)[:, 0, :]
    return np.concatenate([textile, np.zeros((len(YEARS), 1))], axis=1)


def manufacturing_layer(fibre, tot, preloaded_data, current_params, fibre_composition):
    """
    Fills the MA.FI flows of the fibre system. Norwegian raw wool is WO;
    greasy wool is counted as WO including its grease, so the scouring loss
    is WO too. Traded fibre and yarn have the main fibre of their HS codes.
    Hand knitting yarn to DI.RT is WO: the Prodcom code it comes from is wool
    yarn. Yarn to textile manufacturing is the balance of MA.FI per
    material, clipped at 0: a material whose exports, losses and hand
    knitting yarn exceed its supply (wool in 1989 and 2000 in some draws)
    gets 0, the other materials are scaled down so that the flow keeps its
    TOT mass, and the export composition takes up the difference, so that
    every material still balances.
    """
    fibre.flows[HAND_KNITTING_YARN].values[...] = tot.flows[HAND_KNITTING_YARN].values[..., None] * _only('WO')
    fibre.flows[RAW_WOOL].values[...] = tot.flows[RAW_WOOL].values[:, None] * _only('WO')
    fibre.flows[SCOURING_LOSS].values[...] = tot.flows[SCOURING_LOSS].values[:, None] * _only('WO')
    for code, impeks in ((FIBRE_YARN_IMPORT, 1), (FIBRE_YARN_EXPORT, 2)):
        shares = fibre_yarn_composition(preloaded_data, current_params, fibre_composition, impeks)
        fibre.flows[code].values[...] = tot.flows[code].values[:, None] * shares
    supply = sum(fibre.flows[c].values for c in (RAW_WOOL, FIBRE_YARN_IMPORT))
    removed = fibre.flows[SCOURING_LOSS].values + fibre.flows[HAND_KNITTING_YARN].values.sum(axis=1)
    balance = supply - removed - fibre.flows[FIBRE_YARN_EXPORT].values
    clipped = np.clip(balance, 0.0, None)
    total = tot.flows[YARN_TO_MANUFACTURING].values[:, None]
    yarn = clipped * total / clipped.sum(axis=1, keepdims=True)
    fibre.flows[YARN_TO_MANUFACTURING].values[...] = yarn
    fibre.flows[FIBRE_YARN_EXPORT].values[...] = supply - removed - yarn
    if (fibre.flows[FIBRE_YARN_EXPORT].values < -TOLERANCE_KT).any():
        t, m = np.argwhere(fibre.flows[FIBRE_YARN_EXPORT].values < -TOLERANCE_KT)[0]
        raise ValueError(f"MA.FI cannot export more {MATERIALS[m]} than it has in {YEARS[t]}")


def retail_composition(tot, imported):
    """
    Material shares of goods leaving DI.RT, array (year, product, material):
    the mix of registered imports and hand knitting yarn spun in Norway
    (WO), so that DI.RT balances per material. Equal to the import
    composition for every product except retail yarn (YA).
    """
    imports = tot.flows[FINISHED_IMPORT].values
    domestic = tot.flows[HAND_KNITTING_YARN].values
    mixed = imports[..., None] * imported + domestic[..., None] * _only('WO')
    return mixed / (imports + domestic)[..., None]


def _only(material):
    shares = np.zeros(len(MATERIALS))
    shares[MATERIALS.index(material)] = 1.0
    return shares


COHORT_DIMS = fd.DimensionSet(dim_list=[
    fd.Dimension(letter='t', name='Time', dtype=int, items=YEARS),
    fd.Dimension(letter='p', name='Product', dtype=str, items=CORE_GROUP_PRODUCTS),
    fd.Dimension(letter='m', name='Material', dtype=str, items=MATERIALS),
])
# The parallel stock model (D8), reported next to the statistics; named like
# flows from US.HH to itself, as the residual stock change is.
STOCK_MODEL_OUTPUTS = {
    'discards': 'US.HH-US.HH-Stock model discards-TOT',
    'stock': 'US.HH-US.HH-Stock model stock-TOT',
    'stock_change': 'US.HH-US.HH-Stock model stock change-TOT',
}
# Stock level of the statistics-based balance: the residual stock changes
# accumulated from the stock model's stock at the end of 1987 (D2).
RESIDUAL_STOCK_OUTPUT = 'US.HH-US.HH-Stock-TOT'
CORE_STOCK_DIMS = fd.DimensionSet(dim_list=[
    fd.Dimension(letter='t', name='Time', dtype=int, items=YEARS),
    fd.Dimension(letter='g', name='Product group', dtype=str, items=['CORE']),
    fd.Dimension(letter='m', name='Material', dtype=str, items=MATERIALS),
])


def household_cohort_model(tot, supply, current_params):
    """
    Inflow-driven cohort model of the CORE group (CL+HT+FW and retail yarn)
    in US.HH (D8, D20): new goods entering US.HH by material, Weibull
    lifetimes per product. Second-hand
    purchases (1-2 % of the inflow) are left out. Returns
    {'discards', 'stock', 'stock_change'} as FlodymArrays (year, product,
    material) over the model years, and 'stock_1987' as an array (product,
    material); the stock includes the spin-up cohorts.
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    new_goods = sum(tot.flows[code].values for code in NEW_GOODS_TO_HOUSEHOLDS)[:, core]
    inflow = new_goods[:, :, None] * supply[:, core, :]
    n_spinup = START_YEAR - SPINUP_START
    inflow = np.concatenate([np.repeat(inflow[:1], n_spinup, axis=0), inflow], axis=0)

    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=DSM_YEARS),
        fd.Dimension(letter='p', name='Product', dtype=str, items=CORE_GROUP_PRODUCTS),
        fd.Dimension(letter='m', name='Material', dtype=str, items=MATERIALS),
    ])
    shape = np.array([current_params[f'lifetime_shape_US.HH_{p}'] for p in CORE_GROUP_PRODUCTS])
    mean = np.array([current_params[f'lifetime_mean_US.HH_{p}'] for p in CORE_GROUP_PRODUCTS])
    scale = mean / np.array([math.gamma(1.0 + 1.0 / k) for k in shape])
    lifetime = fd.WeibullLifetime(
        dims=dims,
        weibull_shape=fd.Parameter(dims=dims[('p',)], values=shape),
        weibull_scale=fd.Parameter(dims=dims[('p',)], values=scale),
    )
    dsm = fd.InflowDrivenDSM(name='US.HH cohorts', dims=dims, lifetime_model=lifetime,
                             inflow=fd.StockArray(dims=dims, values=inflow))
    dsm.compute()
    stock = dsm.stock.values
    return {
        'discards': fd.FlodymArray(dims=COHORT_DIMS, values=dsm.outflow.values[n_spinup:]),
        'stock': fd.FlodymArray(dims=COHORT_DIMS, values=stock[n_spinup:]),
        'stock_change': fd.FlodymArray(dims=COHORT_DIMS, values=np.diff(stock, axis=0)[n_spinup - 1:]),
        'stock_1987': stock[n_spinup - 1],
    }


def household_discard_composition(cohorts, supply):
    """
    Material shares of household discards, array (year, product group,
    material). CORE: outflow of the cohort model. Other groups: discarded in
    the year supplied.
    """
    outflow = cohorts['discards'].values.sum(axis=1)
    composition = np.empty((len(YEARS), len(PRODUCT_GROUPS), len(MATERIALS)))
    for g, group in enumerate(PRODUCT_GROUPS):
        if group == 'CORE':
            composition[:, g, :] = outflow / outflow.sum(axis=1, keepdims=True)
        else:
            composition[:, g, :] = supply[:, PRODUCTS.index(group), :]
    return composition


def compute_fibre_layer(fibre, tot, preloaded_data, current_params, fibre_composition):
    """
    Fills the fibre system from the closed TOT system and closes it. Returns
    {output name: FlodymArray with material dimension} for the parallel stock
    model and for the stock level of the statistics-based balance.
    """
    unassigned = set(tot.flows) - set(SUPPLY_FLOWS + DISCARD_FLOWS + MIXED_FLOWS + MANUFACTURING_FLOWS)
    if unassigned:
        raise KeyError(f"Flows without a fibre layer rule: {sorted(unassigned)}")

    reset(fibre)
    imported = supply_composition(preloaded_data, current_params, fibre_composition)
    supply = retail_composition(tot, imported)
    for code in SUPPLY_FLOWS:
        shares = imported if code == FINISHED_IMPORT else supply
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * shares
    manufacturing_layer(fibre, tot, preloaded_data, current_params, fibre_composition)
    cohorts = household_cohort_model(tot, supply, current_params)
    discards = household_discard_composition(cohorts, supply)
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
    stock = fibre.stocks['US.HH']
    change = (stock.inflow - stock.outflow).values[:, PRODUCT_GROUPS.index('CORE'), :]
    level = cohorts['stock_1987'].sum(axis=0) + np.cumsum(change, axis=0)
    result = {STOCK_MODEL_OUTPUTS[key]: cohorts[key] for key in STOCK_MODEL_OUTPUTS}
    result[RESIDUAL_STOCK_OUTPUT] = fd.FlodymArray(dims=CORE_STOCK_DIMS, values=level[:, None, :])
    return result
