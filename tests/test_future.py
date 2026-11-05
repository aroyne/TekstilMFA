import numpy as np
import pytest

from calculations.future import BASE, FUTURE_YEARS
from calculations.utils import PRODUCT_GROUPS
from main_future import run_reference

CORE = PRODUCT_GROUPS.index('CORE')
DISCARDS = ['US.HH-CO.CO-Separate collection from households-TOT',
            'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
            'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT']


@pytest.fixture(scope='module')
def reference():
    return run_reference()


def test_future_closes_and_covers_horizon(reference):
    _, fut, _, _, _ = reference
    assert list(fut.dims['t'].items) == FUTURE_YEARS


def test_scaled_discards_continue_from_2025(reference):
    hist, fut, ref, _, _ = reference
    discards_2025 = sum(hist.flows[c].values[BASE, CORE] for c in DISCARDS)
    discards_2026 = sum(fut.flows[c].values[0, CORE] for c in DISCARDS)
    assert ref.scale * ref.cohorts['outflow'][BASE] == pytest.approx(discards_2025)
    assert discards_2026 == pytest.approx(discards_2025, rel=0.03)


def test_supply_per_inhabitant_is_held(reference):
    hist, fut, ref, _, _ = reference
    code = 'DI.RT-US.HH-Sales to households-TOT'
    np.testing.assert_allclose(fut.flows[code].values / ref.growth[:, None], np.repeat(
        hist.flows[code].values[BASE][None], len(FUTURE_YEARS), axis=0))


def test_no_clipping_in_reference(reference):
    _, fut, _, _, _ = reference
    assert all(np.abs(c.values).max() == 0.0 for c in fut.clipped.values())


def test_fibre_layer_adds_up_and_continues(reference):
    hist, fut, _, _, layers = reference
    fibre, stock_model = layers['future']
    for code, flow in fut.flows.items():
        np.testing.assert_allclose(fibre.flows[code].values.sum(axis=-1), flow.values, atol=1e-6)
    _, hist_stock = layers['history']
    level = 'US.HH-US.HH-Stock-TOT'
    gap = stock_model[level].values[0].sum() - hist_stock[level].values[-1].sum()
    change = fut.stocks['US.HH'].inflow.values[0, CORE] - fut.stocks['US.HH'].outflow.values[0, CORE]
    assert gap == pytest.approx(change)


def test_household_stock_grows_by_the_set_amount(reference):
    _, fut, ref, _, _ = reference
    change = fut.stocks['US.HH'].inflow.values[:, CORE] - fut.stocks['US.HH'].outflow.values[:, CORE]
    np.testing.assert_allclose(change, ref.current_params['future_stock_growth_kg_per_capita']
                               * ref.population / 1e6)


def test_scenarios_are_reproducible_and_within_bounds():
    from calculations.future_scenarios import CONTINUOUS, SORTING_BOUNDS, sample_scenarios
    first, second = sample_scenarios(50), sample_scenarios(50)
    assert first == second
    for scenario in first:
        for name, low, high in CONTINUOUS:
            assert low <= getattr(scenario, name) <= high
        assert sum(scenario.sorting_outcome_2035) == pytest.approx(1.0)
        assert all(lo <= x <= hi for x, (lo, hi) in zip(scenario.sorting_outcome_2035, SORTING_BOUNDS))
    assert {s.population for s in first} == {'LLL', 'MMM', 'HHH'}


def test_sampled_scenarios_close_with_fibre_layer():
    from calculations.future_scenarios import sample_scenarios
    from main_future import prepare_history, run_future
    history = prepare_history()
    for scenario in sample_scenarios(20):
        run_future(history, scenario)


def test_policies_act_where_they_should():
    from calculations.future import FUTURE_YEARS, Scenario
    from calculations.future_policies import policy, sample_effects
    from main_future import prepare_history, run_future
    history = prepare_history()
    scenario = Scenario.reference(history['hist'])
    effects = sample_effects(1)[0]
    base, _, _ = run_future(history, scenario, fibre=False)
    i2032 = FUTURE_YEARS.index(2032)
    l2, _, _ = run_future(history, scenario, policy('L2', effects), fibre=False)
    assert l2.flows['CO.CO-RW.RW-Export of unsorted collected textiles-TOT'].values[i2032:].max() == pytest.approx(0)
    l4, _, _ = run_future(history, scenario, policy('L4', effects), fibre=False)
    assert l4.flows['DI.RT-WM.RS-Unsold goods discarded-TOT'].values[FUTURE_YEARS.index(2030):].max() == 0
    l1, _, _ = run_future(history, scenario, policy('L1', effects), fibre=False)
    code = 'US.HH-CO.CO-Separate collection from households-TOT'
    assert (l1.flows[code].values[i2032:, CORE] > base.flows[code].values[i2032:, CORE]).all()
    l0, _, _ = run_future(history, scenario, policy('L0', effects), fibre=False)
    for name, flow in base.flows.items():
        np.testing.assert_array_equal(l0.flows[name].values, flow.values)
    run_future(history, scenario, policy('Lall', effects))


def test_stock_driven_demand_starts_at_2025_level_and_responds_to_lifetimes():
    import dataclasses
    from calculations.fibre_layer import new_goods_to_households
    from calculations.future import FUTURE_YEARS, Policy, Scenario
    from calculations.future_scenarios import sample_scenarios
    from calculations.utils import CORE_GROUP_PRODUCTS, PRODUCTS
    from main_future import prepare_history, run_future
    history = prepare_history()
    scenario = Scenario.reference(history['hist'])
    core = [PRODUCTS.index(p) for p in CORE_GROUP_PRODUCTS]
    supply, _, _ = run_future(history, scenario, fibre=False)
    stock, ref, _ = run_future(history, scenario, fibre=False, demand='stock')
    np.testing.assert_allclose(new_goods_to_households(stock.flows)[0, core],
                               new_goods_to_households(supply.flows)[0, core])
    durable = dataclasses.replace(Policy.none(), name='L3', durability_increase=0.3)
    i2040 = FUTURE_YEARS.index(2040)
    for demand, lower in (('supply', False), ('stock', True)):
        fut, _, _ = run_future(history, scenario, durable, fibre=False, demand=demand,
                               baseline_purchases=ref.purchases if demand == 'stock' else None)
        base = supply if demand == 'supply' else stock
        new, old = (new_goods_to_households(f.flows)[i2040, core].sum() for f in (fut, base))
        assert (new < old - 1.0) == lower
    for sampled in sample_scenarios(10):
        run_future(history, sampled, fibre=False, demand='stock')
