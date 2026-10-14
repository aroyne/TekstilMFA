#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fibre layer (D19). After the TOT system is closed, every TOT flow is
distributed over the materials 'm' (fibre groups SYN, CO, WO, CV, OTH and
non-textile material NT) in a second flodym system with the same processes
and flows. The TOT masses are never changed: they come from the statistics
(D8), and the layer only says what they are made of.

  supply    Imports, sales, private and online imports and exports get
            the composition of registered imports of
            the product in that year: the main fibre stated by the HS code
            (parameters/hs_main_fibre.csv), with codes that state none
            distributed by parameters/fibre_composition.csv, scaled to the
            textile part (1 - nontextile_share). Codes whose weight is
            mainly non-textile (furniture cushions) are NT as a whole. Exports are mostly re-export
            (D6), so they share the import composition. Flows out of DI.RT
            mix in finished goods made in Norway (the MA.TX balance per
            material) and hand knitting yarn spun in Norway (WO).
  discards  Flows out of US.HH: the CORE group (CL+HT+FW and retail
            yarn) gets the composition of the outflow of an inflow-driven
            cohort model of US.HH, so it
            reflects what was bought earlier. CA, TA and OM get the outflow
            of a cohort model of the goods sold to households.
            Reusable and worn residual textiles share one composition.
  collected Flows through CO get the mix of what is collected from
            households and unsold clothing donated by retailers.
  release   Fibres released in laundry and to air have the fibre groups of
            the textile stock of the household cohort model, and fibres from
            industrial laundry those of the US.IC cohort model.
  institutions
            Goods discarded by institutions and businesses get the outflow
            of a cohort model of the goods sold to them.
  mixed     Flows out of WM.RS get the composition of everything entering
            WM.RS that year.
  manufacturing
            MA: raw wool is wool, traded fibre, yarn and fabric have the
            main fibre of their HS codes, yarn to MA.TX is the balance of
            MA.FI per material, and production waste has the mix of MA.TX
            inputs (see manufacturing_layer).

