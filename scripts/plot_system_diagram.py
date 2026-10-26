#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System diagram (Mermaid) of all pools, subpools and flows, generated from
system/processes.csv and system/flows.csv so it cannot drift from the register.
Pools are drawn as boxes; line style follows the flow priority (1 thick,
2 normal, 3 dotted), and planned flows are labelled as such. The rest of the
world is drawn twice, as import source on the left and export sink on the
right, so the main chain reads left to right.

The Mermaid block is written between the SYSTEM_DIAGRAM markers in
docs/SYSTEMDEFINISJON.md, which GitHub renders. The same diagram is drawn as
a PNG with matplotlib for slides and documents; Mermaid cannot be rendered
offline here, so the PNG uses a fixed layout (POS) that must be extended when
a subpool is added.

Usage: python scripts/plot_system_diagram.py
       -> docs/SYSTEMDEFINISJON.md and output_files/plots/system_diagram.png
"""
import re
import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.path import Path

PROCESSES = 'system/processes.csv'
FLOWS = 'system/flows.csv'
TARGET = 'docs/SYSTEMDEFINISJON.md'
START, END = '<!-- SYSTEM_DIAGRAM:START -->', '<!-- SYSTEM_DIAGRAM:END -->'

PNG = 'output_files/plots/system_diagram.png'

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


# PNG layout in inches, sized to fill the text width of a portrait A4 page
# (about 17 cm) without scaling the fonts. Material moves from top to bottom;
# RW.RW is drawn as an import bar on the left and an export bar on the right.
FIG_W, FIG_H = 7.0, 10.0
C1, C2, C3 = 1.45, 3.5, 5.55
G12, G23 = (C1 + C2) / 2, (C2 + C3) / 2
R = [9.35, 8.15, 6.95, 5.75, 4.55, 3.35, 2.15, 0.95]
POS = {
    'PS.WO': (C1, R[0]),
    'MA.FI': (C1, R[1]), 'MA.TX': (C2, R[1]),
    'DI.RT': (C2, R[2]),
    'US.HH': (C2, R[3]), 'US.IC': (C3, R[3]),
    'CO.RE': (C1, R[4]), 'CO.CO': (C2, R[4]), 'CO.SO': (C3, R[4]),
    'WM.RS': (C1, R[5]), 'WM.IN': (C1, R[6]), 'WM.LF': (C2, R[6]), 'WM.RC': (C3, R[6]),
    'EN.WA': (C1, R[7]), 'EN.AI': (C2, R[7]),
}
BAR_IN, BAR_OUT, BAR_W = 0.12, 6.88, 0.24
BAR_Y = (0.55, 9.75)
NODE_W, NODE_H = 1.5, 0.62
# Priority 3 flows are left out of the PNG to keep it readable at A4
MAX_PRIORITY = 2
# Waypoints for arrows that would otherwise cross a node; routed through the
# channels between columns and rows
_mid = lambda i: (R[i] + R[i + 1]) / 2
_top = lambda code: POS[code][1] + NODE_H / 2
_bottom = lambda code: POS[code][1] - NODE_H / 2
ROUTE = {
    ('MA.FI', 'DI.RT'): [(C1, R[2] + 0.15)],
    ('RW.RW', 'MA.TX'): [(C2 - 0.35, _mid(0) - 0.05)],
    ('MA.FI', 'RW.RW'): [(C1 + 0.45, _mid(0) + 0.15), (BAR_OUT, _mid(0) + 0.15)],
    ('RW.RW', 'US.HH'): [(G12, R[3] + 0.1)],
    ('US.HH', 'WM.RS'): [(G12 - 0.1, R[3] - 0.05), (G12 - 0.1, _top('WM.RS') + 0.2),
                         (C1 + 0.4, _top('WM.RS') + 0.2)],
    ('US.HH', 'EN.WA'): [(G12 + 0.1, R[3] - 0.2), (G12 + 0.1, R[7])],
    ('CO.RE', 'US.HH'): [(C1 + 0.3, _mid(3)), (C2 - 0.4, _mid(3))],
    ('CO.SO', 'CO.RE'): [(C3 - 0.3, _bottom('CO.SO') - 0.12), (C1 + 0.3, _bottom('CO.SO') - 0.12)],
    ('CO.CO', 'RW.RW'): [(C2 + 0.45, _mid(3) + 0.05), (BAR_OUT, _mid(3) + 0.05)],
    ('US.IC', 'WM.RS'): [(G23, _bottom('US.IC')), (G23, R[5] + 0.12)],
    ('WM.RS', 'RW.RW'): [(BAR_OUT, R[5] - 0.12)],
}
WIDTH = {1: 2.4, 2: 1.3, 3: 1.0}
STYLE = {1: '-', 2: '-', 3: (0, (3, 2))}
FLOW = '#2a78d6'
FLOW_MINOR = '#6f6e69'
PLANNED = '#c0392b'
POOL_FILL = '#efeee9'
SURFACE = '#ffffff'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'


def _clip(centre, towards, half_w, half_h):
    """Point where an arrow towards a point leaves the box around centre.

    A point straight above, below or beside the box gives a perpendicular
    attachment, so routed arrows start and end at right angles."""
    dx, dy = towards[0] - centre[0], towards[1] - centre[1]
    if abs(dx) < half_w and abs(dy) > half_h:
        return towards[0], centre[1] + half_h * (1 if dy > 0 else -1)
    if abs(dy) < half_h and abs(dx) > half_w:
        return centre[0] + half_w * (1 if dx > 0 else -1), towards[1]
    t = min(half_w / abs(dx) if dx else float('inf'), half_h / abs(dy) if dy else float('inf'))
    return centre[0] + t * dx, centre[1] + t * dy


def _endpoints(source, target, route):
    # Without waypoints, arrows to or from a bar run horizontally
    if route:
        first, last = route[0], route[-1]
    elif source == 'RW.RW':
        first = last = (BAR_IN, POS[target][1])
    elif target == 'RW.RW':
        first = last = (BAR_OUT, POS[source][1])
    else:
        first, last = POS[target], POS[source]
    if source == 'RW.RW':
        start = (BAR_IN + BAR_W / 2, first[1])
    else:
        start = _clip(POS[source], first, NODE_W / 2, NODE_H / 2)
    if target == 'RW.RW':
        end = (BAR_OUT - BAR_W / 2, last[1])
        route = route[:-1] if route and route[-1][0] == BAR_OUT else route
    else:
        end = _clip(POS[target], last, NODE_W / 2 + 0.02, NODE_H / 2 + 0.02)
    return [start, *route, end]


def plot_png():
    procs = pd.read_csv(PROCESSES)
    flows = pd.read_csv(FLOWS)
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.axis('off')

    for pool, group in procs.groupby('pool', sort=False):
        if pool == 'RW':
            continue
        xs, ys = zip(*[POS[c] for c in group['code']])
        x0, y0 = min(xs) - NODE_W / 2 - 0.12, min(ys) - NODE_H / 2 - 0.1
        w, h = max(xs) - min(xs) + NODE_W + 0.24, max(ys) - min(ys) + NODE_H + 0.32
        ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0,rounding_size=0.08',
                                    fc=POOL_FILL, ec='none', zorder=0))
        ax.text(x0 + 0.07, y0 + h - 0.04, f"{group.iloc[0]['pool_name']} ({pool})", ha='left', va='top',
                fontsize=7.5, color=TEXT_MUTED, style='italic', zorder=1)

    for x, label in ((BAR_IN, 'Rest of the world (RW.RW): import'),
                     (BAR_OUT, 'Rest of the world (RW.RW): eksport')):
        ax.add_patch(FancyBboxPatch((x - BAR_W / 2, BAR_Y[0]), BAR_W, BAR_Y[1] - BAR_Y[0],
                                    boxstyle='round,pad=0,rounding_size=0.06', fc='white', ec=TEXT,
                                    lw=0.9, ls='--', zorder=3))
        ax.text(x, sum(BAR_Y) / 2, label, rotation=90, ha='center', va='center', fontsize=9,
                weight='bold', color=TEXT, zorder=4)

    for _, proc in procs[procs['code'] != 'RW.RW'].iterrows():
        x, y = POS[proc['code']]
        ax.add_patch(FancyBboxPatch((x - NODE_W / 2, y - NODE_H / 2), NODE_W, NODE_H,
                                    boxstyle='round,pad=0,rounding_size=0.06', fc='white', ec=TEXT,
                                    lw=2.0 if proc['has_stock'] == 'yes' else 0.9,
                                    ls='--' if proc['type'] == 'boundary' else '-', zorder=3))
        name = textwrap.fill(proc['subpool_name'].replace(' (not followed)', ''), 21)
        ax.text(x, y + 0.15, proc['code'], ha='center', va='center', fontsize=9, weight='bold',
                color=TEXT, zorder=4)
        ax.text(x, y - 0.1, name, ha='center', va='center', fontsize=7.5, color=TEXT, zorder=4,
                linespacing=0.95)

    shown = flows[flows['priority'] <= MAX_PRIORITY]
    for (source, target), group in shown.groupby(['source', 'target'], sort=False):
        priority = group['priority'].min()
        planned = (group['status'] == 'planned').all()
        color = PLANNED if planned else FLOW if priority == 1 else FLOW_MINOR
        verts = _endpoints(source, target, ROUTE.get((source, target), []))
        path = Path(verts, [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1))
        ax.add_patch(FancyArrowPatch(path=path, arrowstyle='-|>', mutation_scale=8 + 2.5 * WIDTH[priority],
                                     lw=WIDTH[priority], ls=STYLE[priority], color=color,
                                     joinstyle='round', capstyle='butt', zorder=2))

    handles = [plt.Line2D([], [], color=FLOW, lw=WIDTH[1], label='Prioritet 1'),
               plt.Line2D([], [], color=FLOW_MINOR, lw=WIDTH[2], label='Prioritet 2'),
               plt.Line2D([], [], color=PLANNED, lw=WIDTH[2], label='Planlagt'),
               plt.Line2D([], [], color=TEXT, lw=2.0, label='Prosess med lager'),
               plt.Line2D([], [], color=TEXT, lw=0.9, ls='--', label='Systemgrense')]
    ax.legend(handles=handles, loc='upper right', bbox_to_anchor=(BAR_OUT / FIG_W - 0.03, 0.99),
              frameon=False, fontsize=7.5, ncol=1, handlelength=2.2)
    ax.text(BAR_OUT - 0.3, R[0] - 0.62, 'Flyter med prioritet 3 er ikke vist.\nAlle flytene står i system/flows.csv.',
            ha='right', va='top', fontsize=7.5, color=TEXT_MUTED)
    fig.savefig(PNG, dpi=300, facecolor=SURFACE)


def main():
    with open(TARGET, encoding='utf-8') as f:
        text = f.read()
    pattern = re.compile(re.escape(START) + '.*?' + re.escape(END), re.S)
    if not pattern.search(text):
        raise ValueError(f'{TARGET} has no {START} ... {END} block')
    text = pattern.sub(lambda _: f'{START}\n{mermaid()}\n{END}', text)
    with open(TARGET, 'w', encoding='utf-8') as f:
        f.write(text)
    plot_png()


if __name__ == '__main__':
    main()
