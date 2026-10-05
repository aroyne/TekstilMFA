#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compares the statistics-based household balance (D8) with the parallel
stock model for CL+HT+FW in US.HH: discards (separate collection + residual
waste vs. cohort-model outflow) and the stock change (residual of the
balance vs. cohort model), each with MC median and 95 % interval.

Usage: python scripts/plot_stock_model.py  ->  output_files/plots/stock_model_comparison.png
"""
import matplotlib.pyplot as plt
import pandas as pd

SUMMARY = 'output_files/MC_summary.csv'
TARGET = 'output_files/plots/stock_model_comparison.png'

STATISTICS = '#2a78d6'
MODEL = '#eb6834'
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'

CORE = ['CL', 'HT', 'FW', 'CORE']
DISCARDS = ['US.HH-CO.CO-Separate collection from households-TOT',
            'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
            'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT']
PANELS = [
    ('Kassert fra husholdningene', DISCARDS, ['US.HH-US.HH-Stock model discards-TOT']),
    ('Lagerendring i husholdningene', ['US.HH-US.HH-Stock change-TOT'],
     ['US.HH-US.HH-Stock model stock change-TOT']),
]


def panel_series(df, flows):
    # Medians and percentiles do not add across flows, so the interval of a
    # sum of flows is approximated by summing the flows' own bounds.
    sel = df[df['flow_name'].isin(flows) & df['product'].isin(CORE)]
    return sel.groupby('year')[['median', 'p2_5', 'p97_5']].sum()


def main():
    df = pd.read_csv(SUMMARY)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True, facecolor=SURFACE)
    for ax, (title, statistics, model) in zip(axes, PANELS):
        ax.set_facecolor(SURFACE)
        ends = []
        for flows, color, label in ((statistics, STATISTICS, 'Statistikk'), (model, MODEL, 'Lagermodell')):
            s = panel_series(df, flows)
            ax.fill_between(s.index, s['p2_5'], s['p97_5'], color=color, alpha=0.16, linewidth=0)
            ax.plot(s.index, s['median'], color=color, linewidth=2, label=label)
            ends.append((s['median'].iloc[-1], label, s.index[-1]))
        # Direct labels at the line ends, pushed apart when the lines end close together.
        (y_low, low, x), (y_high, high, _) = sorted(ends)
        gap = max(0.0, 0.06 * (ax.get_ylim()[1] - ax.get_ylim()[0]) - (y_high - y_low)) / 2
        for y, label in ((y_low - gap, low), (y_high + gap, high)):
            ax.annotate(label, (x, y), textcoords='offset points', xytext=(6, 0), va='center',
                        fontsize=8, color=TEXT_MUTED)
        if 'Lagerendring' in title:
            ax.axhline(0, color=TEXT_MUTED, linewidth=1)
        ax.set_title(title, fontsize=10, color=TEXT, loc='left')
        ax.set_ylabel('kt per år', color=TEXT_MUTED, fontsize=9)
        ax.set_xlim(1988, 2029.5)
        ax.grid(axis='y', color=GRID, linewidth=0.8)
        ax.tick_params(colors=TEXT_MUTED, labelsize=8)
        for spine in ('top', 'right'):
            ax.spines[spine].set_visible(False)
        for spine in ('left', 'bottom'):
            ax.spines[spine].set_color(GRID)
    axes[0].legend(frameon=False, fontsize=8, labelcolor=TEXT_MUTED, loc='upper left')

    fig.suptitle('Klær, hjemmetekstiler og sko: statistikk mot parallell lagermodell, 1988–2025 '
                 '(median og 95 %-intervall)', fontsize=11, color=TEXT, x=0.01, ha='left')
    fig.text(0.01, 0.01, 'Statistikk: innsamling + restavfall (D15, D17), lagerendring som restledd (D8). '
             'Lagermodell: tilført × Weibull-levetider (forslag, se lifetimes.csv), innsvinging fra 1950.',
             fontsize=8, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(TARGET, dpi=150, facecolor=SURFACE)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