The main fibre is taken as the whole textile part of a good (a garment
classified as cotton counts as 100 % cotton); a main fibre to fibre shares
matrix is not yet part of the layer.
"""
import flodym as fd
import numpy as np
import pandas as pd

from calculations.cohorts import use_cohorts
from calculations.system import clip_negative, close, reset, to_dims
from calculations.utils import (CORE_GROUP_PRODUCTS, FIBRE_GROUPS, MATERIALS, PRODUCT_GROUPS, PRODUCTS, START_YEAR,
                                YEARS)

# Main fibre classes in parameters/hs_main_fibre.csv. 'NT' marks codes whose
# weight is mainly non-textile (furniture cushions: foam).
FIBRE_CLASSES = ['CO', 'WO', 'SYN', 'ART', 'MMF', 'OTH', 'RES', 'UNK', 'NT']
DIRECT_CLASSES = {'CO': 'CO', 'WO': 'WO', 'SYN': 'SYN', 'ART': 'CV', 'OTH': 'OTH'}


NEW_GOODS_TO_HOUSEHOLDS = [
    'DI.RT-US.HH-Sales to households-TOT',
    'RW.RW-US.HH-Private imports-TOT',
    'RW.RW-US.HH-Direct online imports-TOT',
]
SUPPLY_FLOWS = [
    'RW.RW-DI.RT-Finished textile products import-TOT',
    'DI.RT-RW.RW-Export of finished textile products-TOT',
    'DI.RT-US.IC-Sales to institutions and businesses-TOT',
    'DI.RT-CO.CO-Unsold goods donated-TOT',
    'DI.RT-WM.RS-Unsold goods discarded-TOT',
] + NEW_GOODS_TO_HOUSEHOLDS
DISCARD_FLOWS = [
    'US.HH-CO.CO-Separate collection from households-TOT',
    'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
    'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT',
]
COLLECTION = 'US.HH-CO.CO-Separate collection from households-TOT'
# Household goods without discard statistics, discarded by a cohort model
# (calculations/us_mc.py).
OTHER_HOUSEHOLD_GOODS = ['CA', 'TA', 'OM']
INSTITUTIONAL_WASTE = 'US.IC-WM.RS-Institutional textile waste-TOT'
INSTITUTIONAL_SALES = 'DI.RT-US.IC-Sales to institutions and businesses-TOT'
# Goods in US.IC discarded by a cohort model; sacks are discarded in the year
# supplied and retail yarn is not sold to the sector.
INSTITUTIONAL_COHORT_PRODUCTS = [p for p in PRODUCTS if p not in ('SA', 'YA')]
INSTITUTIONAL_RELEASE = 'US.IC-WM.WW-Fibre release in industrial laundry-TOT'
# Fibres released from household textiles in use, with the fibre groups of
# the textile stock of the household cohort model.
RELEASE_FLOWS = [
    'US.HH-WM.WW-Fibre release in laundry-TOT',
    'US.HH-EN.AI-Fibre release to air and dust-TOT',
]
UNSOLD_DONATED = 'DI.RT-CO.CO-Unsold goods donated-TOT'
# Flows through CO, with the mix of collected used textiles and donated
# unsold clothing; imported used textiles are assumed to have the same mix.
COLLECTED_FLOWS = [
    'RW.RW-CO.SO-Used textile import-TOT',
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
FABRIC_IMPORT = 'RW.RW-MA.TX-Fabric import-TOT'
TEXTILE_EXPORT = 'MA.TX-RW.RW-Textile export-TOT'
PRECONSUMER_WASTE = 'MA.TX-WM.RS-Preconsumer production waste-TOT'
DOMESTIC_GOODS = 'MA.TX-DI.RT-Domestic finished products-TOT'
MANUFACTURING_FLOWS = [RAW_WOOL, FIBRE_YARN_IMPORT, FIBRE_YARN_EXPORT, SCOURING_LOSS, HAND_KNITTING_YARN,
                       YARN_TO_MANUFACTURING, FABRIC_IMPORT, TEXTILE_EXPORT, PRECONSUMER_WASTE, DOMESTIC_GOODS]
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
        elif fibre_class in ('RES', 'UNK'):  # no fibre stated
            to_group[c, :] = _fallback_composition(fibre_composition, product)
        # NT: no fibre group; see _shares_with_nontextile
    return to_group


def _shares_with_nontextile(kg, products, current_params, fibre_composition, nontextile):
    """
    Material shares, array (year, product, material), from kg per fibre
    class. Codes of class NT are non-textile as a whole; the rest is split
    over fibre groups, with the share nontextile (per product) of it
    non-textile (buttons, zips, soles).
    """
    class_shares = kg / kg.sum(axis=2, keepdims=True)
    synthetic = current_params['mmf_synthetic_share']
    to_group = np.stack([_class_to_group(fibre_composition, p, synthetic) for p in products])
    fibres = np.einsum('tpc,pcg->tpg', class_shares, to_group)
    nt_class = class_shares[:, :, FIBRE_CLASSES.index('NT')]
    nt = nt_class + (1.0 - nt_class) * nontextile[None, :]
    return np.concatenate([fibres * (1.0 - nontextile)[None, :, None], nt[:, :, None]], axis=2)


def supply_composition(preloaded_data, current_params, fibre_composition):
    """Material shares of goods supplied, array (year, product, material)."""
    # 'imports_by_fibre_class' <- data_files/Tab_08801_textiles.csv (SSB 08801,
    # HS 50-64 and 9404) and parameters/hs_main_fibre.csv, summed when the
    # data is loaded
    nontextile = np.array([current_params[f'nontextile_share_{p}'] for p in PRODUCTS])
    return _shares_with_nontextile(preloaded_data['imports_by_fibre_class'], PRODUCTS, current_params,
                                   fibre_composition, nontextile)


def intermediate_composition(preloaded_data, current_params, fibre_composition, product, impeks):
    """
    Material shares of traded fibre and yarn ('FY') or fabric ('FA'), import
    (1) or export (2), array (year, material): the main fibre stated by the
    HS code, no non-textile part.
    """
    # 'intermediate_by_fibre_class' <- data_files/Tab_08801_textiles.csv (SSB
    # 08801, HS 50-60 fibre, yarn and fabric) and parameters/hs_main_fibre.csv,
    # summed when the data is loaded
    kg = preloaded_data['intermediate_by_fibre_class'][(product, impeks)]
    return _shares_with_nontextile(kg, [product], current_params, fibre_composition, np.zeros(1))[:, 0, :]


def manufacturing_layer(fibre, tot, preloaded_data, current_params, fibre_composition):
    """
    Fills the MA flows of the fibre system. Norwegian raw wool is WO;
    greasy wool is counted as WO including its grease, so the scouring loss
    is WO too. Traded fibre and yarn have the main fibre of their HS codes.
    Hand knitting yarn to DI.RT is WO: the Prodcom code it comes from is wool
    yarn. Yarn to textile manufacturing is the balance of MA.FI per
    material, clipped at 0: a material whose exports, losses and hand
    knitting yarn exceed its supply (wool in 1989 and 2000 in some draws)
    gets 0, and the flow is then larger than in TOT by the clipped mass,
    which the clipping stock of MA.FI takes up. Traded fabric has the main
    fibre of its HS codes, production waste the mix of yarn and fabric
    entering MA.TX, and finished goods to DI.RT the rest of MA.TX per
    material.
    """
    fibre.flows[HAND_KNITTING_YARN].values[...] = tot.flows[HAND_KNITTING_YARN].values[..., None] * _only('WO')
    fibre.flows[RAW_WOOL].values[...] = tot.flows[RAW_WOOL].values[:, None] * _only('WO')
    fibre.flows[SCOURING_LOSS].values[...] = tot.flows[SCOURING_LOSS].values[:, None] * _only('WO')
    for code, product, impeks in ((FIBRE_YARN_IMPORT, 'FY', 1), (FIBRE_YARN_EXPORT, 'FY', 2),
                                  (FABRIC_IMPORT, 'FA', 1), (TEXTILE_EXPORT, 'FA', 2)):
        shares = intermediate_composition(preloaded_data, current_params, fibre_composition, product, impeks)
        fibre.flows[code].values[...] = tot.flows[code].values[:, None] * shares
    balance = sum(fibre.flows[c].values for c in (RAW_WOOL, FIBRE_YARN_IMPORT)) - sum(
        fibre.flows[c].values for c in (FIBRE_YARN_EXPORT, SCOURING_LOSS)) - fibre.flows[
        HAND_KNITTING_YARN].values.sum(axis=1)
    clip_negative(fibre, YARN_TO_MANUFACTURING, balance)
    inputs = fibre.flows[YARN_TO_MANUFACTURING].values + fibre.flows[FABRIC_IMPORT].values
    fibre.flows[PRECONSUMER_WASTE].values[...] = (tot.flows[PRECONSUMER_WASTE].values[:, None]
                                                  * inputs / inputs.sum(axis=1, keepdims=True))
    fibre.flows[DOMESTIC_GOODS].values[...] = (tot.flows[DOMESTIC_GOODS].values[..., None]
                                               * domestic_goods_composition(fibre)[:, None, :])


def domestic_goods_composition(fibre):
    """
    Material shares of finished goods made in Norway, array (year, material):
    the balance of MA.TX per material, with materials that come out
    negative set to 0 (the clipping stock of MA.TX takes up the difference).
    Every product gets the same composition.
    """
    balance = (fibre.flows[YARN_TO_MANUFACTURING].values + fibre.flows[FABRIC_IMPORT].values
               - fibre.flows[TEXTILE_EXPORT].values - fibre.flows[PRECONSUMER_WASTE].values)
    clipped = np.clip(balance, 0.0, None)
    total = clipped.sum(axis=1, keepdims=True)
    # In a year where every material is negative, the TOT flow is clipped to
    # 0 too, so the composition does not matter.
    return np.divide(clipped, total, out=np.zeros_like(clipped), where=total > 0)


def retail_composition(tot, imported, domestic_goods):
    """
    Material shares of goods leaving DI.RT, array (year, product, material):
    the mix of registered imports, finished goods made in Norway
    (domestic_goods, array (year, material)) and hand knitting yarn spun in
    Norway (WO), so that DI.RT balances per material.
    """
    imports = tot.flows[FINISHED_IMPORT].values
    goods = tot.flows[DOMESTIC_GOODS].values
    yarn = tot.flows[HAND_KNITTING_YARN].values
    mixed = (imports[..., None] * imported + goods[..., None] * domestic_goods[:, None, :]
             + yarn[..., None] * _only('WO'))
    return mixed / (imports + goods + yarn)[..., None]


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
    lifetimes per product. Second-hand purchases (1-2 % of the inflow) are
    left out. Returns {'discards', 'stock', 'stock_change'} as FlodymArrays
    (year, product, material) over the model years, and 'stock_1987' as an
    array (product, material); the stock includes the spin-up cohorts.
    """
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    new_goods = sum(tot.flows[code].values for code in NEW_GOODS_TO_HOUSEHOLDS)[:, core]
    cohorts = use_cohorts(new_goods[:, :, None] * supply[:, core, :], CORE_GROUP_PRODUCTS, current_params)
    stock = np.concatenate([cohorts['stock_1987'][None], cohorts['stock']], axis=0)
    return {
        'discards': fd.FlodymArray(dims=COHORT_DIMS, values=cohorts['outflow']),
        'stock': fd.FlodymArray(dims=COHORT_DIMS, values=cohorts['stock']),
        'stock_change': fd.FlodymArray(dims=COHORT_DIMS, values=np.diff(stock, axis=0)),
        'stock_1987': cohorts['stock_1987'],
    }


