#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mass balance check for every process in one MC iteration. Stock changes are
recorded as flows from a process to itself ('US.HH-US.HH-Stock change-TOT')
and are the only way a process may gain or lose mass.
"""
from collections import defaultdict

import pandas as pd

TOLERANCE_KT = 1e-6


def check_mass_balance(results, processes):
    """Raises ValueError if inflows - outflows - stock change != 0 anywhere."""
    checked = set(processes.loc[processes['type'] == 'process', 'code'])
    net = defaultdict(float)  # (process, year) -> in - out - stock change
    for rec in results:
        source, target = rec['flow_name'].split('-')[:2]
        value = rec['value']
        if source == target:
            net[(source, rec['year'])] -= value
            continue
        net[(target, rec['year'])] += value
        net[(source, rec['year'])] -= value

    errors = [(p, y, v) for (p, y), v in net.items() if p in checked and abs(v) > TOLERANCE_KT]
    if errors:
        lines = '\n'.join(f"  {p} {y}: {v:+.4f} kt" for p, y, v in sorted(errors)[:20])
        raise ValueError(f"Mass balance violated in {len(errors)} process-years:\n{lines}")


def load_processes(path='system/processes.csv'):
    return pd.read_csv(path)
