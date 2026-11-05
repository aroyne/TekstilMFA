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
    _, fut, _, _ = reference
    assert list(fut.dims['t'].items) == FUTURE_YEARS


def test_scaled_discards_continue_from_2025(reference):
    hist, fut, ref, _ = reference
    discards_2025 = sum(hist.flows[c].values[BASE, CORE] for c in DISCARDS)
    discards_2026 = sum(fut.flows[c].values[0, CORE] for c in DISCARDS)
    assert ref.scale * ref.cohorts['outflow'][BASE] == pytest.approx(discards_2025)
    assert discards_2026 == pytest.approx(discards_2025, rel=0.03)


def test_supply_per_inhabitant_is_held(reference):
    hist, fut, ref, _ = reference
    code = 'DI.RT-US.HH-Sales to households-TOT'
    np.testing.assert_allclose(fut.flows[code].values / ref.growth[:, None], np.repeat(
        hist.flows[code].values[BASE][None], len(FUTURE_YEARS), axis=0))


def test_no_clipping_in_reference(reference):
    _, fut, _, _ = reference
    assert all(np.abs(c.values).max() == 0.0 for c in fut.clipped.values())