def household_discard_composition(tot, cohorts, supply, current_params):
    """
    Material shares of household discards, array (year, product group,
    material). CORE: outflow of the cohort model of new goods. CA, TA and
    OM: outflow of a cohort model of the goods sold to households, as in the
    TOT calculation. SA is not used by households, so it keeps the supply
    composition (its flows are zero).
    """
    outflow = cohorts['discards'].values.sum(axis=1)
    sales = tot.flows['DI.RT-US.HH-Sales to households-TOT'].values
    others = [PRODUCTS.index(p) for p in OTHER_HOUSEHOLD_GOODS]
    other_outflow = use_cohorts(sales[:, others, None] * supply[:, others, :], OTHER_HOUSEHOLD_GOODS,
                                      current_params)['outflow']
    composition = np.empty((len(YEARS), len(PRODUCT_GROUPS), len(MATERIALS)))
    for g, group in enumerate(PRODUCT_GROUPS):
        if group == 'CORE':
            composition[:, g, :] = outflow / outflow.sum(axis=1, keepdims=True)
        elif group in OTHER_HOUSEHOLD_GOODS:
            part = other_outflow[:, OTHER_HOUSEHOLD_GOODS.index(group), :]
            composition[:, g, :] = part / part.sum(axis=1, keepdims=True)
        else:
            composition[:, g, :] = supply[:, PRODUCTS.index(group), :]
    return composition


