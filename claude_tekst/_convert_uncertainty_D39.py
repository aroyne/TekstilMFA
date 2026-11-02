"""One-off conversion of the parameter tables to the D39 uncertainty scheme.

Adds source_type (1-4), bounds ('' = 95 %, 'minmax') and, for anchors,
method_group and common_share. Sets distribution_type by the rule in
calculations/sampling.py: type 4 -> uniform minmax; otherwise normal for
symmetric bounds up to 40 %, lognormal for log-symmetric bounds,
triangular otherwise (minmax when the solved minimum would be < 0, the
maximum > 1 for a share, or the bounds are a literature range).
Run from the project root with --apply to write.
"""
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, '.')
from calculations.sampling import absolute_bounds, triangular_minmax_from_95  # noqa: E402

APPLY = '--apply' in sys.argv

# id -> (source_type, bounds, justification). bounds None = decided by rule.
GLOBAL = {
    'nontextile_share_CL': (2, 'minmax', 'PEFCR measurements, range of reference products'),
    'nontextile_share_HT': (4, None, 'assumption'),
    'nontextile_share_FW': (2, 'minmax', 'PEFCR measurements, range of reference products'),
    'nontextile_share_CA': (4, None, 'assumption'),
    'nontextile_share_TA': (4, None, 'assumption'),
    'nontextile_share_OM': (4, None, 'assumption'),
    'institutional_share': (4, None, 'Danish estimate used for Norway; lower bound from Eurostat TEC (D36)'),
    'retail_markup': (4, None, 'assumption'),
    'crossborder_clothing_share': (2, 'minmax', 'SSB 14221 survey, range over years'),
    'nontextile_share_SA': (4, None, 'assumption'),
    'mmf_synthetic_share': (3, 'minmax', 'global market statistics, not Norwegian imports'),
    'wool_scouring_loss_share': (2, 'minmax', 'literature range of measured losses'),
    'nontextile_share_YA': (4, None, 'assumption'),
    'air_release_relative_to_laundry': (3, None, 'single studies; factor of about 3 either way'),
    'gap_cv_extrapolation': (4, None, 'assumption (D30)'),
    'gap_cv_interpolation': (4, None, 'assumption (D30)'),
    'gap_cv_cap': (4, None, 'assumption (D30)'),
    'ntg_fibre_domestic_share': (4, None, 'assumption'),
}

# parameter_id -> (source_type, bounds, method_group, common_share, justification)
ANCHORS = {
    'lowvalue_undercoverage_CL': (4, None, '', np.nan, 'sensitivity only (D14)'),
    'landfill_share_residual': (3, None, 'ssb_landfill', 0.5,
                                'SSB waste accounts (model-based statistics), same method each year'),
    'retained_share_collected': (2, None, 'collector_survey', 0.5, 'collector survey'),
    'reuse_fraction_retained': (4, None, '', np.nan, 'assumption on the share reused'),
    'residual_export_share': (3, None, 'ssb_residual_export', 0.5, 'SSB waste statistics, same method each year'),
    'reusable_share_residual': (2, 'minmax', 'pick_analysis_reusable', 0.5, 'pick analyses, spread between analyses'),
    'online_direct_CL': (3, None, 'voec', 0.5, 'VOEC registered by Tolletaten, mass not measured directly'),
    'online_direct_HT': (3, None, 'voec', 0.5, 'VOEC registered by Tolletaten, mass not measured directly'),
    'residual_core': (2, None, 'mepex_pick_analysis', 0.5, 'Mepex pick analyses scaled up by NORSUS'),
    'wool_scoured_domestic': (2, None, 'period', 1.0, 'mean over a period; both ends of a period share one draw'),
    'preconsumer_waste_textile_industry': (3, 'minmax', '', np.nan, 'SSB 08604, rounded to whole kt'),
    'unsold_donated': (2, None, 'unsold_survey', 0.5, 'collector reports'),
    'unsold_discarded': (2, None, 'unsold_survey', 0.5, 'survey minimum; large chains did not answer'),
    'laundry_release_synthetic': (4, None, '', np.nan, 'order-of-magnitude estimate (Mepex 2014)'),
    'recycling_share_sorting_rejects': (2, None, '', np.nan, 'single survey'),
    'recycling_institutional': (3, None, 'ntg_figures', 0.5, 'read from figures; split by intake share'),
    'recycling_production_waste': (3, None, 'ntg_figures', 0.5, 'read from figures; split by intake share'),
    'recycling_ntg_fibre': (1, None, 'ntg_figures', 0.5, 'reported by the plant'),
}

DATASETS = {  # name -> (source_type, annual_draw, justification)
    '08801': (1, 'yes', 'registered customs declarations; errors mostly new each year'),
    'grensehandel': (2, 'yes', 'quarterly survey'),
    'totalkalkylen': (1, 'yes', 'weighed-in wool at the wool stations'),
    'vareproduksjon': (2, 'no', 'large units only; the coverage error is systematic'),
    '08801_classification': (4, 'no', 'assumption: goods under a code that do not belong to its product group'),
}

LIFETIME_JUSTIFICATION = 'literature proposal; calibrated in phase C'


