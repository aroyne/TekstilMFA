#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function categories of clothing (CL) and footwear (FW) in the household
cohort model (claude_tekst/2026-11-05_funksjonskategorier_forslag.md). The
register keeps the products; inside the cohort model each cohort of CL and
FW is split into categories by the import mass of their HS codes that year
(SSB 08801), and each category has its own lifetimes. Household textiles
(HT) and retail yarn (YA) are not split.

A category discards goods for two competing reasons: worn out or damaged
(technical lifetime) and no longer wanted (perceived lifetime: out of
fashion, bored, outgrown, no longer fits). The survival is the product of
two Weibull functions. Per category four parameters are drawn:
* relative lifetime: the mean time to discard relative to the product
  (WRAP 2012, 2021: coats and outdoor wear over five years, underwear and
  socks under three), scaled so that the mean for the 2025 mix equals the
  lifetime of the product, so the categories change the spread and the
  dynamics, not the level;
* broken share: the share of discards that are damaged beyond easy repair
  (Syversen et al. 2023, Mepex, table 23: 100 % minus the usable share per
  category, all streams, 2021-2022);
* repairable share: the share of technical discards that can easily be
  fixed and therefore count as usable in the pick analyses; together with
  the broken share it gives the share of discards that are due to wear,
  broken / (1 - repairable), which sets how much durability and repair can
  do (it replaces X18);
* policy sensitivity: how strongly a tax on new textiles or rental and
  sharing (L5, L8) acts on the category (impulse buying and fashion),
  normalised so that the mean over the 2025 mix is 1.