def institutional_discard_composition(tot, supply, current_params):
    """
    Material shares of goods discarded by institutions and businesses, array
    (year, product, material): the outflow of a cohort model of the goods
    sold to them, as in the TOT calculation. Sacks and retail yarn keep the
    supply composition.
    """
    sales = tot.flows[INSTITUTIONAL_SALES].values
    cohort = [PRODUCTS.index(p) for p in INSTITUTIONAL_COHORT_PRODUCTS]
    outflow = use_cohorts(sales[:, cohort, None] * supply[:, cohort, :], INSTITUTIONAL_COHORT_PRODUCTS,
                          current_params, stock='US.IC')['outflow']
    composition = supply.copy()
    composition[:, cohort, :] = outflow / outflow.sum(axis=2, keepdims=True)
    return composition


def institutional_release_composition(tot, supply, current_params):
    """
    Material shares of fibres released in industrial laundry, array (year,
    product, material): the fibre groups of the textile stock of the US.IC
    cohort model per product, without non-textile material. Products
    without a stock keep the supply composition (their flows are zero).
    """
    sales = tot.flows[INSTITUTIONAL_SALES].values
    cohort = [PRODUCTS.index(p) for p in INSTITUTIONAL_COHORT_PRODUCTS]
    stock = use_cohorts(sales[:, cohort, None] * supply[:, cohort, :], INSTITUTIONAL_COHORT_PRODUCTS,
                        current_params, stock='US.IC')['stock']
    stock[:, :, MATERIALS.index('NT')] = 0.0
    composition = supply.copy()
    composition[:, cohort, :] = stock / stock.sum(axis=2, keepdims=True)
    return composition


def release_composition(cohorts):
    """
    Material shares of fibres released from household textiles, array (year,
    material): the fibre groups of the textile stock of the cohort model,
    without non-textile material.
    """
    stock = cohorts['stock'].values.sum(axis=1)
    stock[:, MATERIALS.index('NT')] = 0.0
    return stock / stock.sum(axis=1, keepdims=True)


