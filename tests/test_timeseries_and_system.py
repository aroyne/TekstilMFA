import numpy as np
import pytest

from calculations.params import Parameters
from calculations.system import close, make_system, stock_change
from calculations.timeseries import interpolate
from calculations.utils import CORE_GROUP_PRODUCTS, PRODUCTS
from data_loader import load_all_data
from main_mc import ALL_POOLS, run_pools


def test_interpolate_linear_between_and_constant_outside():
    series = interpolate({2000: 0.0, 2010: 10.0}, range(1995, 2016))
    assert series[0] == 0.0
    assert series[10] == pytest.approx(5.0)
    assert series[-1] == 10.0


@pytest.fixture(scope='module')
def inputs():
    params = Parameters()
    preloaded_data = load_all_data(ALL_POOLS, params)
    return (preloaded_data,) + params.draw(np.random.default_rng(0), deterministic=True)


def _run(inputs, pools=ALL_POOLS):
    preloaded_data, current_params, dataset_noise, anchors = inputs
    mfa = make_system()
    run_pools(mfa, pools, preloaded_data, current_params, dataset_noise, anchors)
    return mfa


def test_baseline_closes(inputs):
    close(_run(inputs))


def test_unassigned_flow_fails(inputs):
    mfa = _run(inputs, pools=ALL_POOLS[:-1])
    with pytest.raises(ValueError, match='NaN'):
        close(mfa)


def test_imbalance_fails(inputs):
    mfa = _run(inputs)
    mfa.flows['CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT'].values[10, 0] += 1.0
    with pytest.raises(ValueError, match='CO.RE'):
        close(mfa)


def test_household_stock_change_is_inflow_minus_discards(inputs):
    mfa = _run(inputs)
    close(mfa)
    core = 0
    core_products = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    inflow = sum(mfa.flows[code].values[:, core_products].sum(axis=1) for code in (
        'DI.RT-US.HH-Sales to households-TOT', 'RW.RW-US.HH-Private imports-TOT',
        'RW.RW-US.HH-Direct online imports-TOT'))
    inflow = inflow + mfa.flows['CO.RE-US.HH-Secondhand sales to households-TOT'].values[:, core]
    discards = (mfa.flows['US.HH-CO.CO-Separate collection from households-TOT'].values[:, core]
                + mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values[:, core]
                + mfa.flows['US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT'].values[:, core]
                + mfa.flows['US.HH-WM.WW-Fibre release in laundry-TOT'].values[:, core]
                + mfa.flows['US.HH-EN.AI-Fibre release to air and dust-TOT'].values[:, core])
    np.testing.assert_allclose(stock_change(mfa, 'US.HH').values[:, core], inflow - discards)


@pytest.fixture(scope='module')
def fibre_run(inputs):
    from calculations.fibre_layer import compute_fibre_layer
    from calculations.params import Parameters
    tot = _run(inputs)
    close(tot)
    fibre = make_system(fibre=True)
    preloaded_data, current_params, _, _ = inputs
    compute_fibre_layer(fibre, tot, preloaded_data, current_params, Parameters().fibre_composition)
    return tot, fibre, current_params


def test_fibre_layer_adds_up_to_tot(fibre_run):
    # A flow clipped per material in the fibre layer exceeds TOT by exactly
    # the mass clipped there.
    tot, fibre, _ = fibre_run
    for code, flow in tot.flows.items():
        # A flow clipped again per material in the fibre layer sums to its
        # unclipped TOT balance plus the mass clipped in the fibre layer.
        own = code in fibre.clipped and fibre.clipped[code] is not tot.clipped.get(code)
        extra = 0.0
        if own:
            extra = fibre.clipped[code].values.sum(axis=-1)
            if code in tot.clipped:
                extra = extra - tot.clipped[code].values
        np.testing.assert_allclose(fibre.flows[code].values.sum(axis=-1) - extra, flow.values, atol=1e-9)


def test_footwear_supply_has_the_non_textile_share(fibre_run):
    from calculations.utils import MATERIALS, PRODUCTS
    _, fibre, current_params = fibre_run
    sales = fibre.flows['DI.RT-US.HH-Sales to households-TOT'].values[:, PRODUCTS.index('FW'), :]
    np.testing.assert_allclose(sales[:, MATERIALS.index('NT')] / sales.sum(axis=1),
                               current_params['nontextile_share_FW'])


def test_every_product_has_imports_every_year(inputs):
    preloaded_data = inputs[0]
    assert (preloaded_data['imports_by_fibre_class'].sum(axis=2) > 0).all()


def test_gap_noise_grows_with_distance_and_is_one_at_anchors():
    from calculations.timeseries import GapNoise
    years = list(range(1988, 2026))
    anchors = [2010, 2020]
    assert (GapNoise(np.random.default_rng(0), True, 0.02, 0.05, 1.0).factor('x', anchors, years) == 1).all()
    draws = np.array([GapNoise(np.random.default_rng(i), False, 0.02, 0.05, 1.0).factor('x', anchors, years)
                      for i in range(2000)])
    spread = draws.std(axis=0)
    at = [years.index(a) for a in anchors]
    assert (spread[at] == 0).all()
    assert spread[years.index(1990)] > spread[years.index(2005)] > spread[years.index(2009)]
    assert spread[years.index(2015)] > spread[years.index(2012)]
    assert abs(np.median(draws, axis=0)[years.index(2015)] - 1) < 0.02
