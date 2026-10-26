#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System diagram (Mermaid) of all pools, subpools and flows, generated from
system/processes.csv and system/flows.csv so it cannot drift from the register.
Pools are drawn as boxes; line style follows the flow priority (1 thick,
2 normal, 3 dotted), and planned flows are labelled as such. The rest of the
world is drawn twice, as import source on the left and export sink on the
right, so the main chain reads left to right.

The block is written between the SYSTEM_DIAGRAM markers in
docs/SYSTEMDEFINISJON.md, which GitHub renders.

Usage: python scripts/plot_system_diagram.py
"""
import re

import pandas as pd

PROCESSES = 'system/processes.csv'
FLOWS = 'system/flows.csv'
TARGET = 'docs/SYSTEMDEFINISJON.md'
START, END = '<!-- SYSTEM_DIAGRAM:START -->', '<!-- SYSTEM_DIAGRAM:END -->'

ARROW = {1: '==>', 2: '-->', 3: '-.->'}
SHAPE = {'boundary': ('((', '))'), 'sink': ('{{', '}}'), 'process': ('[', ']')}


def node_id(code, role=''):
    return code.replace('.', '_') + role


def node(proc, role=''):
    open_, close = ('[(', ')]') if proc['has_stock'] == 'yes' else SHAPE[proc['type']]
    return f'{node_id(proc["code"], role)}{open_}"{proc["code"]}<br>{proc["subpool_name"]}"{close}'


def mermaid():
    procs = pd.read_csv(PROCESSES)
    flows = pd.read_csv(FLOWS)
    lines = ['```mermaid', 'flowchart LR']
    for pool, group in procs.groupby('pool', sort=False):
        if pool == 'RW':
            proc = group.iloc[0]
            lines += [f'  subgraph RW_import["Rest of the world (import)"]', f'    {node(proc, "_in")}', '  end',
                      f'  subgraph RW_export["Rest of the world (export)"]', f'    {node(proc, "_out")}', '  end']
            continue
        lines.append(f'  subgraph {pool}["{group.iloc[0]["pool_name"]} ({pool})"]')
        lines += [f'    {node(proc)}' for _, proc in group.iterrows()]
        lines.append('  end')
    # Parallel flows between the same pair of subpools share one arrow
    for (source, target), group in flows.groupby(['source', 'target'], sort=False):
        label = ' + '.join(f'{name} (planlagt)' if status == 'planned' else name
                           for name, status in zip(group['name'], group['status']))
        src = node_id(source, '_in' if source == 'RW.RW' else '')
        dst = node_id(target, '_out' if target == 'RW.RW' else '')
        lines.append(f'  {src} {ARROW[group["priority"].min()]}|"{label}"| {dst}')
    lines.append('```')
    return '\n'.join(lines)


def main():
    with open(TARGET, encoding='utf-8') as f:
        text = f.read()
    pattern = re.compile(re.escape(START) + '.*?' + re.escape(END), re.S)
    if not pattern.search(text):
        raise ValueError(f'{TARGET} has no {START} ... {END} block')
    text = pattern.sub(lambda _: f'{START}\n{mermaid()}\n{END}', text)
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    main()
