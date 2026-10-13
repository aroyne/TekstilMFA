#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MA (manufacturing) pool. MA.FI (fibre and yarn production) receives
Norwegian raw wool and imported fibre and yarn, and sends fibre and yarn
abroad, hand knitting yarn to retail (DI.RT) and the rest to MA.TX. Traded fibre and yarn are the HS 50-55 codes that are
neither woven fabric nor yarn put up for retail sale (parameters/
hs_mapping.csv, product 'FY'); retail yarn goes to DI.RT as product 'YA'
and HS 56 is outside the scope.

Most Norwegian wool is exported greasy and scoured abroad (mainly in
Bradford); only the part scoured in Norway loses its grease and dirt here.

MA.TX (textile, apparel and footwear manufacturing) receives yarn from
MA.FI and imported fabric (product 'FA': woven fabric in HS 50-55, HS 58
and 60; HS 59 is outside the scope), exports fabric, discards production
waste and sends the rest to DI.RT as finished goods. Exports of finished
goods stay with DI.RT (D6).
"""
import numpy as np
import pandas as pd

from calculations.system import clip_negative
from calculations.timeseries import interpolate
from calculations.trade import trade_kt
from calculations.utils import PRODUCTS, YEARS

HAND_KNITTING_YARN_PRODCOM = '13.10.50.50'
# Prodcom has most published quantities in 2008, 2009 and 2011; their mean
# per commodity is one anchor, placed at 2009.
PRODCOM_ANCHOR_YEAR = 2009
# Footwear is made mainly of leather and rubber, which are not MA.TX inputs,
# so the textile balance of MA.TX cannot become footwear.
NOT_FROM_TEXTILE_BALANCE = ['FW']


def execute_calculations_ma(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _norwegian_raw_wool_mc(mfa, preloaded_data, dataset_noise)
    _fibre_and_yarn_import_mc(mfa, preloaded_data, dataset_noise)
    _fibre_and_yarn_export_mc(mfa, preloaded_data, dataset_noise)
    _wool_scouring_loss_mc(mfa, current_params, anchors)
    _domestic_hand_knitting_yarn_mc(mfa, preloaded_data, dataset_noise)
    _yarn_to_manufacturing_mc(mfa)
    _fabric_import_mc(mfa, preloaded_data, dataset_noise)
    _textile_export_mc(mfa, preloaded_data, dataset_noise)
    _preconsumer_waste_mc(mfa, anchors)
    _domestic_finished_products_mc(mfa, preloaded_data)


def _norwegian_raw_wool_mc(mfa, preloaded_data, dataset_noise):
    """
    Norwegian wool (greasy, as weighed in) from Totalkalkylen for
    jordbrukssektoren (Budsjettnemnda for jordbruket, NIBIO), the official
    agricultural account; the series starts in 1959. The last year in the
    file is a budget figure and the one before it preliminary.
    """
    # 'wool_production' <- data_files/NIBIO_totalkalkylen_ull.csv: Norwegian
    # wool, tonnes, NOK/kg and value per year from Totalkalkylen (NIBIO API)
    tonnes = preloaded_data['wool_production']
    kt = np.array([tonnes[year] for year in YEARS]) / 1000
    mfa.flows['PS.WO-MA.FI-Norwegian raw wool-TOT'].values[...] = kt * dataset_noise['totalkalkylen']


def _fibre_and_yarn_import_mc(mfa, preloaded_data, dataset_noise):
    """
    Registered imports of fibre and yarn, SSB 08801 (HS 50-55 except woven
    fabric and retail yarn). Includes raw, scoured and carbonised wool and
    tops returning after scouring abroad.
    """
    mfa.flows['RW.RW-MA.FI-Fibre and yarn import-TOT'].values[...] = (
        trade_kt(preloaded_data, dataset_noise, True, 'intermediate', ['FY'])[:, 0])


def _fibre_and_yarn_export_mc(mfa, preloaded_data, dataset_noise):
    """
    Registered exports of fibre and yarn, SSB 08801 (HS 50-55 except woven
    fabric and retail yarn). Dominated by greasy Norwegian wool (HS 5101.11
    and 5101.19), which since 2007 is 90-100 % of Norwegian wool. Yarn
    exports may include re-export of yarn spun abroad for Norwegian brands,
    which the trade statistics do not separate from domestic production.
    """
    mfa.flows['MA.FI-RW.RW-Fibre and yarn export-TOT'].values[...] = (
        trade_kt(preloaded_data, dataset_noise, False, 'intermediate', ['FY'])[:, 0])


def _wool_scouring_loss_mc(mfa, current_params, anchors):
    """
    Grease, suint and dirt removed when greasy wool is scoured in Norway,
    sent with the scouring water to wastewater treatment. The greasy wool
    scoured in Norway is Norwegian wool plus imports minus exports of greasy
    wool, as a mean over periods because the annual balance is dominated by
    the timing of shearing, storage and export (anchors derived by
    scripts/derive_wool_scouring_anchors.py): about 2.8 kt in 1988-1995,
    2.2 kt in 1996-2000, 1.3 kt in 2001-2006 and 0.3 kt from 2007, when
    nearly all Norwegian wool is exported greasy. Exports declared as
    carbonised wool in 1996-2000 and 2002 are counted as greasy, because
    they are priced like greasy wool. The loss share is about a third of the
    greasy weight.
    """
    scoured = interpolate(anchors['wool_scoured_domestic'])
    mfa.flows['MA.FI-WM.WW-Wool scouring loss-TOT'].values[...] = (
        scoured * current_params['wool_scouring_loss_share'])


def _domestic_hand_knitting_yarn_mc(mfa, preloaded_data, dataset_noise):
    """
    Yarn spun in Norway and put up for retail sale (product YA), sold to
    households through retail; hand knitting yarn is by far the largest
    product of the Norwegian spinning mills. Wool yarn put up for retail
    sale produced in large establishments: 0.99 and 0.89 kt in 1988 and 1989
    (SSB Industristatistikk, Varetall, commodity 5109.10), and 0.59-1.03 kt
    in 2008-2023 (SSB 10455, Prodcom 13.10.50.50, sold production). SSB
    published no commodity figures for 1990-2007, and suppresses some
    Prodcom years; those years are interpolated, and the series is held at
    its last value after 2023. Both sources cover large units only (Sandnes
    Garn alone makes about 600 t a year, and SNL gives about 1000 t for all
    Norwegian spinning mills), so the noise factor is skewed upwards. Cotton
    and synthetic yarn put up for retail sale are suppressed in every year
    and are left out.
    """
    # 'varetall' <- data_files/SSB_industristatistikk_varetall_1988_1989.csv:
    # commodities produced in large establishments in 1988 and 1989 (SSB
    # Industristatistikk, Hefte II Varetall); product YA is wool yarn put up
    # for retail sale, in tonnes
    varetall = preloaded_data['varetall']
    yarn = varetall[varetall['product'] == 'YA']
    early = yarn.groupby('year')['quantity'].sum() / 1000
    # 'prodcom' <- data_files/SSB_10455_prodcom_garn_tau_nett_2008_2025.csv:
    # sold production by Prodcom code (13.10 yarn, 13.94 ropes and nets),
    # quantity and value, 2008-2025, with SSB's status codes
    prodcom = preloaded_data['prodcom']
    sel = prodcom[(prodcom['prodcom'] == HAND_KNITTING_YARN_PRODCOM) & (prodcom['variable'] == 'Mengde')]
    published = sel.dropna(subset=['value'])
    late = published.set_index('year')['value'] / 1e6
    kt = interpolate({**early.to_dict(), **late.to_dict()})
    flow = mfa.flows['MA.FI-DI.RT-Domestic hand knitting yarn-TOT']
    flow.values[...] = 0.0
    flow.values[:, PRODUCTS.index('YA')] = kt * dataset_noise['vareproduksjon']


def _yarn_to_manufacturing_mc(mfa):
    """
    Balance of MA.FI: Norwegian wool and imported fibre and yarn minus
    exports, the scouring loss and hand knitting yarn sold through retail.
    A negative balance is not physical and is clipped at 0; the clipped
    mass is recorded and reported on the flow page.
    """
    supply = (mfa.flows['PS.WO-MA.FI-Norwegian raw wool-TOT'].values
              + mfa.flows['RW.RW-MA.FI-Fibre and yarn import-TOT'].values)
    removed = (mfa.flows['MA.FI-RW.RW-Fibre and yarn export-TOT'].values
               + mfa.flows['MA.FI-WM.WW-Wool scouring loss-TOT'].values
               + mfa.flows['MA.FI-DI.RT-Domestic hand knitting yarn-TOT'].values.sum(axis=1))
    balance = supply - removed
    clip_negative(mfa, 'MA.FI-MA.TX-Yarn to textile manufacturing-TOT', balance)


def _fabric_import_mc(mfa, preloaded_data, dataset_noise):
    """Registered imports of fabric, SSB 08801 (woven fabric in HS 50-55, HS 58 and 60)."""
    mfa.flows['RW.RW-MA.TX-Fabric import-TOT'].values[...] = (
        trade_kt(preloaded_data, dataset_noise, True, 'intermediate', ['FA'])[:, 0])


def _textile_export_mc(mfa, preloaded_data, dataset_noise):
    """
    Registered exports of fabric, SSB 08801 (woven fabric in HS 50-55, HS 58
    and 60). Exports of finished goods are counted from DI.RT, because the
    trade statistics do not separate re-export from Norwegian production
    (D6).
    """
    mfa.flows['MA.TX-RW.RW-Textile export-TOT'].values[...] = (
        trade_kt(preloaded_data, dataset_noise, False, 'intermediate', ['FA'])[:, 0])


def _manufacturing_input(mfa):
    return (mfa.flows['MA.FI-MA.TX-Yarn to textile manufacturing-TOT'].values
            + mfa.flows['RW.RW-MA.TX-Fabric import-TOT'].values)


def _preconsumer_waste_mc(mfa, anchors):
    """
    Textile waste generated by the textile, apparel and leather industry
    (NACE 13-15) in SSB's surveys of industrial waste (08604, 14457): 1 kt in
    2008 and below 0.5 kt in 2015 and 2022 (published rounded to whole kt).
    The waste is expressed per kt of MA.TX input (yarn and fabric) in the
    anchor years and the ratio is interpolated, so the waste follows the
    input before 2008, with 2008 as reference, and after 2022.
    """
    waste = anchors['preconsumer_waste_textile_industry']
    total_input = _manufacturing_input(mfa)
    ratio = interpolate({year: kt / total_input[YEARS.index(year)] for year, kt in waste.items()})
    mfa.flows['MA.TX-WM.RS-Preconsumer production waste-TOT'].values[...] = ratio * total_input


def _domestic_product_shares(preloaded_data):
    """
    Mass share of each product in finished goods made in Norway, array
    (year, product), from SSB's commodity statistics for large units (D26).
    """
    # 'domestic_production' <- data_files/domestic_production_mass.csv: mass
    # of finished goods made in Norway per commodity in 1988, 1989 (SSB
    # Industristatistikk, Varetall) and 2008, 2009, 2011 (Prodcom, SSB 10455),
    # from scripts/derive_domestic_product_mass.py
    mass = preloaded_data['domestic_production']
    early = mass[mass['source'] == 'varetall'].groupby(['year', 'product'])['mass_t'].sum().unstack(fill_value=0.0)
    prodcom = mass[mass['source'] == 'prodcom'].groupby(['code', 'product'])['mass_t'].mean()
    late = prodcom.groupby('product').sum().to_frame(PRODCOM_ANCHOR_YEAR).T
    table = pd.concat([early, late]).reindex(columns=PRODUCTS, fill_value=0.0).fillna(0.0)
    table[NOT_FROM_TEXTILE_BALANCE] = 0.0
    shares = table.div(table.sum(axis=1), axis=0)
    return np.stack([interpolate(shares[p].to_dict()) for p in PRODUCTS], axis=1)


def _domestic_finished_products_mc(mfa, preloaded_data):
    """
    Balance of MA.TX: yarn and fabric in, minus fabric exports and
    production waste, split over products by mass shares of finished goods
    made in Norway (D26). The shares come from SSB's commodity statistics
    for large units: Industristatistikk, Varetall, 1988 and 1989, and
    Prodcom 2008, 2009 and 2011 averaged per commodity (anchor 2009). Mass
    is taken as published, from pieces times the import mass per piece, or
    from value divided by a Norwegian price per kg. The shares are
    interpolated between the anchors and held after 2009. Footwear is left
    out, because its main materials (leather, rubber) are not MA.TX inputs.
    Around 1988-89 clothing and household textiles are about a third each
    and tarpaulins and tents about a fifth; in 2008-2011 household textiles
    (mostly bedding) are about half, tarpaulins and tents a quarter and
    clothing a fifth.

    The balance seems too high: SSB's commodity statistics give 7-8 kt for
    large units in 1988-89 and about 4.5 kt in 2008-2011, against 8-18 kt
    here, and the household stock rises accordingly. Part of the imported
    fabric and yarn probably goes to other industries (upholstery,
    mattresses, vehicle and boat interiors, technical uses), which are
    outside the scope. The balance is kept until this is resolved.

    A negative balance is not physical and is clipped at 0; the clipped
    mass is recorded and reported on the flow page.
    """
    balance = (_manufacturing_input(mfa)
               - mfa.flows['MA.TX-RW.RW-Textile export-TOT'].values
               - mfa.flows['MA.TX-WM.RS-Preconsumer production waste-TOT'].values)
    clip_negative(mfa, 'MA.TX-DI.RT-Domestic finished products-TOT',
                  balance[:, None] * _domestic_product_shares(preloaded_data))

