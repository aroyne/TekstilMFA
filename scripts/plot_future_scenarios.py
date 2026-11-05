#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fan chart of the future scenarios (phase D, step 2): history (iteration 0),
the reference path, and the 5-95 percentile and min-max range over the
Latin hypercube scenarios, for six of the metrics. The band is a range of
what is possible under the spans of the uncertain factors, not a
confidence interval.

Usage: python scripts/plot_future_scenarios.py  ->  output_files/plots/future_scenarios.png
Run main_future.py and future_scenarios.py first.
"""
import matplotlib.pyplot as plt
import pandas as pd

SUMMARY = 'output_files/future_scenarios_summary.csv'
REFERENCE = 'output_files/future_reference.csv'
TARGET = 'output_files/plots/future_scenarios.png'

LINE = '#2a78d6'
SURFACE = '#fcfcfb'
TEXT = '#0b0b0b'
TEXT_MUTED = '#52514e'
GRID = '#e4e3df'

CORE = ['CL', 'HT', 'FW', 'YA', 'CORE']
DISCARDS = ['US.HH-CO.CO-Separate collection from households-TOT',
            'US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT',
            'US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT',
            'US.HH-WM.RS-Household textiles in commercial and bulky waste-TOT']
# metric: (title, unit, scale, history flows (product filter), history scale)
PANELS = {
    'collection_rate': ('Innsamlingsgrad, husholdninger', '%', 100,
                        (['Separate collection rate, households, CORE (share)'], ['ALL'])),
    'household_discards_kt': ('Kassert fra husholdningene (CL+HT+FW)', 'kt per år', 1, (DISCARDS, CORE)),
    'reuse_in_norway_kt': ('Ombruk i Norge (salg av brukt)', 'kt per år', 1,
                           (['CO.RE-US.HH-Secondhand sales to households-TOT'], CORE)),
    'material_recycling_kt': ('Materialgjenvinning', 'kt per år', 1,
                              (['CO.SO-WM.RC-Sorted for recycling-TOT',
                                'US.IC-WM.RC-Institutional textiles to recycling-TOT',
                                'MA.TX-WM.RC-Production waste to recycling-TOT'], CORE + ['ALL', 'TOTAL'])),
    'incineration_kt': ('Til forbrenning (Norge og utlandet)', 'kt per år', 1,
                        (['WM.RS-WM.IN-Domestic incineration-TOT',
                          'WM.RS-RW.RW-Residual waste export for incineration-TOT'], ['ALL'])),
    # The level depends on the lifetimes through the stock at the start
    # (D2), so the change per year is shown.
    'household_stock_change_kt': ('Lagerendring i husholdningene (restledd)', 'kt per år', 1,
                                  (['US.HH-US.HH-Stock change-TOT'], ['CORE'])),
}


def history_series(reference, flows, products):
    sel = reference[reference['flow_name'].isin(flows) & reference['product'].isin(products)
                    & (reference['period'] == 'history')]
    # Product rows and their TOTAL row must not both be summed.
    if 'TOTAL' in products:
        sel = sel[~((sel['product'] == 'TOTAL') & sel['flow_name'].isin(
            sel.loc[sel['product'] != 'TOTAL', 'flow_name']))]
    return sel.groupby('year')['value'].sum()


def main():
    summary = pd.read_csv(SUMMARY)
    reference = pd.read_csv(REFERENCE)
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.2), facecolor=SURFACE)
    for ax, (metric, (title, unit, scale, (flows, products))) in zip(axes.flat, PANELS.items()):
        ax.set_facecolor(SURFACE)
        s = summary[summary['metric'] == metric].set_index('year')
        hist = history_series(reference, flows, products) * scale
        ax.fill_between(s.index, s['min'] * scale, s['max'] * scale, color=LINE, alpha=0.10, linewidth=0)
        ax.fill_between(s.index, s['p5'] * scale, s['p95'] * scale, color=LINE, alpha=0.22, linewidth=0)
        ax.plot(hist.index, hist.values, color=LINE, linewidth=2)
        ax.plot(s.index, s['reference'] * scale, color=LINE, linewidth=2, linestyle='--')
        ax.axvline(2025.5, color=TEXT_MUTED, linewidth=1, linestyle=':')
        if s['min'].min() >= 0:
            ax.set_ylim(bottom=0)
        else:
            ax.axhline(0, color=TEXT_MUTED, linewidth=1)
        ax.set_xlim(2000, 2050)
        ax.set_title(title, fontsize=10, color=TEXT, loc='left')
        ax.set_ylabel(unit, color=TEXT_MUTED, fontsize=9)
        ax.grid(axis='y', color=GRID, linewidth=0.8)
        ax.tick_params(colors=TEXT_MUTED, labelsize=8)
        for spine in ('top', 'right'):
            ax.spines[spine].set_visible(False)
        for spine in ('left', 'bottom'):
            ax.spines[spine].set_color(GRID)
    fig.suptitle('Fremtidsscenarier 2026–2050 uten nye tiltak: historikk, referansebane og spenn over 1 000 '
                 'scenarier', fontsize=11, color=TEXT, x=0.01, ha='left')
    fig.text(0.01, 0.01, 'Heltrukket: historikk (iterasjon 0). Stiplet: referansebane (2025-verdier videreført). '
             'Mørkt bånd: 5–95-persentil, lyst bånd: min–maks over scenariene (spenn, ikke sannsynlighet).\n'
             'Fra 2026 er husholdningstekstiler i næringsavfall og grovavfall (D42) med i kasseringene og i nevneren '
             'for innsamlingsgraden; spranget i 2026 er et brudd i definisjonen.', fontsize=8, color=TEXT_MUTED)
    fig.tight_layout(rect=(0, 0.045, 1, 0.95))
    fig.savefig(TARGET, dpi=150, facecolor=SURFACE)
    print(f"Wrote {TARGET}")


if __name__ == '__main__':
    main()
