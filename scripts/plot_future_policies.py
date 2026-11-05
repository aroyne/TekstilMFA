#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Measures in the future scenarios (phase D, step 3): per target, the median
and the 5-95 percentile range over the scenarios for each alternative, the
threshold, and the share of scenarios that meet it (satisficing). The
range is what is possible under the spans of the factors and effects, not
a confidence interval.

Usage: python scripts/plot_future_policies.py  ->  output_files/plots/future_policies.png
Run future_policies.py first.
"""
import matplotlib.pyplot as plt
import pandas as pd

SOURCE = 'output_files/future_policies_robustness.csv'
TARGET = 'output_files/plots/future_policies.png'

MARK = '#2a78d6'
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'

ALTERNATIVES = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'Lall']
LABELS = {'L0': 'L0 ingen nye tiltak', 'L1': 'L1 produsentansvar', 'L2': 'L2 sortering i Norge',
          'L3': 'L3 holdbarhet', 'L4': 'L4 destruksjonsforbud', 'L5': 'L5 avgift / mot ultrarask mote',
          'Lall': 'Alle (L1–L5)'}
# (metric, basis, title, scale, unit)
PANELS = [
    ('collection_rate_recorded', 'recorded', 'Innsamlingsgrad 2035 (målt)', 100, '%'),
    ('collection_rate', 'with D42', 'Innsamlingsgrad 2035 (med næringsavfall)', 100, '%'),
    ('unsorted_export_share', 'recorded', 'Andel eksportert usortert 2035', 100, '%'),
    ('reuse_in_norway_kt', 'recorded', 'Ombruk i Norge 2035', 1, 'kt'),
    ('incineration_recorded_kt', 'recorded', 'Til forbrenning 2035 (målt)', 1, 'kt'),
    ('household_discards_recorded_kt', 'recorded', 'Kassert fra husholdningene 2040 (målt)', 1, 'kt'),
]


def main():
    table = pd.read_csv(SOURCE)
    fig, axes = plt.subplots(2, 3, figsize=(14, 7.5), facecolor=SURFACE)
    for ax, (metric, basis, title, scale, unit) in zip(axes.flat, PANELS):
        ax.set_facecolor(SURFACE)
        rows = table[(table['metric'] == metric) & (table['basis'] == basis)].set_index('alternative')
        threshold = float(rows['target'].iloc[0].split()[1]) * scale
        for i, name in enumerate(ALTERNATIVES):
            y = len(ALTERNATIVES) - 1 - i
            r = rows.loc[name]
            ax.plot([r['p5'] * scale, r['p95'] * scale], [y, y], color=MARK, linewidth=2, alpha=0.45,
                    solid_capstyle='round')
            ax.plot(r['median'] * scale, y, 'o', color=MARK, markersize=7, markeredgecolor=SURFACE,
                    markeredgewidth=2)
            ax.annotate(f"{r['satisficing']:.0%}", (1.0, y), xycoords=('axes fraction', 'data'),
                        xytext=(6, 0), textcoords='offset points', va='center', fontsize=8, color=TEXT_MUTED)
        ax.axvline(threshold, color=TEXT_MUTED, linewidth=1, linestyle='--')
        ax.set_yticks(range(len(ALTERNATIVES)))
        ax.set_yticklabels([LABELS[a] for a in reversed(ALTERNATIVES)] if ax in axes[:, 0] else [], fontsize=8,
                           color=TEXT_MUTED)
        ax.tick_params(axis='y', length=0)
        ax.set_title(title, fontsize=10, color=TEXT, loc='left')
        ax.set_xlabel(f"{unit}  (stiplet: terskel {rows['target'].iloc[0].split()[0]} {threshold:.3g})",
                      fontsize=8, color=TEXT_MUTED)
        ax.set_xlim(left=0)
        ax.grid(axis='x', color=GRID, linewidth=0.8)
        ax.tick_params(axis='x', colors=TEXT_MUTED, labelsize=8)
        for spine in ('top', 'right', 'left'):
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color(GRID)
    fig.suptitle('Ambisiøse tiltak i 1 000 fremtidsscenarier: median, 5–95-persentil og andel scenarier som '
                 'når målet (tall til høyre)', fontsize=11, color=TEXT, x=0.01, ha='left')
    fig.text(0.01, 0.01, '«Målt» er som statistikken (uten husholdningstekstiler i næringsavfall og grovavfall, '
             'D42); tersklene er sammenlignet med 2025. Spennene er det som er mulig, ikke sannsynligheter.',
             fontsize=8, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.03, 0.98, 0.95))
    fig.savefig(TARGET, dpi=150, facecolor=SURFACE)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
