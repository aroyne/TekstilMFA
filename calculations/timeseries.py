#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turns anchor points ({year: value}) into annual series. Values are linearly
interpolated between anchors and held constant before the first and after
the last anchor. Regime shifts (e.g. the 2009 landfill ban) are expressed by
placing two anchors in adjacent years rather than by special-casing here.

Years without published values are less certain than the anchors (D30).
GapNoise adds a multiplicative, lognormal factor with median 1 (so the
central value stays at what the data say) whose coefficient of variation
grows with the distance to the nearest anchor:
r_interp per year inside a gap (zero at the anchors, largest mid-way) and
r_extrap per year outside the anchors, capped. One standard normal draw per
series and gap (or side) is used for all years in it, so the error is
systematic within a gap rather than jumping from year to year. The draw is
limited to two standard deviations: a lognormal factor with a coefficient
of variation of 100 % would otherwise reach more than ten times the median
in one draw of a thousand, which no extrapolation supports.
"""
import numpy as np

from calculations.utils import YEARS

MAX_Z = 2.0


class GapNoise:
    """Gap factors for one MC iteration; all factors are 1 in the deterministic run."""

    def __init__(self, rng, deterministic, r_interp, r_extrap, cap):
        self.rng = rng
        self.deterministic = deterministic
        self.r_interp = r_interp
        self.r_extrap = r_extrap
        self.cap = cap
        self._z = {}

    def _draw(self, name, segment):
        key = (name, segment)
        if key not in self._z:
            self._z[key] = float(np.clip(self.rng.standard_normal(), -MAX_Z, MAX_Z))
        return self._z[key]

    def factor(self, name, anchor_years, years=YEARS):
        """Array of factors, one per year, for the series name with anchors in anchor_years."""
        if self.deterministic:
            return np.ones(len(years))
        anchor_years = sorted(anchor_years)
        factors = np.ones(len(years))
        for i, year in enumerate(years):
            if year < anchor_years[0]:
                cv, segment = min(self.r_extrap * (anchor_years[0] - year), self.cap), 'before'
            elif year > anchor_years[-1]:
                cv, segment = min(self.r_extrap * (year - anchor_years[-1]), self.cap), 'after'
            elif year in anchor_years:
                continue
            else:
                after = next(a for a in anchor_years if a > year)
                before = max(a for a in anchor_years if a < year)
                cv, segment = min(self.r_interp * min(year - before, after - year), self.cap), (before, after)
            sigma = np.sqrt(np.log(1.0 + cv ** 2))
            factors[i] = np.exp(sigma * self._draw(name, segment))
        return factors


class AnchorSeries(dict):
    """Anchor points {year: value} of one parameter, with the gap noise of the iteration."""

    def __init__(self, name, points, gap_noise):
        super().__init__(points)
        self.name = name
        self.gap_noise = gap_noise


def interpolate(points, years=YEARS, noise=None, upper=None):
    """
    Returns an array with one value per year in years. noise is the
    AnchorSeries whose gap noise applies (by default points itself, if it
    is one); a series derived from anchors (e.g. a ratio) passes the
    anchors it was derived from. upper caps the values (1 for shares).
    """
    anchor_years = np.array(sorted(points), dtype=float)
    anchor_values = np.array([points[y] for y in sorted(points)], dtype=float)
    values = np.interp(np.array(years, dtype=float), anchor_years, anchor_values)
    noise = points if noise is None and isinstance(points, AnchorSeries) else noise
    if noise is not None:
        values = values * noise.gap_noise.factor(noise.name, list(points), years)
    if upper is not None:
        # A drawn share above 1 has no physical meaning.
        values = np.minimum(values, upper)
    return values
