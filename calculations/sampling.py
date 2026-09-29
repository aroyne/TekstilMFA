#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte Carlo draws for single parameters. Uses the same conventions as the
NitrogenBudsjett model (lower/upper bounds, 'perc' or 'abs' uncertainty type,
PERT/lognormal/normal distributions), so that parameter tables can be read
the same way in both projects.
"""
import numpy as np
import pandas as pd


def draw_from_pert(rng, low, likely, high):
    """Draws one sample from a PERT distribution."""
    range_val = high - low
    if range_val == 0:
        return likely
    alpha = 1 + 4 * (likely - low) / range_val
    beta = 1 + 4 * (high - likely) / range_val
    return low + rng.beta(alpha, beta) * range_val


def draw_perturbed_value(rng, val, low_b, upp_b, unc_type, dist_type):
    """
    Draws one perturbed value for a parameter given its base value,
    uncertainty bounds and distribution type.

    A blank (NaN) low_b/upp_b, or low_b == upp_b == 0, means the parameter is
    not perturbed and val is returned unchanged.

    For unc_type == 'perc', low_b/upp_b are +/- percentages of val. For
    'abs', low_b/upp_b are absolute bounds on the drawn value, not offsets.
    """
    if pd.isna(low_b) or pd.isna(upp_b) or (low_b == 0 and upp_b == 0):
        return val

    low_b = float(low_b)
    upp_b = float(upp_b)
    unc_type = str(unc_type).lower().strip()
    dist_type = str(dist_type).lower().strip()

    if unc_type == 'perc':
        abs_min = val * (1 - low_b / 100.0)
        abs_max = val * (1 + upp_b / 100.0)
        std_dev = ((low_b + upp_b) / 2.0 / 100.0) * val
    else:
        abs_min = low_b
        abs_max = upp_b
        std_dev = (upp_b - low_b) / 2.0 / 1.96

    if 'pert' in dist_type:
        chosen_val = draw_from_pert(rng, abs_min, val, abs_max)
    elif 'log' in dist_type:
        cv = std_dev / val
        sigma_log = np.sqrt(np.log(1 + cv**2))
        mu_log = np.log(val) - (sigma_log ** 2) / 2
        chosen_val = rng.lognormal(mu_log, sigma_log)
    else:
        chosen_val = rng.normal(val, std_dev)

    # A negative mass or share has no physical meaning.
    if val >= 0 and chosen_val < 0:
        chosen_val = 0.0

    return chosen_val
