#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measures in the future scenarios (phase D, steps 3 and 4): per target, the
median and the 5-95 percentile range over the scenarios for each
alternative under both demands (supply-driven and stock-driven), the
threshold, and the share of scenarios that meet it (satisficing). The
range is what is possible under the spans of the factors and effects, not
a confidence interval.

Usage: python scripts/plot_future_policies.py  ->  output_files/plots/future_policies.png
Run future_policies.py first.
"""
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

SOURCE = 'output_files/future_policies_robustness.csv'
TARGET = 'output_files/plots/future_policies.png'

SERIES = {'supply': ('#2a78d6', 'Tilførselsdrevet etterspørsel'), 'stock': ('#eb6834', 'Lagerdrevet etterspørsel')}
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'

ALTERNATIVES = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'Lall']
LABELS = {'L0': 'L0 ingen nye tiltak', 'L1': 'L1 produsentansvar', 'L2': 'L2 sortering i Norge',
          'L3': 'L3 holdbarhet', 'L4': 'L4 destruksjonsforbud', 'L5': 'L5 avgift / ultrarask mote',
          'L6': 'L6 ombruk i Norge', 'L7': 'L7 reparasjon', 'L8': 'L8 utleie og deling',
          'L9': 'L9 resirkulert innhold', 'Lall': 'Alle (L1–L9)'}
# (metric, title, scale, unit)
PANELS = [
    ('new_goods_kg_per_capita', 'Ny tilførsel per innbygger 2035', 1, 'kg'),
    ('virgin_fibre_kg_per_capita', 'Jomfruelig fiber per innbygger 2035', 1, 'kg'),
    ('collection_rate', 'Innsamlingsgrad 2035 (med næringsavfall)', 100, '%'),
    ('reuse_in_norway_kt', 'Ombruk i Norge 2035', 1, 'kt'),
    ('incineration_recorded_kt', 'Til forbrenning 2035 (målt)', 1, 'kt'),
    ('household_discards_recorded_kt', 'Kassert fra husholdningene 2040 (målt)', 1, 'kt'),
]
OFFSET = {'supply': 0.18, 'stock': -0.18}


def main():
    table = pd.read_csv(SOURCE)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), facecolor=SURFACE)
    for ax, (metric, title, scale, unit) in zip(axes.flat, PANELS):
        ax.set_facecolor(SURFACE)
        rows = table[table['metric'] == metric]
        target = rows['target'].iloc[0]
        threshold = float(target.split()[1]) * scale
        for demand, (color, _) in SERIES.items():
            sel = rows[rows['demand'] == demand].set_index('alternative')
            for i, name in enumerate(ALTERNATIVES):
                y = len(ALTERNATIVES) - 1 - i + OFFSET[demand]
                r = sel.loc[name]
                ax.plot([r['p5'] * scale, r['p95'] * scale], [y, y], color=color, linewidth=2, alpha=0.45,
                        solid_capstyle='round')
                ax.plot(r['median'] * scale, y, 'o', color=color, markersize=6, markeredgecolor=SURFACE,
                        markeredgewidth=1.5)
                ax.annotate(f"{r['satisficing']:.0%}", (1.0, y), xycoords=('axes fraction', 'data'),
                            xytext=(4, 0), textcoords='offset points', va='center', fontsize=7, color=TEXT_MUTED)
        ax.axvline(threshold, color=TEXT_MUTED, linewidth=1, linestyle='--')
        ax.set_yticks(range(len(ALTERNATIVES)))
        ax.set_yticklabels([LABELS[a] for a in reversed(ALTERNATIVES)] if ax in axes[:, 0] else [], fontsize=8,
                           color=TEXT_MUTED)
        ax.tick_params(axis='y', length=0)
        ax.set_title(title, fontsize=10, color=TEXT, loc='left')
        ax.set_xlabel(f"{unit}  (stiplet: terskel {target.split()[0]} {threshold:.3g})", fontsize=8,
                      color=TEXT_MUTED)
        ax.set_xlim(left=0)
        ax.grid(axis='x', color=GRID, linewidth=0.8)
        ax.tick_params(axis='x', colors=TEXT_MUTED, labelsize=8)
        for spine in ('top', 'right', 'left'):
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color(GRID)
    handles = [Line2D([0], [0], color=c, marker='o', linewidth=2, label=l) for c, l in SERIES.values()]
    fig.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.01, 0.955), frameon=False, fontsize=9,
               labelcolor=TEXT_MUTED, ncol=2)
    fig.suptitle('Ambisiøse tiltak i 1 000 fremtidsscenarier, to formuleringer av etterspørselen: median, '
                 '5–95-persentil og andel scenarier som når målet (tall til høyre)', fontsize=11, color=TEXT,
                 x=0.01, ha='left')
    fig.text(0.01, 0.01, '«Målt» er som statistikken (uten husholdningstekstiler i næringsavfall og grovavfall, '
             'D42); tersklene er sammenlignet med 2025 (ny tilførsel og jomfruelig fiber: −30 %). Spennene er det som '
             'er mulig, ikke sannsynligheter.', fontsize=8, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.02, 0.98, 0.925))
    fig.savefig(TARGET, dpi=150, facecolor=SURFACE)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
