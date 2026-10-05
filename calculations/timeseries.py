#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turns anchor points ({year: value}) into annual series. Values are linearly
interpolated between anchors and held constant before the first and after
the last anchor. Regime shifts (e.g. the 2009 landfill ban) are expressed by
placing two anchors in adjacent years rather than by special-casing here.
"""
import numpy as np

from calculations.utils import YEARS


def interpolate(anchors, years=YEARS):
    """Returns an array with one value per year in years."""
    anchor_years = np.array(sorted(anchors), dtype=float)
    anchor_values = np.array([anchors[y] for y in sorted(anchors)], dtype=float)
    return np.interp(np.array(years, dtype=float), anchor_years, anchor_values)