"""
import math

import numpy as np
from scipy import integrate

from calculations.cohorts import competing_survival, unit_cohorts
from calculations.utils import CORE_GROUP_PRODUCTS, YEARS

CATEGORIES = {'CL': ['K1', 'K2', 'K3', 'K4', 'K5'], 'FW': ['S1', 'S2', 'S3', 'S4']}
# Units of the household cohort model for the CORE group: categories for CL
# and FW, the product itself for HT and YA.
UNITS = [u for p in CORE_GROUP_PRODUCTS for u in CATEGORIES.get(p, [p])]
PRODUCT_OF_UNIT = {u: p for p in CORE_GROUP_PRODUCTS for u in CATEGORIES.get(p, [p])}
CATEGORY_LABELS = {
    'K1': 'underwear, socks, nightwear', 'K2': 'tops and knitwear', 'K3': 'bottoms and dresses',
    'K4': 'outerwear, sports and functional clothing, accessories', 'K5': "children's and babies' clothing",
    'S1': 'sports and leisure footwear', 'S2': 'everyday and formal leather footwear',
    'S3': 'winter, hiking and waterproof footwear', 'S4': 'other footwear (sandals, slippers, textile, parts)',
}
# HS4 of chapters 61 and 62 per clothing category.
CLOTHING_HS4 = {
    'K1': ['6107', '6108', '6115', '6207', '6208', '6212'],
    'K2': ['6105', '6106', '6109', '6110', '6205', '6206'],
    'K3': ['6103', '6104', '6203', '6204'],
    'K4': ['6101', '6102', '6112', '6113', '6114', '6116', '6117', '6201', '6202', '6210', '6211', '6213', '6214',
           '6215', '6216', '6217'],
    'K5': ['6111', '6209'],
}
# HS6 of chapter 64 per footwear category: sports (incl. ski boots),
# leather everyday and formal, covering the ankle or waterproof (and safety
# footwear with a metal toe-cap), and the rest (sandals, slippers, textile
# and wooden footwear, parts).
FOOTWEAR_HS6 = {
    'S1': ['640211', '640212', '640219', '640311', '640312', '640319', '640411'],
    'S2': ['640351', '640359', '640399'],
    'S3': ['640110', '640191', '640192', '640199', '640291', '640340', '640391'],
    'S4': ['640220', '640230', '640299', '640320', '640330', '640419', '640420', '640510', '640520', '640590',
           '640610', '640620', '640690', '640691', '640699'],
}
TECHNICAL_SHAPE = 2.0
PERCEIVED_SHAPE = 1.5


def category_of(product, hs8):
    """The function category of an HS8 code of CL or FW; KeyError for a code not covered."""
    table = CLOTHING_HS4 if product == 'CL' else FOOTWEAR_HS6
    key = hs8[:4] if product == 'CL' else hs8[:6]
    for category, codes in table.items():
        if key in codes:
            return category
    raise KeyError(f"HS code {hs8} of {product} has no function category")


def category_shares(trade):
    """
    Import mass share of each category within CL and FW per year, {product:
    array (year, category)}, from the in-scope finished-goods imports. Goods
    sold, imported privately or bought online are taken to have the same mix.
    """
    shares = {}
    for product, categories in CATEGORIES.items():
        sel = trade[(trade['category'] == 'finished') & (trade['in_scope'] == 'yes') & (trade['impeks'] == 1)
                    & (trade['product'] == product)]
        cat = sel['HS8'].map(lambda hs: category_of(product, hs))
        kg = sel.groupby([sel['year'], cat])['amount'].sum().unstack(fill_value=0.0).reindex(
            index=YEARS, columns=categories, fill_value=0.0)
        shares[product] = (kg / kg.sum(axis=1).to_numpy()[:, None]).to_numpy()
    return shares


def unit_shares(shares):
    """Share of each unit within its product per year, array (year, unit); 1 for HT and YA."""
    out = np.ones((len(YEARS), len(UNITS)))
    for product, categories in CATEGORIES.items():
        for j, category in enumerate(categories):
            out[:, UNITS.index(category)] = shares[product][:, j]
    return out


# Wear share w (probability that the technical lifetime ends first) and the
# mean time to discard g, both as functions of the ratio of the perceived to
# the technical Weibull scale, with technical scale 1. Tabulated once and
# inverted by interpolation.
_RATIOS = np.logspace(-2.5, 3.0, 600)


def _tabulate():
    wear, mean = [], []
    for rho in _RATIOS:
        def survival(a, rho=rho):
            return np.exp(-a ** TECHNICAL_SHAPE - (a / rho) ** PERCEIVED_SHAPE)

        def technical_density(a, rho=rho):
            return TECHNICAL_SHAPE * a ** (TECHNICAL_SHAPE - 1.0) * survival(a)
        wear.append(integrate.quad(technical_density, 0.0, np.inf, limit=200)[0])
        mean.append(integrate.quad(survival, 0.0, np.inf, limit=200)[0])
    return np.array(wear), np.array(mean)


_WEAR, _MEAN = _tabulate()


def unit_lifetimes(current_params, shares_2025):
    """
    Technical and perceived Weibull scales per unit, arrays (unit,), and the
    repairable share per unit, from the lifetime of each product and the
    category parameters in current_params. HT and YA have one technical
    lifetime (perceived scale infinite), as before, and their repairable
    share is one minus their broken share.

    The wear share of a category is broken / (1 - repairable); it must be at
    most 0.98 (the spans are chosen so; a draw outside raises). The ratio of
    the scales follows from the wear share, and the technical scale from the
    mean time to discard.
    """
    technical = np.empty(len(UNITS))
    perceived = np.empty(len(UNITS))
    repairable = np.zeros(len(UNITS))
    for product in CORE_GROUP_PRODUCTS:
        mean = current_params[f'lifetime_mean_US.HH_{product}']
        if product not in CATEGORIES:
            shape = current_params[f'lifetime_shape_US.HH_{product}']
            technical[UNITS.index(product)] = mean / math.gamma(1.0 + 1.0 / shape)
            perceived[UNITS.index(product)] = np.inf
            # One reason to discard only, so the broken share is set
            # directly through the repairable share.
            repairable[UNITS.index(product)] = 1.0 - current_params[f'broken_share_{product}']
            continue
        categories = CATEGORIES[product]
        relative = np.array([current_params[f'relative_lifetime_{c}'] for c in categories])
        # The mean over the 2025 mix equals the lifetime of the product.
        scale = mean / (shares_2025[product] * relative).sum()
        for c, rel in zip(categories, relative):
            broken = current_params[f'broken_share_{c}']
            repair = current_params[f'repairable_share_{c}']
            wear = broken / (1.0 - repair)
            if not 0.0 < wear <= 0.98:
                raise ValueError(f"Wear share of {c} is {wear:.2f} (broken {broken:.2f}, repairable {repair:.2f})")
            ratio = np.interp(wear, _WEAR, _RATIOS)
            u = UNITS.index(c)
            technical[u] = rel * scale / np.interp(ratio, _RATIOS, _MEAN)
            perceived[u] = technical[u] * ratio
            repairable[u] = repair
    return technical, perceived, repairable


def policy_sensitivity(current_params, shares_2025):
    """Sensitivity of each unit to L5 and L8, array (unit,), mean 1 over the 2025 mix of its product; 1 for HT, YA."""
    out = np.ones(len(UNITS))
    for product, categories in CATEGORIES.items():
        raw = np.array([current_params[f'policy_sensitivity_{c}'] for c in categories])
        raw = raw / (shares_2025[product] * raw).sum()
        for c, value in zip(categories, raw):
            out[UNITS.index(c)] = value
    return out


def history_units(category_shares_by_product):
    """
    Unit setup of the household cohort model for the historical years:
    unit shares per year (array (year, unit) over YEARS), the 2025 shares
    per product and no lifetime factors.
    """
    return {'shares': unit_shares(category_shares_by_product),
            'shares_2025': {p: s[-1] for p, s in category_shares_by_product.items()},
            'technical_factor': None, 'perceived_factor': None, 'period_factor': None}


def household_core_cohorts(new_goods, units, current_params):
    """
    Cohort model of the CORE group in US.HH by unit (D20 with the function
    categories). new_goods: array (year, CORE product, material) over the
    years from START_YEAR; units: the unit setup (history_units, or the
    future module's, with shares and lifetime factors over the same years).
    Returns per product {'outflow', 'stock', 'broken'} as arrays (year,
    product, material) and 'stock_1987' (product, material), and the same
    per unit under 'units'.
    """
    product_index = [CORE_GROUP_PRODUCTS.index(PRODUCT_OF_UNIT[u]) for u in UNITS]
    inflow = new_goods[:, product_index, :] * units['shares'][:, :, None]
    technical, perceived, repairable = unit_lifetimes(current_params, units['shares_2025'])
    technical_shape = np.array([TECHNICAL_SHAPE if PRODUCT_OF_UNIT[u] in CATEGORIES
                                else current_params[f'lifetime_shape_US.HH_{u}'] for u in UNITS])
    sf, share = competing_survival(new_goods.shape[0], technical, perceived, technical_shape, PERCEIVED_SHAPE,
                                   units['technical_factor'], units['perceived_factor'], units['period_factor'])
    per_unit = unit_cohorts(inflow, sf, share, repairable, current_params['spinup_inflow_factor'])
    aggregate = np.zeros((len(UNITS), len(CORE_GROUP_PRODUCTS)))
    aggregate[np.arange(len(UNITS)), product_index] = 1.0
    result = {key: np.einsum('tum,up->tpm', per_unit[key], aggregate) for key in ('outflow', 'stock', 'broken')}
    result['stock_1987'] = np.einsum('um,up->pm', per_unit['stock_1987'], aggregate)
    result['units'] = per_unit
    return result