def rule(val, row, source_type, bounds, is_share):
    """(distribution_type, bounds) for one perturbed row."""
    if source_type == 4:
        return 'uniform', 'minmax'
    low, high = absolute_bounds(val, row)
    if bounds == 'minmax':
        return 'triangular', 'minmax'
    if low <= 0 or val <= 0:
        return 'triangular', 'minmax'
    d_lo, d_hi = val - low, high - val
    if abs(d_lo - d_hi) > 0.1 * (high - low):
        if abs(np.log(val / low) - np.log(high / val)) <= 0.1 * np.log(high / low):
            return 'lognormal', ''
        dist = 'triangular'
    elif d_hi / val <= 0.40 and not (is_share and val + 1.9 * d_hi > 1):
        return 'normal', ''
    else:
        dist = 'triangular'
    if val <= low or val >= high:
        return 'triangular', 'minmax'
    a, b = triangular_minmax_from_95(val, low, high)
    if a < 0 or (is_share and b > 1):
        return 'triangular', 'minmax'
    return dist, ''


def perturbed(row):
    return not (pd.isna(row['lower_bound']) or pd.isna(row['upper_bound'])
                or (row['lower_bound'] == 0 and row['upper_bound'] == 0))


def convert(df, id_col, table, value_col='value'):
    df = df.copy()
    for col in ('source_type', 'bounds'):
        df[col] = '' if col == 'bounds' else np.nan
    for i, row in df.iterrows():
        spec = table[row[id_col]]
        source_type, bounds = spec[0], spec[1]
        df.at[i, 'source_type'] = source_type
        df.at[i, 'uncertainty_source'] = spec[-1]
        if pd.isna(row[value_col]) or not perturbed(row):
            df.at[i, 'distribution_type'] = 'none'
            continue
        is_share = str(row.get('unit', '')) in ('kg/kg', '-', 'share') or 'share' in str(row[id_col])
        dist, b = rule(float(row[value_col]), row, source_type, bounds, is_share)
        df.at[i, 'distribution_type'] = dist
        df.at[i, 'bounds'] = b
    df['source_type'] = df['source_type'].astype('Int64')
    return df


def move_after(df, cols, after):
    rest = [c for c in df.columns if c not in cols]
    i = rest.index(after) + 1
    return df[rest[:i] + cols + rest[i:]]


g = pd.read_csv('parameters/global_parameters.csv')
g = move_after(convert(g, 'parameter_id', GLOBAL), ['bounds', 'source_type'], 'distribution_type')

frames = {}
for path in ('parameters/time_dependent_parameters.csv', 'data_files/anchor_values.csv'):
    a = pd.read_csv(path)
    a = convert(a, 'parameter_id', {k: (v[0], v[1], v[4]) for k, v in ANCHORS.items()})
    a['method_group'] = a['parameter_id'].map(lambda p: ANCHORS[p][2])
    a['common_share'] = a['parameter_id'].map(lambda p: ANCHORS[p][3])
    # Both ends of a wool period are one mean: one group per period value.
    wool = a['parameter_id'] == 'wool_scoured_domestic'
    a.loc[wool, 'method_group'] = 'wool_' + a.loc[wool, 'value'].astype(str)
    laitala = (a['parameter_id'] == 'residual_core') & (a['year'] == 2009)
    a.loc[laitala, ['method_group', 'common_share', 'source_type']] = ['', np.nan, 3]
    a.loc[laitala, 'uncertainty_source'] = 'Laitala et al. 2012, Oslo pick analyses scaled to Norway'
    frames[path] = move_after(a, ['bounds', 'source_type', 'method_group', 'common_share'], 'distribution_type')

d = pd.read_csv('parameters/dataset_uncertainties.csv', dtype={'dataset_name': str})
if '08801_classification' not in set(d['dataset_name']):
    d.loc[len(d)] = {'dataset_name': '08801_classification', 'source': 'assumption', 'lower_bound': 5,
                     'upper_bound': 5, 'uncertainty_type': 'perc', 'distribution_type': 'uniform',
                     'status': 'assumption'}
d['source_type'] = d['dataset_name'].map(lambda n: DATASETS[n][0])
d['annual_draw'] = d['dataset_name'].map(lambda n: DATASETS[n][1])
d['uncertainty_source'] = d['dataset_name'].map(lambda n: DATASETS[n][2])
rules = [rule(1.0, r, s, None, False) for (_, r), s in zip(d.iterrows(), d['source_type'])]
d['distribution_type'] = [r[0] for r in rules]
d['bounds'] = [r[1] for r in rules]
d = move_after(d, ['bounds', 'source_type', 'annual_draw'], 'distribution_type')

lt = pd.read_csv('parameters/lifetimes.csv')
lt['source_type'] = np.where(lt['mean_years'].notna(), 4, np.nan)
lt['source_type'] = lt['source_type'].astype('Int64')
lt['uncertainty_source'] = np.where(lt['mean_years'].notna(), LIFETIME_JUSTIFICATION, '')
lt['mean_distribution'] = np.where(lt['mean_years'].notna(), 'uniform', 'none')
lt['bounds'] = np.where(lt['mean_years'].notna(), 'minmax', '')
lt = move_after(lt, ['mean_distribution', 'bounds', 'source_type'], 'upper_bound')

pd.set_option('display.width', 250)
pd.set_option('display.max_rows', 300)
pd.set_option('display.max_columns', 20)
print(g[['parameter_id', 'value', 'lower_bound', 'upper_bound', 'distribution_type', 'bounds', 'source_type']])
for path, a in frames.items():
    print(a[['parameter_id', 'year', 'value', 'lower_bound', 'upper_bound', 'uncertainty_type',
             'distribution_type', 'bounds', 'source_type', 'method_group']])
print(d)
if APPLY:
    g.to_csv('parameters/global_parameters.csv', index=False)
    for path, a in frames.items():
        a.to_csv(path, index=False)
    d.to_csv('parameters/dataset_uncertainties.csv', index=False)
    lt.to_csv('parameters/lifetimes.csv', index=False)
    print('written')