def collected_composition(fibre):
    """
    Material shares of what passes through CO, array (year, product group,
    material): the mix of used textiles collected from households and
    unsold goods donated by retailers, so that CO.CO balances per material.
    """
    mix = to_dims(fibre.flows[COLLECTION], ('t', 'g', 'm')).values + to_dims(
        fibre.flows[UNSOLD_DONATED], ('t', 'g', 'm')).values
    total = mix.sum(axis=2, keepdims=True)
    # Groups that collect nothing (all but CORE) get zero flows anyway.
    return np.divide(mix, total, out=np.zeros_like(mix), where=total > 0)


def compute_fibre_layer(fibre, tot, preloaded_data, current_params, fibre_composition):
    """
    Fills the fibre system from the closed TOT system and closes it. Returns
    {output name: FlodymArray with material dimension} for the parallel stock
    model and for the stock level of the statistics-based balance.
    """
    unassigned = set(tot.flows) - set(SUPPLY_FLOWS + DISCARD_FLOWS + COLLECTED_FLOWS + RELEASE_FLOWS + MIXED_FLOWS
                                      + MANUFACTURING_FLOWS + [INSTITUTIONAL_WASTE, INSTITUTIONAL_RELEASE])
    if unassigned:
        raise KeyError(f"Flows without a fibre layer rule: {sorted(unassigned)}")

    reset(fibre)
    imported = supply_composition(preloaded_data, current_params, fibre_composition)
    manufacturing_layer(fibre, tot, preloaded_data, current_params, fibre_composition)
    supply = retail_composition(tot, imported, domestic_goods_composition(fibre))
    for code in SUPPLY_FLOWS:
        shares = imported if code == FINISHED_IMPORT else supply
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * shares
    fibre.flows[INSTITUTIONAL_WASTE].values[...] = tot.flows[INSTITUTIONAL_WASTE].values[..., None] * (
        institutional_discard_composition(tot, supply, current_params))
    fibre.flows[INSTITUTIONAL_RELEASE].values[...] = tot.flows[INSTITUTIONAL_RELEASE].values[..., None] * (
        institutional_release_composition(tot, supply, current_params))
    cohorts = household_cohort_model(tot, supply, current_params)
    discards = household_discard_composition(tot, cohorts, supply, current_params)
    for code in DISCARD_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * discards
    collected = collected_composition(fibre)
    for code in COLLECTED_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * collected
    released = release_composition(cohorts)
    for code in RELEASE_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * released[:, None, :]

    mix = sum(to_dims(f, ('t', 'm')).values for f in fibre.flows.values() if f.to_process.name == MIXED_SOURCE)
    mix_shares = mix / mix.sum(axis=1, keepdims=True)
    for code in MIXED_FLOWS:
        fibre.flows[code].values[...] = tot.flows[code].values[..., None] * mix_shares

    # Flows taken from TOT carry its clipping; MA.FI yarn is clipped again per
    # material and exceeds TOT by that clipped mass, which stays in MA.TX
    # because the MA.TX outflows are taken from TOT.
    fibre.clipped_inflows = set(fibre.clipped)
    fibre.clipped_at_target = set(tot.clipped_at_target)
    for code, clipped in tot.clipped.items():
        fibre.clipped.setdefault(code, clipped)
    close(fibre)
    for code, flow in tot.flows.items():
        own = code in fibre.clipped and fibre.clipped[code] is not tot.clipped.get(code)
        extra = fibre.clipped[code].values.sum(axis=-1) if own else 0.0
        gap = np.abs(fibre.flows[code].values.sum(axis=-1) - extra - flow.values).max()
        if gap > TOLERANCE_KT:
            raise ValueError(f"Fibre layer of {code} does not add up to TOT (max gap {gap:.2e} kt)")
    stock = fibre.stocks['US.HH']
    change = (stock.inflow - stock.outflow).values[:, PRODUCT_GROUPS.index('CORE'), :]
    level = cohorts['stock_1987'].sum(axis=0) + np.cumsum(change, axis=0)
    result = {STOCK_MODEL_OUTPUTS[key]: cohorts[key] for key in STOCK_MODEL_OUTPUTS}
    result[RESIDUAL_STOCK_OUTPUT] = fd.FlodymArray(dims=CORE_STOCK_DIMS, values=level[:, None, :])
    return result
