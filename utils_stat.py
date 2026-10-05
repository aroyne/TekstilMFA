#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Plotly figures for the report pages, built from the MC
summaries in output_files/: one time series per flow (by product, with the
95 % interval of the total), its composition by material (fibre layer), and
a mass balance per subpool and pool. Written as standalone HTML files that
load plotly.js from the CDN, so they can be embedded with an iframe.
"""
import os

import plotly.graph_objects as go

# Categorical slots in fixed order (validated default palette, light mode).
SLOTS = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948']
OTHER = '#9a9893'
COLOR_OF_PRODUCT = {'CL': SLOTS[0], 'HT': SLOTS[1], 'FW': SLOTS[2], 'CA': SLOTS[3], 'SA': SLOTS[4],
                    'TA': SLOTS[5], 'OM': SLOTS[6], 'CORE': SLOTS[7], 'ALL': SLOTS[0]}
COLOR_OF_MATERIAL = dict(zip(['SYN', 'CO', 'WO', 'CV', 'OTH', 'NT'], SLOTS))
PRODUCT_NAMES = {'CL': 'Klær', 'HT': 'Hjemmetekstiler', 'FW': 'Sko', 'CA': 'Tepper', 'SA': 'Sekker',
                 'TA': 'Presenninger og telt', 'OM': 'Andre konfeksjonerte varer',
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
