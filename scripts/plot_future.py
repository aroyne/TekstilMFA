#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
History (iteration 0) and the reference path of the future module for
CL+HT+FW in US.HH: new goods entering the households, discards
(statistics, and from 2026 the cohort model scaled to 2025, against the
unscaled cohort model) and the stock (residual of the balance against the
cohort model).

Usage: python scripts/plot_future.py  ->  output_files/plots/future_reference.png
"""
import matplotlib.pyplot as plt
import pandas as pd

SOURCE = 'output_files/future_reference.csv'
TARGET = 'output_files/plots/future_reference.png'

STATISTICS = '#2a78d6'
MODEL = '#eb6834'
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'

CORE = ['CL', 'HT', 'FW', 'YA', 'CORE']
NEW_GOODS = ['DI.RT-US.HH-Sales to households-TOT', 'RW.RW-US.HH-Private imports-TOT',
             'RW.RW-US.HH-Direct online imports-TOT']
RETURNS = ['US.HH-RW.RW-Returns of direct online purchases-TOT']
DISCARDS = ['US.HH-CO.CO-Separate collection from households-TOT',
            'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
            'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT']
PANELS = [
    ('Nye varer til husholdningene', 'kt per år', [(NEW_GOODS, RETURNS, STATISTICS, 'Tilført')]),
    ('Kassert fra husholdningene', 'kt per år',
     [(DISCARDS, [], STATISTICS, 'Statistikk / skalert'),
      (['US.HH-US.HH-Stock model discards-TOT'], [], MODEL, 'Lagermodell')]),
    ('Lager i husholdningene', 'kt',
     [(['US.HH-US.HH-Stock-TOT'], [], STATISTICS, 'Restledd'),
      (['US.HH-US.HH-Stock model stock-TOT'], [], MODEL, 'Lagermodell')]),
]


def series(df, plus, minus):
    sel = df[df['product'].isin(CORE)]
    total = sel[sel['flow_name'].isin(plus)].groupby('year')['value'].sum()
    if minus:
        total = total - sel[sel['flow_name'].isin(minus)].groupby('year')['value'].sum()
    return total


def main():
    df = pd.read_csv(SOURCE)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), facecolor=SURFACE)
    for ax, (title, unit, lines) in zip(axes, PANELS):
        ax.set_facecolor(SURFACE)
        for plus, minus, color, label in lines:
            s = series(df, plus, minus)
            ax.plot(s.index, s.values, color=color, linewidth=2)
            ax.annotate(label, (s.index[-1], s.values[-1]), textcoords='offset points', xytext=(6, 0),
                        va='center', fontsize=8, color=TEXT_MUTED)
        ax.set_ylim(bottom=0)
        ax.axvline(2025.5, color=TEXT_MUTED, linewidth=1, linestyle=':')
        ax.annotate('Referansebane', (2026.5, ax.get_ylim()[1]), va='top', fontsize=8, color=TEXT_MUTED)
        ax.set_title(title, fontsize=10, color=TEXT, loc='left')
        ax.set_ylabel(unit, color=TEXT_MUTED, fontsize=9)
        ax.set_xlim(1988, 2062)
        ax.set_xticks(range(1990, 2051, 10))
        ax.grid(axis='y', color=GRID, linewidth=0.8)
        ax.tick_params(colors=TEXT_MUTED, labelsize=8)
        for spine in ('top', 'right'):
            ax.spines[spine].set_visible(False)
        for spine in ('left', 'bottom'):
            ax.spines[spine].set_color(GRID)

    fig.suptitle('Klær, hjemmetekstiler og sko: historikk 1988–2025 og referansebane 2026–2050 '
                 '(deterministisk kjøring)', fontsize=11, color=TEXT, x=0.01, ha='left')
    fig.text(0.01, 0.01, 'Referansebane: 2025-nivå per innbygger × SSBs framskriving (MMM); kasseringer fra '
             'lagermodellen skalert til statistikken i 2025; ingen nye tiltak.', fontsize=8, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(TARGET, dpi=150, facecolor=SURFACE)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
