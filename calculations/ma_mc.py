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
"""
import numpy as np

from calculations.timeseries import interpolate
from calculations.trade import trade_kt
from calculations.utils import PRODUCTS, YEARS

HAND_KNITTING_YARN_PRODCOM = '13.10.50.50'


def execute_calculations_ma(mfa, preloaded_data, current_params, dataset_noise, anchors):
    _norwegian_raw_wool_mc(mfa, preloaded_data, dataset_noise)
    _fibre_and_yarn_import_mc(mfa, preloaded_data, dataset_noise)
    _fibre_and_yarn_export_mc(mfa, preloaded_data, dataset_noise)
    _wool_scouring_loss_mc(mfa, current_params, anchors)
    _domestic_hand_knitting_yarn_mc(mfa, preloaded_data, dataset_noise)
    _yarn_to_manufacturing_mc(mfa)


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
    # wool yarn put up for retail sale produced in large establishments,
    # tonnes, from SSB Industristatistikk 1988 and 1989, Hefte II Varetall
    varetall = preloaded_data['varetall']
    early = varetall.groupby('year')['quantity'].sum() / 1000
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
    """
    supply = (mfa.flows['PS.WO-MA.FI-Norwegian raw wool-TOT'].values
              + mfa.flows['RW.RW-MA.FI-Fibre and yarn import-TOT'].values)
    removed = (mfa.flows['MA.FI-RW.RW-Fibre and yarn export-TOT'].values
               + mfa.flows['MA.FI-WM.WW-Wool scouring loss-TOT'].values
               + mfa.flows['MA.FI-DI.RT-Domestic hand knitting yarn-TOT'].values.sum(axis=1))
    balance = supply - removed
    if (balance < 0).any():
        year = YEARS[int(np.argmax(balance < 0))]
        raise ValueError(f"Negative MA.FI balance in {year}: {balance[YEARS.index(year)]:.3f} kt")
    mfa.flows['MA.FI-MA.TX-Yarn to textile manufacturing-TOT'].values[...] = balance
