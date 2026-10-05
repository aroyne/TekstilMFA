#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates the GitHub Pages site (just-the-docs) from the register and the MC
summaries: one folder per pool with a pool page, one page per subpool and
one page per flow, as in NitrogenBudsjett.

  * Flow pages live under the subpool the flow leaves (imports under RW.RW).
    They hold the register entry, plots (by product and by material), key
    numbers, and the docstring of the function in calculations/ that
    computes the flow, so the documentation in the code is shown as is.
  * Subpool and pool pages hold their flows and a mass balance plot.
  * Text written by hand between <!-- MANUAL:<NAME>:START --> and
    <!-- MANUAL:<NAME>:END --> survives regeneration; everything else on a
    page is rebuilt.

Run main_mc.py with all pools first. Usage: python report_generator.py
"""
import ast
import glob
import os
import re
from datetime import date

import pandas as pd

import utils_stat

PROCESSES_CSV = 'system/processes.csv'
FLOWS_CSV = 'system/flows.csv'
SUMMARY = 'output_files/MC_summary.csv'
FIBRE_SUMMARY = 'output_files/MC_summary_fibre.csv'
PLOT_DIR = 'output_files/plots/pages'
KEY_YEARS = [1990, 2000, 2010, 2018, 2022, 2025]
REPO_URL = 'https://github.com/aroyne/TekstilMFA/blob/main'

FORM_NAMES = {'FIB': 'fibre og garn', 'FAB': 'metervare og halvfabrikata', 'NEW': 'nye varer',
              'MIX': 'brukte, usortert', 'USE': 'brukte, ombrukbare', 'WRN': 'brukte, utslitte',
              'PCW': 'produksjonsavfall', 'MFR': 'mikrofibre'}
DIM_NAMES = {'t': 'år', 'p': 'produkt', 'g': 'produktgruppe'}
FIBRE_RULES = {
    'supply': 'Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).',
    'discards': 'For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. '
                'For andre produkter: tilførselssammensetningen samme år.',
    'mixed': 'Blandingen av alt som går inn i WM.RS samme år.',
}


# --- Pages and manual blocks ----------------------------------------------

def _manual_block(path, name):
    if not os.path.exists(path):
        return None
    text = open(path, encoding='utf-8').read()
    match = re.search(rf'<!-- MANUAL:{name}:START -->\n(.*?)\n<!-- MANUAL:{name}:END -->', text, re.DOTALL)
    return match.group(1) if match else None


def write_page(path, frontmatter, body, manual_name, manual_default):
    """Writes frontmatter + body, keeping the existing manual block if there is one."""
    manual = _manual_block(path, manual_name)
    manual = manual if manual is not None else manual_default
    lines = ['---'] + [f'{k}: {v}' for k, v in frontmatter.items()] + ['---', '']
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n' + body.rstrip() + '\n\n'
                + f'<!-- MANUAL:{manual_name}:START -->\n{manual}\n<!-- MANUAL:{manual_name}:END -->\n')


def _iframe(path, height):
    return f'<iframe src="../{path}" width="100%" height="{height}px" frameborder="0" scrolling="no"></iframe>'


# --- Code documentation ----------------------------------------------------

def flow_functions(paths=None):
    """
    {flow code: (file, function name, line, documentation)} for every
    function in calculations/*_mc.py that assigns a flow, found from the
    source: an assignment to mfa.flows['<code>'].values, directly or through
    a variable bound to mfa.flows['<code>']. The documentation is the
    function's docstring followed by those of the helper functions in the
    same module that it calls (where data sources are often named).
    """
    found = {}
    for path in paths or sorted(glob.glob('calculations/*_mc.py')):
        tree = ast.parse(open(path, encoding='utf-8').read())
        local = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        for func in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
            bound = {}
            for node in ast.walk(func):
                if (isinstance(node, ast.Assign) and len(node.targets) == 1
                        and isinstance(node.targets[0], ast.Name) and _flow_key(node.value)):
                    bound[node.targets[0].id] = _flow_key(node.value)
            for node in ast.walk(func):
                if not isinstance(node, (ast.Assign, ast.AugAssign)):
                    continue
                for target in (node.targets if isinstance(node, ast.Assign) else [node.target]):
                    if not _is_values_target(target):
                        continue
                    for sub in ast.walk(target):
                        code = _flow_key(sub) or (bound.get(sub.id) if isinstance(sub, ast.Name) else None)
                        if code:
                            found.setdefault(code, (path, func.name, func.lineno, _documentation(func, local)))
    return found


def _documentation(func, local):
    parts = [ast.get_docstring(func) or '']
    called = dict.fromkeys(n.func.id for n in ast.walk(func)
                           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in local)
    for name in called:
        doc = ast.get_docstring(local[name])
        if doc and name != func.name:
            parts.append(f'`{name}`: {doc}')
    return '\n\n'.join(p for p in parts if p)


def _flow_key(node):
    """'<code>' if node is <x>.flows['<code>'], else None."""
    if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) and node.value.attr == 'flows'
            and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str)):
        return node.slice.value
    return None


def _is_values_target(target):
    return any(isinstance(n, ast.Attribute) and n.attr == 'values' for n in ast.walk(target))


# --- Register --------------------------------------------------------------

def _snake(text):
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')


def _flow_slug(code):
    source, target, name, _ = code.split('-')
    return _snake(f'{source}_{target}_{name}')


class Site:
    def __init__(self):
        self.processes = pd.read_csv(PROCESSES_CSV)
        self.flows = pd.read_csv(FLOWS_CSV)
        self.summary = pd.read_csv(SUMMARY)
        self.fibre = pd.read_csv(FIBRE_SUMMARY)
        self.functions = flow_functions()
        self.pools = list(dict.fromkeys(self.processes['pool']))
        self.pool_name = dict(zip(self.processes['pool'], self.processes['pool_name']))

    def folder(self, pool):
        return f'{_snake(self.pool_name[pool])}_pool'

    def pool_title(self, pool):
        return f'{self.pools.index(pool) + 1}. {self.pool_name[pool]} ({pool})'

    def subpool_title(self, code):
        row = self.processes.set_index('code').loc[code]
        return f'{row["subpool_name"]} ({code})'

    def subpool_file(self, code):
        return f'subpool_{_snake(code)}.md'

    def subpool_link(self, code):
        pool = code.split('.')[0]
        return f'../{self.folder(pool)}/{self.subpool_file(code)[:-3]}.html'

    def flow_link(self, code):
        pool = code.split('-')[0].split('.')[0]
        return f'../{self.folder(pool)}/flow_{_flow_slug(code)}.html'

    def implemented(self, row):
        return str(row['status']).startswith('implemented')


# --- Flow pages ------------------------------------------------------------

def _key_numbers(summary, code):
    rows = summary[(summary['flow_name'] == code) & summary['product'].isin(['TOTAL', 'ALL'])]
    rows = rows[rows['year'].isin(KEY_YEARS)].set_index('year')
    lines = ['| År | Median (kt) | 95 %-intervall (kt) |', '|---|---|---|']
    for year, r in rows.iterrows():
        lines.append(f"| {year} | {r['median']:.2f} | {r['p2_5']:.2f} – {r['p97_5']:.2f} |")
    return '\n'.join(lines)


def _fibre_rule(code):
    from calculations import fibre_layer
    for key, codes in (('supply', fibre_layer.SUPPLY_FLOWS), ('discards', fibre_layer.DISCARD_FLOWS),
                       ('mixed', fibre_layer.MIXED_FLOWS)):
        if code in codes:
            return FIBRE_RULES[key]
    return ''


def write_flow_page(site, row, nav_order):
    code = row['flow_code']
    pool = row['source'].split('.')[0]
    path = os.path.join(site.folder(pool), f'flow_{_flow_slug(code)}.md')
    dims = ' × '.join(DIM_NAMES[d] for d in str(row['dims']).split(',')) if site.implemented(row) else '–'
    table = [
        '| | |', '|---|---|',
        f"| Flytkode | `{code}` |",
        f"| Fra | [{site.subpool_title(row['source'])}]({site.subpool_link(row['source'])}) |",
        f"| Til | [{site.subpool_title(row['target'])}]({site.subpool_link(row['target'])}) |",
        f"| Tekstilform | {row['form']} – {FORM_NAMES[row['form']]} |",
        f"| Dimensjoner | {dims} |",
        f"| Metode | {row['method']} |",
        f"| Status | {row['status']} |",
        f"| Prioritet | {row['priority']} |",
        f"| Kandidatdata | {row['candidate_data'] if pd.notna(row['candidate_data']) else '–'} |",
        f"| Merknad | {row['note'] if pd.notna(row['note']) else '–'} |",
    ]
    body = [f"# {row['name']}", '', '\n'.join(table), '']
    if site.implemented(row):
        slug = _flow_slug(code)
        plot = f'{PLOT_DIR}/{slug}.html'
        fibre_plot = f'{PLOT_DIR}/{slug}_materials.html'
        utils_stat.plot_flow(site.summary, code, f"{row['name']} – per produkt (median, 95 % for summen)", plot)
        utils_stat.plot_flow_materials(site.fibre, code, f"{row['name']} – per materiale (median)", fibre_plot)
        body += ['## Tidsserie', '', _iframe(plot, 420), '', '## Nøkkeltall (sum over produkter)', '',
                 _key_numbers(site.summary, code), '',
                 '## Materialsammensetning (fiberlag, D19)', '', _fibre_rule(code), '', _iframe(fibre_plot, 420), '']
        if code in site.functions:
            file, func, line, doc = site.functions[code]
            quoted = '\n'.join('> ' + l if l else '>' for l in doc.splitlines())
            body += ['## Beregning i koden', '',
                     f'Beregnes i `{func}` i [{file}]({REPO_URL}/{file}#L{line}). Dokumentasjonen i koden:', '',
                     quoted, '']
    else:
        body += ['*Flyten er ikke implementert ennå.*', '']
    body += ['## Beskrivelse', '']
    frontmatter = {'layout': 'default', 'title': row['name'], 'parent': site.subpool_title(row['source']),
                   'grand_parent': site.pool_title(pool), 'nav_order': nav_order}
    write_page(path, frontmatter, '\n'.join(body), 'FLOW_DESCRIPTION', '*Ingen manuell beskrivelse ennå.*')


# --- Subpool and pool pages ------------------------------------------------

def _flow_lines(site, rows, direction):
    lines = []
    for _, r in rows.iterrows():
        other = r['target'] if direction == 'out' else r['source']
        status = '' if site.implemented(r) else ' *(planlagt)*'
        lines.append(f"* [{r['name']}]({site.flow_link(r['flow_code'])}) "
                     f"{'→' if direction == 'out' else '←'} {other}{status}")
    return '\n'.join(lines) if lines else '*Ingen.*'


def _stock_outputs(site, code):
    names = [f'{code}-{code}-Stock change-TOT']
    return [(f'Lagerendring {code}', n) for n in names if n in set(site.summary['flow_name'])]


def write_subpool_page(site, proc, nav_order):
    code = proc['code']
    pool = proc['pool']
    flows = site.flows
    inflows = flows[flows['target'] == code]
    outflows = flows[flows['source'] == code]
    body = [f"# {site.subpool_title(code)}", '', proc['description'], '',
            f"Type: {proc['type']}. Lager: {proc['has_stock']}.", '',
            '## Flyter ut', '', _flow_lines(site, outflows, 'out'), '',
            '## Flyter inn', '', _flow_lines(site, inflows, 'in'), '']
    impl_in = [(r['name'], r['flow_code']) for _, r in inflows.iterrows() if site.implemented(r)]
    impl_out = [(r['name'], r['flow_code']) for _, r in outflows.iterrows() if site.implemented(r)]
    if impl_in or impl_out:
        plot = f'{PLOT_DIR}/balance_{_snake(code)}.html'
        utils_stat.plot_balance(site.summary, impl_in, impl_out, _stock_outputs(site, code),
                                f'Massebalanse {code} (median; inn over null, ut og lagerendring under)', plot)
        body += ['## Massebalanse', '', _iframe(plot, 500), '']
    if code == 'US.HH':
        stock_plot = f'{PLOT_DIR}/stock_us_hh.html'
        utils_stat.plot_flow(site.summary, 'US.HH-US.HH-Stock-TOT',
                             'Lager i husholdningene, CL+HT+FW (startlager fra lagermodellen + restledd)', stock_plot)
        body += ['## Lager og parallell lagermodell (D8)', '', _iframe(stock_plot, 420), '',
                 '![Statistikk mot lagermodell](../output_files/plots/stock_model_comparison.png)', '',
                 'Se også [notatet om lagermodellen mot statistikken]'
                 f'({REPO_URL}/claude_tekst/2026-10-05_lagermodell_mot_statistikk.md).', '']
    body += ['## Merknader', '']
    frontmatter = {'layout': 'default', 'title': site.subpool_title(code), 'parent': site.pool_title(pool),
                   'nav_order': nav_order, 'has_children': 'true'}
    write_page(os.path.join(site.folder(pool), site.subpool_file(code)), frontmatter, '\n'.join(body),
               'POOL_TEXT', '*Ingen manuelle merknader ennå.*')


def write_pool_page(site, pool, nav_order):
    procs = site.processes[site.processes['pool'] == pool]
    links = '\n'.join(f"* [{site.subpool_title(c)}]({site.subpool_file(c)[:-3]}.html)" for c in procs['code'])
    body = [f'# {site.pool_title(pool)}', '', 'Subpooler:', '', links, '']
    flows = site.flows[site.flows.apply(site.implemented, axis=1)]
    pool_of = lambda c: c.split('.')[0]
    inflows = flows[(flows['target'].map(pool_of) == pool) & (flows['source'].map(pool_of) != pool)]
    outflows = flows[(flows['source'].map(pool_of) == pool) & (flows['target'].map(pool_of) != pool)]
    if not inflows.empty or not outflows.empty:
        stocks = [s for c in procs['code'] for s in _stock_outputs(site, c)]
        plot = f'{PLOT_DIR}/balance_pool_{_snake(pool)}.html'
        utils_stat.plot_balance(site.summary, list(zip(inflows['name'], inflows['flow_code'])),
                                list(zip(outflows['name'], outflows['flow_code'])), stocks,
                                f'Massebalanse for poolen {pool} (flyter over poolgrensen)', plot)
        body += ['## Massebalanse', '', _iframe(plot, 500), '']
    body += ['## Merknader', '']
    frontmatter = {'layout': 'default', 'title': site.pool_title(pool), 'nav_order': nav_order + 1,
                   'has_children': 'true'}
    write_page(os.path.join(site.folder(pool), f'pool_{_snake(site.pool_name[pool])}.md'), frontmatter,
               '\n'.join(body), 'POOL_TEXT', '*Ingen manuelle merknader ennå.*')


# --- Landing page and config -----------------------------------------------

CONFIG = """remote_theme: just-the-docs/just-the-docs
title: Tekstil-MFA Norge
description: Dynamisk, probabilistisk materialstrømanalyse av tekstiler i Norge 1988–2025
nav_sort: case_insensitive
nav_exclude:
  - /index.md
include:
  - output_files
exclude:
  - data_files
  - litteratur
  - tests
  - "*.csv.gz"
"""


def write_index(site):
    pools = '\n'.join(f"* [{site.pool_title(p)}]({site.folder(p)}/pool_{_snake(site.pool_name[p])}.html)"
                      for p in site.pools)
    body = [
        '# Tekstil-MFA for Norge', '', f'**Sist generert:** {date.today().isoformat()}', '',
        '{: .label .label-red }', 'Under arbeid', '',
        '> Modellen, dataene og resultatene er under utvikling og ikke validert. Ikke bruk tallene '
        'til forskning eller beslutninger ennå.', '',
        'Dynamisk, probabilistisk MFA (Monte Carlo, flodym) for klær, hjemmetekstiler, sko og andre '
        'tekstilvarer i Norge, 1988–2025. Hver flyt har en egen side med tidsserie, usikkerhet, '
        'fibersammensetning og dokumentasjon fra koden. Systemdefinisjon, metode og plan står i '
        f'[SYSTEMDEFINISJON]({REPO_URL}/docs/SYSTEMDEFINISJON.md), [METODE]({REPO_URL}/docs/METODE.md) og '
        f'[PLAN]({REPO_URL}/docs/PLAN.md).', '',
        '## Pools', '', pools, '',
        '## Kjerneflyter i husholdningene', '',
        '![Kjerneflyter](output_files/plots/core_household_flows.png)', '',
        '## Statistikk mot parallell lagermodell', '',
        '![Lagermodell](output_files/plots/stock_model_comparison.png)', '',
    ]
    write_page('index.md', {'layout': 'default', 'title': 'Hjem', 'nav_order': 1}, '\n'.join(body),
               'INDEX_TEXT', '')


def main():
    site = Site()
    if not os.path.exists('_config.yml'):
        open('_config.yml', 'w', encoding='utf-8').write(CONFIG)
    write_index(site)
    for i, pool in enumerate(site.pools, start=1):
        os.makedirs(site.folder(pool), exist_ok=True)
        write_pool_page(site, pool, i)
        for j, (_, proc) in enumerate(site.processes[site.processes['pool'] == pool].iterrows(), start=1):
            write_subpool_page(site, proc, j)
            outflows = site.flows[site.flows['source'] == proc['code']]
            for k, (_, row) in enumerate(outflows.iterrows(), start=1):
                write_flow_page(site, row, k)
    n_flows = len(site.flows)
    print(f"[INFO] Wrote {len(site.pools)} pool pages, {len(site.processes)} subpool pages and {n_flows} flow pages")


if __name__ == '__main__':
    main()
