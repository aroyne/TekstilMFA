import pandas as pd

flows = pd.read_csv('system/flows.csv')
processes = pd.read_csv('system/processes.csv')


def test_flow_code_fields_match_columns():
    parts = flows['flow_code'].str.split('-')
    assert (parts.str.len() == 4).all(), "flow names must not contain '-'"
    assert (parts.str[0] == flows['source']).all()
    assert (parts.str[1] == flows['target']).all()
    assert (parts.str[2] == flows['name']).all()
    assert (parts.str[3] == flows['layer']).all()


def test_flows_only_connect_registered_processes():
    codes = set(processes['code'])
    assert set(flows['source']) <= codes
    assert set(flows['target']) <= codes


def test_flow_codes_unique():
    assert flows['flow_code'].is_unique


def test_hs_mapping_finished_products_match_product_list():
    from calculations.utils import PRODUCTS
    mapping = pd.read_csv('parameters/hs_mapping.csv', dtype={'hs_prefix': str})
    finished = mapping[(mapping['category'] == 'finished') & (mapping['in_scope'] == 'yes')]
    assert set(finished['product']) == set(PRODUCTS)


def test_implemented_flows_have_valid_dims():
    implemented = flows[flows['status'].str.startswith('implemented')]
    for code, dims in zip(implemented['flow_code'], implemented['dims']):
        assert isinstance(dims, str), f"{code} has no dims"
        letters = dims.split(',')
        assert letters[0] == 't' and set(letters) <= {'t', 'p', 'g'}, f"{code}: {dims}"
        assert not {'p', 'g'} <= set(letters), f"{code} has both product and product group"


def test_stocks_and_sinks_have_stock_dims():
    needs = processes[(processes['has_stock'] == 'yes') | (processes['type'] == 'sink')]
    assert needs['stock_dims'].notna().all()
