#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turns anchor points ({year: value}) into annual series. Values are linearly
interpolated between anchors and held constant before the first and after
the last anchor. Regime shifts (e.g. the 2009 landfill ban) are expressed by
placing two anchors in adjacent years rather than by special-casing here.
"""
import numpy as np


def interpolate(anchors, years):
    """Returns {year: value} for every year in years."""
    anchor_years = np.array(sorted(anchors), dtype=float)
    anchor_values = np.array([anchors[y] for y in sorted(anchors)], dtype=float)
    values = np.interp(np.array(sorted(years), dtype=float), anchor_years, anchor_values)
    return dict(zip(sorted(years), values))
