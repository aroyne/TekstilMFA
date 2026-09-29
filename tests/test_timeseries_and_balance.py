import pandas as pd
import pytest

from calculations.balances import check_mass_balance
from calculations.timeseries import interpolate


def test_interpolate_linear_between_and_constant_outside():
    series = interpolate({2000: 0.0, 2010: 10.0}, range(1995, 2016))
    assert series[1995] == 0.0
    assert series[2005] == pytest.approx(5.0)
    assert series[2015] == 10.0


def _rec(flow, year, value):
    return {'flow_name': flow, 'product': 'ALL', 'year': year, 'value': value}


PROCESSES = pd.DataFrame({'code': ['A.A', 'B.B', 'RW.RW'], 'type': ['process', 'process', 'boundary']})


def test_balance_passes_with_stock_change():
    results = [_rec('RW.RW-A.A-In-TOT', 2000, 10.0), _rec('A.A-B.B-Out-TOT', 2000, 7.0),
               _rec('A.A-A.A-Stock change-TOT', 2000, 3.0), _rec('B.B-RW.RW-Export-TOT', 2000, 7.0)]
    check_mass_balance(results, PROCESSES)


def test_balance_fails_when_mass_disappears():
    results = [_rec('RW.RW-A.A-In-TOT', 2000, 10.0), _rec('A.A-RW.RW-Out-TOT', 2000, 7.0)]
    with pytest.raises(ValueError, match='A.A 2000'):
        check_mass_balance(results, PROCESSES)
