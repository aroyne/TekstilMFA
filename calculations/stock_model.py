#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inflow-driven dynamic stock model for textiles in use. Each year's inflow is
a cohort that leaves the stock according to a lifetime distribution; the
outflow in year t is the sum over all earlier cohorts of the share that
reaches end of use at that age.

Discrete convention: S(a) is the share of a cohort still in the stock a
years after entering. A cohort enters during year c, so at the end of year c
the share S(1) remains and the share 1 - S(1) has already left. This makes
stock(t) - stock(t-1) = inflow(t) - outflow(t) hold exactly.
"""
import math
import numpy as np


def survival_curve(distribution_type, mean_years, shape, n_ages):
    """
    Returns S(a) for a = 0 .. n_ages, with S(0) = 1.

    weibull:   shape is the Weibull shape parameter k; the scale follows from
               the mean as mean / Gamma(1 + 1/k).
    lognormal: shape is the standard deviation of log(lifetime).
    immediate: everything leaves in the year it enters (no stock); used for
               products treated as packaging. mean_years and shape are ignored.
    """
    ages = np.arange(n_ages + 1, dtype=float)
    dist = distribution_type.lower().strip()

    if dist == 'immediate':
        return (ages == 0).astype(float)

    if dist == 'weibull':
        scale = mean_years / math.gamma(1.0 + 1.0 / shape)
        return np.exp(-(ages / scale) ** shape)

    if dist == 'lognormal':
        mu = math.log(mean_years) - shape ** 2 / 2.0
        surv = np.ones_like(ages)
        pos = ages > 0
        z = (np.log(ages[pos]) - mu) / (shape * math.sqrt(2.0))
        surv[pos] = 0.5 * (1.0 - np.vectorize(math.erf)(z))
        return surv

    raise ValueError(f"Unknown lifetime distribution '{distribution_type}'")


def inflow_driven(inflows, survival):
    """
    Runs the inflow-driven model.

    inflows  : 1D array, one value per year (first element is the first
               model year, including any spin-up years).
    survival : S(a) from survival_curve; must cover at least len(inflows)
               ages, otherwise the oldest cohorts never fully leave.

    Returns (stock, outflow, stock_change) as 1D arrays of the same length.
    """
    inflows = np.asarray(inflows, dtype=float)
    n = len(inflows)
    if len(survival) < n + 1:
        raise ValueError("survival curve is shorter than the time series")

    # Probability of leaving at age a (0-based): S(a) - S(a+1).
    leave_prob = survival[:-1] - survival[1:]

    stock = np.zeros(n)
    outflow = np.zeros(n)
    for t in range(n):
        ages = t - np.arange(t + 1)            # age of each cohort 0..t in year t
        cohorts = inflows[:t + 1]
        outflow[t] = np.sum(cohorts * leave_prob[ages])
        stock[t] = np.sum(cohorts * survival[ages + 1])

    stock_change = np.diff(stock, prepend=0.0)
    return stock, outflow, stock_change
