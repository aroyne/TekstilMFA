import numpy as np
import pytest

from calculations.stock_model import survival_curve, inflow_driven


@pytest.mark.parametrize('dist,shape', [('weibull', 2.0), ('lognormal', 0.5)])
def test_mass_balance(dist, shape):
    rng = np.random.default_rng(0)
    inflows = rng.uniform(50, 150, size=40)
    surv = survival_curve(dist, mean_years=5.0, shape=shape, n_ages=200)
    stock, outflow, dstock = inflow_driven(inflows, surv)
    np.testing.assert_allclose(dstock, inflows - outflow, atol=1e-9)


def test_steady_state_stock_equals_inflow_times_mean_lifetime():
    # With constant inflow the stock approaches inflow * sum_{a>=1} S(a),
    # which is close to inflow * mean lifetime for a smooth distribution.
    surv = survival_curve('weibull', mean_years=6.0, shape=2.0, n_ages=300)
    stock, outflow, _ = inflow_driven(np.full(200, 10.0), surv)
    assert outflow[-1] == pytest.approx(10.0, rel=1e-6)
    assert stock[-1] == pytest.approx(10.0 * surv[1:].sum(), rel=1e-6)
    assert stock[-1] == pytest.approx(60.0, rel=0.1)


def test_immediate_lifetime_has_no_stock():
    inflows = np.array([3.0, 5.0, 4.0])
    surv = survival_curve('immediate', mean_years=None, shape=None, n_ages=10)
    stock, outflow, _ = inflow_driven(inflows, surv)
    np.testing.assert_allclose(stock, 0.0)
    np.testing.assert_allclose(outflow, inflows)
