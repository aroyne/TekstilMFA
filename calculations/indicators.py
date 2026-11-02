#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indicators computed from the closed TOT system in each MC iteration, so that
their uncertainty keeps the correlations between the flows they combine
(phase E: E1 and E2).

E1, the basis for extended producer responsibility (EPR): textiles and
footwear made available on the Norwegian market for the first time, for the
customs codes in annex 1 of the proposed regulation (Miljødirektoratet,
hearing 2026/4671): chapters 61 and 62, headings 6301-6304 (except electric
blankets, 6301 1000), 6309, 6401-6405, 4203 and 6504-6505. Leather clothing
(4203) and hats (6504-6505) are not in the trade data of the model and are
left out; they are small. Duvets and cushions (9404), which the model counts
as household textiles, are outside the scope. Foreign web shops that sell
directly to Norwegian end users are producers, so direct online imports are
included.

E2, the separate collection rate: textiles collected separately from
households divided by all textiles discarded by households (collection plus
reusable and worn textiles in residual and bulky waste), for the CORE group.
"""
import numpy as np

from calculations.utils import PRODUCTS, YEARS

EPR_HS_PREFIXES = ('61', '62', '6301', '6302', '6303', '6304', '6401', '6402', '6403', '6404', '6405')
EPR_EXCLUDED_HS8 = ('63011000',)
EPR_PRODUCTS = ['CL', 'HT', 'FW']


def epr_scope_shares(trade):
    """
    Share of the finished-goods mass of each EPR product that is within the
    EPR customs codes, {(impeks, product): array (year,)}, from the HS8
    trade data. Clothing and footwear are (nearly) all in scope; household
    textiles lose the duvets and cushions in 9404. Key 'used' is the share
    of used clothing (6309, in scope) in the import of used textiles, which
    also holds rags (6310, out of scope).
    """
    finished = trade[(trade['category'] == 'finished') & (trade['in_scope'] == 'yes')]
    in_scope = (finished['HS8'].str.startswith(EPR_HS_PREFIXES) & ~finished['HS8'].isin(EPR_EXCLUDED_HS8))
    total = finished.groupby(['impeks', 'product', 'year'])['amount'].sum()
    scope = finished[in_scope].groupby(['impeks', 'product', 'year'])['amount'].sum()
    shares = {}
    for impeks in (1, 2):
        for product in EPR_PRODUCTS:
            t = total.loc[impeks, product].reindex(YEARS)
            s = scope.reindex(t.index.map(lambda y: (impeks, product, y))).to_numpy()
            shares[(impeks, product)] = np.nan_to_num(s, nan=0.0) / t.to_numpy()
    used = trade[(trade['category'] == 'used') & (trade['impeks'] == 1)].groupby(['year', 'product'])['amount'].sum()
    used = used.unstack(fill_value=0.0).reindex(YEARS)
    shares['used'] = (used['UT'] / used.sum(axis=1)).to_numpy()
    return shares


def _by_epr_product(mfa, code):
    values = mfa.flows[code].values
    return {p: values[:, PRODUCTS.index(p)] for p in EPR_PRODUCTS}


def indicators(mfa, preloaded_data):
    """{indicator name: array (year,)} for one closed TOT system."""
    # 'epr_scope_share' <- data_files/Tab_08801_textiles.csv (SSB 08801), the
    # share of finished-goods mass within the EPR customs codes, computed
    # when the data is loaded
    shares = preloaded_data['epr_scope_share']
    imports = _by_epr_product(mfa, 'RW.RW-DI.RT-Finished textile products import-TOT')
    exports = _by_epr_product(mfa, 'DI.RT-RW.RW-Export of finished textile products-TOT')
    domestic = _by_epr_product(mfa, 'MA.TX-DI.RT-Domestic finished products-TOT')
    online = _by_epr_product(mfa, 'RW.RW-US.HH-Direct online imports-TOT')
    returns = _by_epr_product(mfa, 'US.HH-RW.RW-Returns of direct online purchases-TOT')
    used_import = mfa.flows['RW.RW-CO.SO-Used textile import-TOT'].values[:, 0] * shares['used']

    # Goods made in Norway are taken to have the same scope share as imports.
    gross = sum(shares[(1, p)] * (imports[p] + domestic[p]) + online[p] for p in EPR_PRODUCTS) + used_import
    net = gross - sum(shares[(2, p)] * exports[p] + returns[p] for p in EPR_PRODUCTS)

    collection = mfa.flows['US.HH-CO.CO-Separate collection from households-TOT'].values[:, 0]
    residual = (mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values[:, 0]
                + mfa.flows['US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT'].values[:, 0])
    return {
        'EPR basis, placed on market, gross (kt)': gross,
        'EPR basis, net of re-export and online returns (kt)': net,
        'Separate collection rate, households, CORE (share)': collection / (collection + residual),
    }
