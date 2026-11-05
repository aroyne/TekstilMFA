import math

import numpy as np
import pytest

from calculations.categories import (CATEGORIES, UNITS, _MEAN, _RATIOS, _WEAR, category_of, category_shares,
                                     unit_lifetimes)
from calculations.cohorts import competing_survival, unit_cohorts, use_cohorts
from calculations.params import Parameters
from data_loader import load_all_data


@pytest.fixture(scope='module')
def data():
    params = Parameters()
    return params, load_all_data(['rw'], params)


def test_every_clothing_and_footwear_code_has_one_category(data):
    _, preloaded = data
    trade = preloaded['trade_textiles']
    codes = trade[(trade['category'] == 'finished') & trade['product'].isin(CATEGORIES)]
    for product, hs8 in codes[['product', 'HS8']].drop_duplicates().itertuples(index=False):
        assert category_of(product, hs8) in CATEGORIES[product]


def test_category_shares_sum_to_one(data):
    _, preloaded = data
    for shares in category_shares(preloaded['trade_textiles']).values():
        np.testing.assert_allclose(shares.sum(axis=1), 1.0)


def test_unit_lifetimes_keep_the_product_mean_and_wear_share(data):
    params, preloaded = data
    current, _, _ = params.draw(1, 0)
    shares = {p: s[-1] for p, s in category_shares(preloaded['trade_textiles']).items()}
    technical, perceived, repairable = unit_lifetimes(current, shares)
    for product, categories in CATEGORIES.items():
        means, wears = [], []
        for c in categories:
            u = UNITS.index(c)
            ratio = perceived[u] / technical[u]
            means.append(technical[u] * np.interp(ratio, _RATIOS, _MEAN))
            wears.append(np.interp(ratio, _RATIOS, _WEAR))
            assert wears[-1] == pytest.approx(current[f'broken_share_{c}'] / (1 - current[f'repairable_share_{c}']),
                                              rel=1e-3)
        assert np.dot(shares[product], means) == pytest.approx(current[f'lifetime_mean_US.HH_{product}'], rel=1e-3)


def test_competing_survival_without_perceived_lifetime_is_weibull():
    params = {'spinup_inflow_factor': 1.0, 'lifetime_shape_US.HH_CL': 2.0, 'lifetime_mean_US.HH_CL': 6.0}
    n = 63
    sf, share = competing_survival(n, np.array([6.0 / math.gamma(1.5)]), np.array([np.inf]), 2.0, 1.5)
    inflow = np.random.default_rng(3).uniform(1, 2, (n, 1, 2))
    a = use_cohorts(inflow, ['CL'], params)
    b = unit_cohorts(inflow, sf, share, np.array([0.0]), 1.0)
    np.testing.assert_allclose(b['stock'], a['stock'], atol=1e-10)
    np.testing.assert_allclose(b['outflow'], a['outflow'], atol=1e-10)
