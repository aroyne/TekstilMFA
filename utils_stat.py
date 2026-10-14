#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Plotly figures for the report pages, built from the MC
summaries in output_files/: one time series per flow (by product, with the
95 % interval of the total), its composition by material (fibre layer), and
a mass balance per subpool and pool. Written as standalone HTML files that
load plotly.js from the CDN, so they can be embedded with an iframe.
"""
import json
import os

import plotly.graph_objects as go

# Categorical slots in fixed order (validated default palette, light mode).
SLOTS = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948']
OTHER = '#9a9893'
COLOR_OF_PRODUCT = {'CL': SLOTS[0], 'HT': SLOTS[1], 'FW': SLOTS[2], 'CA': SLOTS[3], 'SA': SLOTS[4],
                    'TA': SLOTS[5], 'OM': SLOTS[6], 'CORE': SLOTS[7], 'ALL': SLOTS[0],
                    # Retail yarn never shares a flow with the CORE group (flows have products or
                    # product groups, not both), so the two can share a slot.
                    'YA': SLOTS[7]}
COLOR_OF_MATERIAL = dict(zip(['SYN', 'CO', 'WO', 'CV', 'OTH', 'NT'], SLOTS))
PRODUCT_NAMES = {'CL': 'Klær', 'HT': 'Hjemmetekstiler', 'FW': 'Sko', 'CA': 'Tepper', 'SA': 'Sekker',
                 'TA': 'Presenninger og telt', 'OM': 'Andre konfeksjonerte varer', 'YA': 'Garn i detaljsalg',
                 'CORE': 'Klær, hjemmetekstiler og sko', 'ALL': 'Alle produkter'}
MATERIAL_NAMES = {'SYN': 'Syntetisk', 'CO': 'Bomull', 'WO': 'Ull', 'CV': 'Regenerert cellulose',
                  'OTH': 'Andre fibre', 'NT': 'Ikke-tekstil'}
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'
MAX_BALANCE_SERIES = 8


def _layout(fig, title, height=380):
    fig.update_layout(
        title=dict(text=title, x=0.01, font=dict(size=14, color=TEXT)),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE, height=height,
        font=dict(family='system-ui, sans-serif', size=12, color=TEXT_MUTED),
        margin=dict(l=60, r=20, t=50, b=40), hovermode='x unified', bargap=0.15,
        legend=dict(orientation='h', y=-0.15, x=0, font=dict(size=11)),
        yaxis=dict(title='kt per år', gridcolor=GRID, zeroline=True, zerolinecolor=TEXT_MUTED),
        xaxis=dict(gridcolor=SURFACE, dtick=5),
    )
    return fig


def _write(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.write_html(path, include_plotlyjs='cdn', full_html=True, config={'displaylogo': False})


def plot_flow(summary, flow_code, title, path):
    """
    Stacked bars of the median per product (or product group), with the
    median and 95 % interval of the total as a line and band.
    """
    rows = summary[summary['flow_name'] == flow_code]
    parts = rows[~rows['product'].isin(['TOTAL'])]
    total = rows[rows['product'] == 'TOTAL'] if (rows['product'] == 'TOTAL').any() else parts
    fig = go.Figure()
    for product in COLOR_OF_PRODUCT:
        part = parts[parts['product'] == product]
        if part.empty or (part['median'].abs() < 1e-9).all():
            continue
        fig.add_bar(x=part['year'], y=part['median'], name=PRODUCT_NAMES[product],
                    marker=dict(color=COLOR_OF_PRODUCT[product], line=dict(color=SURFACE, width=1)),
                    hovertemplate='%{y:.2f} kt')
    fig.add_scatter(x=total['year'], y=total['p97_5'], mode='lines', line=dict(width=0),
                    showlegend=False, hoverinfo='skip')
    fig.add_scatter(x=total['year'], y=total['p2_5'], mode='lines', line=dict(width=0), fill='tonexty',
                    fillcolor='rgba(11,11,11,0.10)', name='95 %-intervall (sum)', hoverinfo='skip')
    fig.add_scatter(x=total['year'], y=total['median'], mode='lines', name='Sum (median)',
                    line=dict(color=TEXT, width=2), customdata=total[['p2_5', 'p97_5']].to_numpy(),
                    hovertemplate='%{y:.2f} kt (%{customdata[0]:.2f}–%{customdata[1]:.2f})')
    fig.update_layout(barmode='relative')
    _write(_layout(fig, title), path)


def plot_flow_materials(fibre_summary, flow_code, title, path):
    """Stacked bars of the median per material, summed over products."""
    rows = fibre_summary[(fibre_summary['flow_name'] == flow_code)
                         & fibre_summary['product'].isin(['TOTAL', 'ALL'])]
    fig = go.Figure()
    for material in COLOR_OF_MATERIAL:
        part = rows[rows['material'] == material]
        fig.add_bar(x=part['year'], y=part['median'], name=MATERIAL_NAMES[material],
                    marker=dict(color=COLOR_OF_MATERIAL[material], line=dict(color=SURFACE, width=1)),
                    hovertemplate='%{y:.2f} kt')
    fig.update_layout(barmode='stack')
    _write(_layout(fig, title), path)


def _fold(series):
    """
    Keeps the largest series (by mean absolute median) in their register
    order, each with the colour of its position, and folds the rest into
    'Andre'. Colour follows the flow, not its rank.
    """
    coloured = [(label, code, values, SLOTS[i % len(SLOTS)]) for i, (label, code, values) in enumerate(series)]
    if len(coloured) <= MAX_BALANCE_SERIES:
        return coloured
    order = sorted(range(len(coloured)), key=lambda i: -coloured[i][2].abs().mean())
    largest = set(order[:MAX_BALANCE_SERIES - 1])
    kept = [s for i, s in enumerate(coloured) if i in largest]
    folded = sum(s[2] for i, s in enumerate(coloured) if i not in largest)
    return kept + [('Andre', None, folded, OTHER)]


def plot_balance(summary, inflows, outflows, stock_changes, title, path):
    """
    Mass balance of a subpool or pool: inflows stacked above zero, outflows
    and stock changes below, from the 'TOTAL'/'ALL' medians. inflows,
    outflows and stock_changes are lists of (label, flow code).
    """
    totals = summary[summary['product'].isin(['TOTAL', 'ALL'])].pivot_table(
        index='year', columns='flow_name', values='median', aggfunc='first')
    series = [(label, code, totals[code]) for label, code in inflows]
    series += [(label, code, -totals[code]) for label, code in outflows + stock_changes]
    fig = go.Figure()
    for label, code, values, color in _fold(series):
        fig.add_bar(x=values.index, y=values, name=label, hovertemplate='%{y:.2f} kt',
                    marker=dict(color=color, line=dict(color=SURFACE, width=1)))
    fig.update_layout(barmode='relative')
    _write(_layout(fig, title, height=460), path)


# --- Sankey diagrams --------------------------------------------------------
# The page is drawn by the JavaScript in templates/sankey_template.html (taken
# from NitrogenBudsjett): year slider, colouring by textile form (TOT) or by
# material (fibre layer), loops for flows back to an earlier column, and a
# value-to-pixel scale fixed across the years.

SANKEY_TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'sankey_template.html')
SANKEY_FIRST_YEAR = 1990
SANKEY_POOLS = {
    'RW': ('Utlandet', '#4a5568'),
    'PS': ('Norsk ull', '#8c6d46'),
    'MA': ('Industri', '#d69e2e'),
    'DI': ('Handel', '#2c7a7b'),
    'US': ('Bruk', '#2f855a'),
    'CO': ('Innsamling og sortering', '#2b6cb0'),
    'WM': ('Avfallsbehandling', '#97266d'),
    'EN': ('Avløp og luft', '#718096'),
}
SANKEY_FORMS = {
    'NEW': ('Nye varer', SLOTS[0]), 'FIB': ('Fiber og garn', SLOTS[3]), 'FAB': ('Metervare', SLOTS[1]),
    'MIX': ('Brukte, usortert', SLOTS[6]), 'USE': ('Brukte, ombrukbare', SLOTS[2]),
    'WRN': ('Brukte, utslitte', SLOTS[7]), 'PCW': ('Produksjonsavfall', SLOTS[4]),
    'MFR': ('Mikrofibre', SLOTS[5]), 'BYP': ('Biprodukt, ikke tekstil', OTHER),
}
# The finished goods trade dwarfs the other flows; the 'hide' view leaves it out.
SANKEY_HIDDEN = ['RW.RW-DI.RT-Finished textile products import-TOT',
                 'DI.RT-RW.RW-Export of finished textile products-TOT']
NATIONAL_SANKEY_COLS = [['RW_in', 'PS'], ['MA'], ['DI'], ['US'], ['CO'], ['WM'], ['RW_out', 'EN']]
NATIONAL_SANKEY_HEADS = ['Tilførsel', 'Industri', 'Handel', 'Bruk', 'Innsamling', 'Avfall', 'Ut av systemet']


def _sankey_rows(summary, flow_codes, years, by_material):
    rows = summary[summary['flow_name'].isin(flow_codes) & summary['product'].isin(['TOTAL', 'ALL'])
                   & summary['year'].isin(years)]
    keys = ['flow_name', 'material'] if by_material else ['flow_name']
    return rows.groupby(keys + ['year'])[['median', 'p2_5', 'p97_5']].sum()


def _sankey_records(summary, fibre_summary, register, years, node_of, name_of):
    """
    Flow records for the page: 'flows' (TOT, key = textile form) and
    'materialFlows' (fibre layer, one per flow and material). Flows that are
    zero in all years are left out.
    """
    codes = list(register['flow_code'])
    form_of = dict(zip(register['flow_code'], register['form']))
    out = {'flows': [], 'materialFlows': []}
    for by_material, target in ((False, 'flows'), (True, 'materialFlows')):
        rows = _sankey_rows(fibre_summary if by_material else summary, codes, years, by_material)
        for key, g in rows.groupby(level=[0, 1] if by_material else 0):
            code = key[0] if by_material else key
            g = g.droplevel(list(range(g.index.nlevels - 1))).reindex(years).fillna(0.0).clip(lower=0.0)
            if g['median'].max() <= 0:
                continue
            source, target_code = code.split('-')[:2]
            out[target].append({
                's': node_of(source, True), 't': node_of(target_code, False),
                'name': name_of(code, source, target_code),
                'key': key[1] if by_material else form_of[code],
                'hide': code in SANKEY_HIDDEN,
                'v': g['median'].round(4).tolist(), 'lo': g['p2_5'].round(4).tolist(),
                'hi': g['p97_5'].round(4).tolist(),
            })
    return out


def _write_sankey_page(data, path):
    data = {
        'forms': {k: {'name': n, 'color': c} for k, (n, c) in SANKEY_FORMS.items()},
        'materials': {m: {'name': MATERIAL_NAMES[m], 'color': c} for m, c in COLOR_OF_MATERIAL.items()},
        'hiddenNames': sorted({f['name'] for f in data['flows'] if f['hide']}),
        **data,
    }
    with open(SANKEY_TEMPLATE, encoding='utf-8') as fh:
        html = fh.read().replace('__DATA__', json.dumps(data, separators=(',', ':')))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)


def plot_national_sankey(summary, fibre_summary, register, path):
    """
    Sankey diagram of the whole system at pool level, for the home page.
    Flows within a pool are left out; RW appears as a source (imports) and as
    a target (exports).
    """
    years = [int(y) for y in sorted(summary["year"].unique()) if y >= SANKEY_FIRST_YEAR]
    register = register[register['source'].str[:2] != register['target'].str[:2]]

    def node_of(code, is_source):
        pool = code[:2]
        return pool + ('_in' if is_source else '_out') if pool == 'RW' else pool

    roles = {'RW_in': 'import', 'RW_out': 'eksport'}
    nodes = {n: {'name': SANKEY_POOLS[n[:2]][0], 'color': SANKEY_POOLS[n[:2]][1], 'role': roles.get(n, '')}
             for col in NATIONAL_SANKEY_COLS for n in col}
    data = {
        'title': 'Sankey-diagram av tekstilstrømmer i Norge',
        'years': years,
        'layout': {'cols': NATIONAL_SANKEY_COLS, 'colHeads': NATIONAL_SANKEY_HEADS,
                   'marginL': 110, 'marginR': 130, 'mainH': 470, 'nodeGap': 18},
        'nodes': nodes,
        'loopNote': 'Flyter som går tilbake til en tidligere kolonne (bruktsalg til husholdningene, '
                    'gjenvunnet fiber til spinning), er tegnet som løkker under diagrammet.',
        **_sankey_records(summary, fibre_summary, register, years, node_of,
                          lambda code, s, t: code.split('-')[2]),
    }
    _write_sankey_page(data, path)


def _subpool_columns(subpools, internal):
    """
    Column of each subpool in a pool diagram (as in NitrogenBudsjett).
    internal maps (source, target) pairs to their largest yearly flow. Pairs
    are added largest first while the graph stays acyclic; each subpool sits
    one column right of its furthest upstream subpool, and the pairs left
    out are drawn as loops.
    """
    edges = []

    def reaches(a, b):
        stack, seen = [a], set()
        while stack:
            n = stack.pop()
            if n == b:
                return True
            seen.add(n)
            stack += [t for s, t in edges if s == n and t not in seen]
        return False

    for (s, t), _ in sorted(internal.items(), key=lambda kv: -kv[1]):
        if not reaches(t, s):
            edges.append((s, t))
    col = {sp: 0 for sp in subpools}
    for _ in subpools:
        for s, t in edges:
            col[t] = max(col[t], col[s] + 1)
    return col


def plot_pool_sankey(summary, fibre_summary, register, processes, pool, path):
    """
    Sankey diagram for one pool page: the pool's subpools in the middle,
    flows from other pools on the left and to other pools on the right
    (other pools shown at pool level; the tooltip names the subpool), and
    the flows between the subpools.
    """
    years = [int(y) for y in sorted(summary["year"].unique()) if y >= SANKEY_FIRST_YEAR]
    register = register[((register['source'].str[:2] == pool) | (register['target'].str[:2] == pool))
                        & (register['source'] != register['target'])]
    subpools = sorted(set(register.loc[register['source'].str[:2] == pool, 'source'])
                      | set(register.loc[register['target'].str[:2] == pool, 'target']))
    totals = summary[summary['product'].isin(['TOTAL', 'ALL'])].groupby('flow_name')['median'].max()
    internal = {}
    for _, r in register[register['source'].isin(subpools) & register['target'].isin(subpools)].iterrows():
        internal[(r['source'], r['target'])] = max(internal.get((r['source'], r['target']), 0.0),
                                                   totals.get(r['flow_code'], 0.0))
    sub_col = _subpool_columns(subpools, internal)
    n_sub_cols = max(sub_col.values()) + 1

    def node_of(code, is_source):
        return code if code in subpools else code[:2] + ('_in' if is_source else '_out')

    def name_of(code, s, t):
        name = code.split('-')[2]
        other = t if s in subpools else s
        if other in subpools or other[:2] == other[3:]:
            return name
        return f"{name} ({'til' if s in subpools else 'fra'} {other})"

    records = _sankey_records(summary, fibre_summary, register, years, node_of, name_of)
    used = {f['s'] for f in records['flows']} | {f['t'] for f in records['flows']}
    sources = [p + '_in' for p in SANKEY_POOLS if p + '_in' in used]
    targets = [p + '_out' for p in SANKEY_POOLS if p + '_out' in used]
    cols = [c for c in [sources] + [[sp for sp in subpools if sub_col[sp] == c] for c in range(n_sub_cols)]
            + [targets] if c]
    names = dict(zip(processes['code'], processes['subpool_name']))
    nodes = {sp: {'name': names[sp], 'color': SANKEY_POOLS[pool][1], 'role': sp} for sp in subpools}
    for n in sources + targets:
        nodes[n] = {'name': SANKEY_POOLS[n[:2]][0], 'color': SANKEY_POOLS[n[:2]][1], 'role': ''}
    heads = (['Fra andre pooler'] if sources else []) + ['Subpooler' if len(subpools) > 1 else ''] \
        + [''] * (n_sub_cols - 1) + (['Til andre pooler'] if targets else [])
    data = {
        'title': f'Sankey-diagram av tekstilstrømmer i poolen {SANKEY_POOLS[pool][0]}',
        'years': years,
        'layout': {'cols': cols, 'colHeads': heads, 'marginL': 150, 'marginR': 150, 'mainH': 400, 'nodeGap': 34},
        'nodes': nodes,
        'loopNote': 'Flyter mellom subpooler som går tilbake til en tidligere kolonne, er tegnet som løkker '
                    'under diagrammet.',
        **records,
    }
    _write_sankey_page(data, path)
