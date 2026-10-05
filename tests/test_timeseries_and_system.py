import numpy as np
import pytest

from calculations.params import Parameters
from calculations.system import close, make_system, stock_change
from calculations.timeseries import interpolate
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
    inflow = sum(mfa.flows[code].values[:, :3].sum(axis=1) for code in (
        'DI.RT-US.HH-Sales to households-TOT', 'RW.RW-US.HH-Private imports-TOT',
        'RW.RW-US.HH-Direct online imports-TOT'))
    inflow = inflow + mfa.flows['CO.RE-US.HH-Secondhand sales to households-TOT'].values[:, core]
    discards = (mfa.flows['US.HH-CO.CO-Separate collection from households-TOT'].values[:, core]
                + mfa.flows['US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT'].values[:, core]
                + mfa.flows['US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT'].values[:, core])
    np.testing.assert_allclose(stock_change(mfa, 'US.HH').values[:, core], inflow - discards)
