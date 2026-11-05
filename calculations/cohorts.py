#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inflow-driven cohort model of goods in use, in households (US.HH) or
institutions and businesses (US.IC) (D20): Weibull lifetimes per stock and
product from parameters/lifetimes.csv, inflow counted as
arriving in the middle of the year (flodym's default). The inflow before
1988 is held at the 1988 composition and at the 1988 level times
spinup_inflow_factor (1 in the main run) from 1950 (D2), so the stock in
1988 includes the spin-up cohorts.
"""
import math

import flodym as fd
import numpy as np

from calculations.utils import START_YEAR

SPINUP_START = 1950
N_SPINUP = START_YEAR - SPINUP_START


def _weibull(dims, products, current_params, stock, cohort_factor):
    """Weibull lifetime model over dims (t from SPINUP_START), mean per product times cohort_factor."""
    shape = np.array([current_params[f'lifetime_shape_{stock}_{p}'] for p in products])
    mean = np.array([current_params[f'lifetime_mean_{stock}_{p}'] for p in products])
    scale = mean / np.array([math.gamma(1.0 + 1.0 / k) for k in shape])
    if cohort_factor is None:
        scale_dims, scale = dims[('p',)], scale
    else:
        factor = np.concatenate([np.ones((N_SPINUP, len(products))), cohort_factor], axis=0)
        scale_dims, scale = dims[('t', 'p')], scale[None, :] * factor
    return fd.WeibullLifetime(
        dims=dims,
        weibull_shape=fd.Parameter(dims=dims[('p',)], values=shape),
        weibull_scale=fd.Parameter(dims=scale_dims, values=scale),
    )


def survival(n_years, products, current_params, stock='US.HH', cohort_factor=None, period_factor=None):
    """
    Survival factors of the cohort model, array (year, cohort, product) over
    the spin-up years and n_years from START_YEAR: the share of the inflow of
    a cohort still in use at the end of a year, with the same lifetimes as
    use_cohorts.

    period_factor (array (year, product) over the n_years) multiplies the
    Weibull scale of every cohort in that year, so that a measure such as
    repair lowers the risk of discarding at a given age for goods already
    in use too (a period effect, unlike cohort_factor). The survival is then
    built year by year from the conditional survival over each year: with a
    factor of 1 in every year it equals the plain Weibull survival.
    """
    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=list(range(SPINUP_START, START_YEAR + n_years))),
        fd.Dimension(letter='p', name='Product', dtype=str, items=products),
    ])
    if period_factor is None:
        return _weibull(dims, products, current_params, stock, cohort_factor).sf
    shape = np.array([current_params[f'lifetime_shape_{stock}_{p}'] for p in products])
    mean = np.array([current_params[f'lifetime_mean_{stock}_{p}'] for p in products])
    scale = mean / np.array([math.gamma(1.0 + 1.0 / k) for k in shape])
    n = N_SPINUP + n_years
    cohort = np.ones((n, len(products))) if cohort_factor is None else np.concatenate(
        [np.ones((N_SPINUP, len(products))), cohort_factor], axis=0)
    period = np.concatenate([np.ones((N_SPINUP, len(products))), period_factor], axis=0)

    def weibull_sf(age, lam):
        return np.exp(-(np.clip(age, 0.0, None) / lam) ** shape)

    sf = np.zeros((n, n, len(products)))
    for t in range(n):
        # Inflow arrives in the middle of the year (as in flodym), so a
        # cohort is t - c + 0.5 years old at the end of year t.
        age = (t - np.arange(t + 1) + 0.5)[:, None]
        lam = scale[None, :] * cohort[:t + 1] * period[t][None, :]
        conditional = weibull_sf(age, lam) / weibull_sf(age - 1.0, lam)
        previous = np.ones((t + 1, len(products)))
        previous[:t] = sf[t - 1, :t] if t > 0 else previous[:t]
        sf[t, :t + 1] = previous * conditional
    return sf


def use_cohorts(inflow, products, current_params, stock='US.HH', cohort_factor=None, period_factor=None):
    """
    inflow: array (year, product, material) over the years from START_YEAR
    on: YEARS, or YEARS followed by the years of the future module (D12);
    stock: 'US.HH' or 'US.IC', which selects the lifetimes. Returns
    {'outflow', 'stock'} as arrays (year, product, material) over the same
    years, and 'stock_1987' as an array (product, material).

    cohort_factor (array (year, product) over the same years as inflow)
    multiplies the mean lifetime of each cohort, for lifetimes that change
    in the future module (phase D, X4b); None keeps the lifetimes of the
    parameters for every cohort. period_factor (same shape) multiplies the
    lifetime of all cohorts in use in a year (survival); None means none.
    """
    if period_factor is not None:
        return _cohorts_from_survival(inflow, products, current_params, stock, cohort_factor, period_factor)
    dsm_years = list(range(SPINUP_START, START_YEAR + inflow.shape[0]))
    spinup = inflow[:1] * current_params['spinup_inflow_factor']
    inflow = np.concatenate([np.repeat(spinup, N_SPINUP, axis=0), inflow], axis=0)
    dims = fd.DimensionSet(dim_list=[
        fd.Dimension(letter='t', name='Time', dtype=int, items=dsm_years),
        fd.Dimension(letter='p', name='Product', dtype=str, items=products),
        fd.Dimension(letter='m', name='Material', dtype=int, items=list(range(inflow.shape[2]))),
    ])
    lifetime = _weibull(dims, products, current_params, stock, cohort_factor)
    dsm = fd.InflowDrivenDSM(name=f'{stock} cohorts', dims=dims, lifetime_model=lifetime,
                             inflow=fd.StockArray(dims=dims, values=inflow))
    dsm.compute()
    return {
        'outflow': dsm.outflow.values[N_SPINUP:],
        'stock': dsm.stock.values[N_SPINUP:],
        'stock_1987': dsm.stock.values[N_SPINUP - 1],
    }


def _cohorts_from_survival(inflow, products, current_params, stock, cohort_factor, period_factor):
    """use_cohorts with a period effect on the lifetimes, from the survival factors of survival()."""
    sf = survival(inflow.shape[0], products, current_params, stock, cohort_factor, period_factor)
    spinup = inflow[:1] * current_params['spinup_inflow_factor']
    full = np.concatenate([np.repeat(spinup, N_SPINUP, axis=0), inflow], axis=0)
    stock_all = np.einsum('tcp,cpm->tpm', sf, full)
    outflow = full - np.diff(np.concatenate([np.zeros_like(stock_all[:1]), stock_all]), axis=0)
    return {
        'outflow': outflow[N_SPINUP:],
        'stock': stock_all[N_SPINUP:],
        'stock_1987': stock_all[N_SPINUP - 1],
    }


def competing_survival(n_years, technical, perceived, technical_shape, perceived_shape, technical_factor=None,
                       perceived_factor=None, period_factor=None):
    """
    Survival of cohorts with two competing reasons to discard, technical
    (worn out, damaged) and perceived (no longer wanted), each Weibull, over
    the spin-up years and n_years from START_YEAR. technical and perceived
    are the scales per unit (array (unit,); perceived may be infinite);
    technical_factor and perceived_factor (arrays (year, unit) over n_years)
    multiply the scales of each cohort, and period_factor multiplies the
    technical scale of all cohorts in a year (repair). Inflow arrives in the
    middle of the year. Returns (sf, technical share): sf (year, cohort,
    unit) is the share of a cohort still in use at the end of a year, and
    technical share (year, cohort, unit) the share of the goods leaving in
    that year that leave for technical reasons.
    """
    n = N_SPINUP + n_years
    units = len(technical)

    def full(factor):
        if factor is None:
            return np.ones((n, units))
        return np.concatenate([np.ones((N_SPINUP, units)), factor], axis=0)

    lam_t = technical[None, :] * full(technical_factor)
    lam_p = perceived[None, :] * full(perceived_factor)
    period = full(period_factor)
    sf = np.zeros((n, n, units))
    share = np.zeros((n, n, units))
    for t in range(n):
        age = (t - np.arange(t + 1) + 0.5)[:, None]
        before = np.clip(age - 1.0, 0.0, None)
        lt = lam_t[:t + 1] * period[t][None, :]
        d_tech = (age / lt) ** technical_shape - (before / lt) ** technical_shape
        d_perc = (age / lam_p[:t + 1]) ** perceived_shape - (before / lam_p[:t + 1]) ** perceived_shape
        previous = np.ones((t + 1, units))
        if t > 0:
            previous[:t] = sf[t - 1, :t]
        sf[t, :t + 1] = previous * np.exp(-d_tech - d_perc)
        share[t, :t + 1] = d_tech / (d_tech + d_perc)
    return sf, share


def unit_cohorts(inflow, sf, technical_share, repairable, spinup_inflow_factor):
    """
    Stock and outflow of cohorts from survival factors (competing_survival).
    inflow: array (year, unit, material) over the years from START_YEAR.
    Returns {'outflow', 'stock', 'broken'} as arrays (year, unit, material)
    over the same years, with 'broken' the outflow damaged beyond easy
    repair (technical outflow times one minus the repairable share per
    unit), and 'stock_1987' as an array (unit, material).
    """
    spinup = inflow[:1] * spinup_inflow_factor
    full = np.concatenate([np.repeat(spinup, N_SPINUP, axis=0), inflow], axis=0)
    previous = np.concatenate([np.ones((1,) + sf.shape[1:]), sf[:-1]], axis=0)
    # A cohort enters during its year, so before that year nothing of it is
    # in use and nothing leaves.
    entered = np.tril(np.ones(sf.shape[:2]))[:, :, None]
    leaving = np.clip(previous * entered - sf, 0.0, None) * entered
    leaving[np.arange(sf.shape[0]), np.arange(sf.shape[0])] = 1.0 - sf[np.arange(sf.shape[0]), np.arange(sf.shape[0])]
    stock = np.einsum('tcu,cum->tum', sf, full)
    outflow = np.einsum('tcu,cum->tum', leaving, full)
    broken = np.einsum('tcu,cum->tum', leaving * technical_share * (1.0 - repairable)[None, None, :], full)
    return {'outflow': outflow[N_SPINUP:], 'stock': stock[N_SPINUP:], 'broken': broken[N_SPINUP:],
            'stock_1987': stock[N_SPINUP - 1]}
