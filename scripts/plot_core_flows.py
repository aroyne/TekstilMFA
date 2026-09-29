#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small multiples of the household (US.HH, CL+HT+FW) flows from
output_files/MC_summary.csv: supply to households, separate collection,
textiles in residual waste and the stock change (residual of the balance),
each with its MC median and 95 % interval. Anchor years for residual waste
are marked.

Usage: python scripts/plot_core_flows.py  ->  output_files/plots/core_household_flows.png
"""
import matplotlib.pyplot as plt
import pandas as pd

SUMMARY = 'output_files/MC_summary.csv'
ANCHORS = 'data_files/anchor_values.csv'
TARGET = 'output_files/plots/core_household_flows.png'

SERIES = '#2a78d6'
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'

CORE = ['CL', 'HT', 'FW', 'CORE']
INFLOWS = ['DI.RT-US.HH-Sales to households-TOT', 'RW.RW-US.HH-Private imports-TOT',
           'RW.RW-US.HH-Direct online imports-TOT', 'CO.RE-US.HH-Secondhand sales to households-TOT']
PANELS = [
    ('Tilført husholdninger (salg, privatimport, netthandel, brukt)', INFLOWS),
    ('Separat innsamlet', ['US.HH-CO.CO-Separate collection from households-TOT']),
    ('Tekstiler i restavfall', ['US.HH-WM.RS-Textiles in residual and bulky waste-TOT']),
    ('Lagerendring i husholdningene (restledd)', ['US.HH-US.HH-Stock change-TOT']),
]


def panel_series(df, flows):
    # Medians and percentiles do not add across flows, so the interval of a
    # sum of flows is approximated by summing the flows' own bounds.
    sel = df[df['flow_name'].isin(flows) & df['product'].isin(CORE)]
    return sel.groupby('year')[['median', 'p2_5', 'p97_5']].sum()


def main():
    df = pd.read_csv(SUMMARY)
    anchors = pd.read_csv(ANCHORS)
    residual_anchors = anchors[anchors['parameter_id'] == 'residual_core']

    fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=True, facecolor=SURFACE)
    for ax, (title, flows) in zip(axes.flat, PANELS):
        s = panel_series(df, flows)
        ax.set_facecolor(SURFACE)
        ax.fill_between(s.index, s['p2_5'], s['p97_5'], color=SERIES, alpha=0.18, linewidth=0)
        ax.plot(s.index, s['median'], color=SERIES, linewidth=2)
        if 'Stock change' in flows[0]:
            ax.axhline(0, color=TEXT_MUTED, linewidth=1)
        if 'residual' in flows[0]:
            ax.plot(residual_anchors['year'], residual_anchors['value'], 'o', markersize=8,
                    color=SERIES, markeredgecolor=SURFACE, markeredgewidth=2, zorder=3)
            for _, r in residual_anchors.iterrows():
                ax.annotate(f"{int(r['year'])}", (r['year'], r['value']), textcoords='offset points',
                            xytext=(0, 9), ha='center', fontsize=8, color=TEXT_MUTED)
        ax.set_title(title, fontsize=10, color=TEXT, loc='left')
        ax.set_ylabel('kt', color=TEXT_MUTED, fontsize=9)
        ax.grid(axis='y', color=GRID, linewidth=0.8)
        ax.tick_params(colors=TEXT_MUTED, labelsize=8)
        for spine in ('top', 'right'):
            ax.spines[spine].set_visible(False)
        for spine in ('left', 'bottom'):
            ax.spines[spine].set_color(GRID)

    fig.suptitle('Klær, hjemmetekstiler og sko i husholdningene, 1988–2025 (median og 95 %-intervall)',
                 fontsize=11, color=TEXT, x=0.01, ha='left')
    fig.text(0.01, 0.005, 'Punkter: ankerår for restavfall (SSB 1998; Mepex-plukkanalyser 2018, 2022, 2025). '
             'Intervall for summerte flyter er tilnærmet som sum av grensene.', fontsize=8, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    fig.savefig(TARGET, dpi=150, facecolor=SURFACE)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
