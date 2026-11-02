#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte Carlo draws for single uncertain inputs (D39).

Every input is drawn through its quantile function: a uniform number u in
(0, 1) from the item's own random-number stream is mapped to a value. The
same function gives the 2.5th and 97.5th percentiles that the contribution
analysis sets one source at a time, and a correlated draw for anchor points
that share a method (a standard normal mixed from a common and an own part).

Bounds (lower_bound, upper_bound) are a 95 % interval (2.5th and 97.5th
percentiles) unless the row says bounds = 'minmax'. For unc_type 'perc' they
are percentages of the base value below and above it, for 'abs' absolute
values. The distribution follows how the bounds are given (the rule from
NitrogenBudsjett):
- normal: symmetric bounds up to +/-40 %, truncated at 0,
- lognormal: bounds symmetric in log space (an uncertainty factor),
- triangular: wider or asymmetric bounds, and quantities with a hard bound
  at 0 or 1 (then marked minmax),
- uniform: source type 4 (expert estimate or assumption), with the bounds
  as the lowest and highest plausible value. A mode would claim knowledge
  of where in the range the value lies that such a source does not give
  (Weijenberg et al. 2026).
"""
import zlib

import numpy as np
import pandas as pd
from scipy import stats

DEFAULT_SEED = 1
Z95 = stats.norm.ppf(0.975)


def item_rng(seed, sim_id, group, item_id):
    """
    Random-number stream for one item in one iteration, fixed by the master
    seed, the iteration and (group, item_id). Adding, removing or reordering
    items therefore leaves the draws of every other item unchanged.
    """
    key = zlib.crc32(f"{group}:{item_id}".encode('utf-8'))
    return np.random.default_rng(np.random.SeedSequence(seed, spawn_key=(key, sim_id)))


class Probe:
    """
    One uncertainty source set to a fixed standard-normal score z in an
    otherwise deterministic run (iteration 0), for the contribution analysis.
    Every source the model asks for is recorded in `requested`, so a probe
    without a target traces which sources a run uses.
    """

    def __init__(self, group=None, item_id=None, z=0.0):
        self.target = (group, item_id)
        self.z_value = z
        self.requested = set()

    def z(self, group, item_id):
        self.requested.add((group, item_id))
        return self.z_value if (group, item_id) == self.target else 0.0


def normal_score(seed, sim_id, group, item_id, probe=None):
    """
    Standard-normal score of one item: drawn from the item's own stream in
    iterations 1..n; 0 in the deterministic iteration, or the probe's value
    for the probed item.
    """
    if sim_id == 0:
        return probe.z(group, item_id) if probe is not None else 0.0
    return float(stats.norm.ppf(item_rng(seed, sim_id, group, item_id).random()))


def is_perturbed(row):
    """A row is perturbed unless its distribution is 'none'; a perturbed row without bounds is an error."""
    dist = str(row['distribution_type']).strip().lower()
    if dist == 'none':
        return False
    if pd.isna(row['lower_bound']) or pd.isna(row['upper_bound']):
        raise ValueError(f"{row.name}: distribution {dist} without bounds")
    return True


def absolute_bounds(val, row):
    """(low, high) in the unit of the value."""
    low, high = float(row['lower_bound']), float(row['upper_bound'])
    if str(row['uncertainty_type']).strip().lower() == 'perc':
        return val * (1 - low / 100.0), val * (1 + high / 100.0)
    return low, high


def _triangular_quantiles(t):
    """2.5th and 97.5th percentiles of a triangular distribution on [0, 1] with its mode at t."""
    def q(p):
        return np.sqrt(p * t) if p < t else 1 - np.sqrt((1 - p) * (1 - t))
    return q(0.025), q(0.975)


def triangular_minmax_from_95(mode, lo, hi):
    """
    Minimum and maximum of the triangular distribution with the given mode
    whose 2.5th and 97.5th percentiles are lo and hi: the relative position
    of the mode t is found by bisection on the ratio of the two distances
    to the mode, and the width follows from lo.
    """
    target = (mode - lo) / (hi - lo)

    def position(t):
        q_lo, q_hi = _triangular_quantiles(t)
        return (t - q_lo) / (q_hi - q_lo)

    a, b = 1e-9, 1 - 1e-9
    for _ in range(80):
        m = (a + b) / 2
        if position(m) < target:
            a = m
        else:
            b = m
    t = (a + b) / 2
    q_lo, q_hi = _triangular_quantiles(t)
    width = (hi - lo) / (q_hi - q_lo)
    minimum = lo - q_lo * width
    return minimum, minimum + width


def quantile(u, val, row):
    """Value of the row's distribution at cumulative probability u."""
    dist = str(row['distribution_type']).strip().lower()
    minmax = str(row.get('bounds', '')).strip().lower() == 'minmax'
    low, high = absolute_bounds(val, row)
    if low == high:
        return val
    if dist == 'normal':
        sd = (high - low) / 2 / Z95
        # Truncated at 0: a negative mass or share has no physical meaning.
        p0 = stats.norm.cdf(0.0, val, sd)
        return float(stats.norm.ppf(p0 + u * (1 - p0), val, sd))
    if dist == 'lognormal':
        # The base value is the median; the bounds set the spread in log space.
        sigma = np.log(high / low) / 2 / Z95
        return float(val * np.exp(sigma * stats.norm.ppf(u)))
    if dist == 'triangular':
        a, b = (low, high) if minmax else triangular_minmax_from_95(val, low, high)
        return float(stats.triang.ppf(u, (val - a) / (b - a), loc=a, scale=b - a))
    if dist == 'uniform':
        if not minmax:
            width = (high - low) / 0.95
            low, high = low - 0.025 * width, high + 0.025 * width
        return float(low + u * (high - low))
    raise ValueError(f"unknown distribution '{dist}'")
