#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turns anchor points ({year: value}) into annual series. Values are linearly
interpolated between anchors and held constant before the first and after
the last anchor. Regime shifts (e.g. the 2009 landfill ban) are expressed by
placing two anchors in adjacent years rather than by special-casing here.

Years without published values are less certain than the anchors (D30,
revised in phase A). GapNoise adds a multiplicative, lognormal factor with
median 1 (so the central value stays at what the data say). Its upper 95 %
bound is 1 + u(d), with u(d) = u0 + k * d growing with the distance d to the
nearest anchor, as in the fill uncertainties of NitrogenBudsjett:
interpolation between anchors (u0 5 %, k 2 % per year) and values held flat
before the first or after the last anchor (u0 10 %, k 5 % per year). One
standard normal draw per series and gap (or side) is used for all years in
it, so the error is systematic within a gap: the filled period gets an
uncertain level and trend, not noise from year to year.
"""
import numpy as np

from calculations.sampling import Z95, normal_score
from calculations.utils import YEARS

class GapNoise:
    """
    Gap factors for one MC iteration; all factors are 1 in the deterministic
    run unless a probe (sampling.Probe) sets one gap.
    """

    def __init__(self, seed, sim_id, fill, probe=None):
        """fill: {'interpolation': (u0, k), 'carry': (u0, k)}, u as a fraction of the value."""
        self.seed = seed
        self.sim_id = sim_id
        self.probe = probe
        self.deterministic = sim_id == 0 and probe is None
        self.fill = fill
        self._z = {}

    def _draw(self, name, segment):
        key = (name, segment)
        if key not in self._z:
            self._z[key] = normal_score(self.seed, self.sim_id, 'gap', f'{name}:{segment}', self.probe)
        return self._z[key]

    def factor(self, name, anchor_years, years=YEARS):
        """Array of factors, one per year, for the series name with anchors in anchor_years."""
        if self.deterministic:
            return np.ones(len(years))
        anchor_years = sorted(anchor_years)
        factors = np.ones(len(years))
        for i, year in enumerate(years):
            if year < anchor_years[0]:
                kind, d, segment = 'carry', anchor_years[0] - year, 'before'
            elif year > anchor_years[-1]:
                kind, d, segment = 'carry', year - anchor_years[-1], 'after'
            elif year in anchor_years:
                continue
            else:
                after = next(a for a in anchor_years if a > year)
                before = max(a for a in anchor_years if a < year)
                kind, d, segment = 'interpolation', min(year - before, after - year), (before, after)
            u0, k = self.fill[kind]
            sigma = np.log(1.0 + u0 + k * d) / Z95
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
