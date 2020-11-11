import io
from io import StringIO

import pytest

from autogen_configs.generation import read_csv, generate_state_configs, combine


@pytest.fixture
def csv_file():
    csv = """TYPE,MODEL,STATE,STATECODE,NAMELSAD,COUNTYFP,GEOID,NAME,GTFSFOLDERS
Main,None,Georgia,GA,Chatham County,51,13051,Chatham,Georgia/Chatham-GTFS
Extra,None,Texas,TX,Hardin County,199,48199,Hardin
Main,None,Georgia,GA,Fulton County,121,13121,Fulton,Georgia/atlanta-grta
Main,None,Georgia,GA,Fulton County,121,13121,Fulton,Georgia/atlanta-gtfs_ASC
Main,None,Georgia,GA,Fulton County,121,13121,Fulton,Georgia/atlanta-marta
"""
    return csv


@pytest.fixture
def processed_data():
    return [
        {'COUNTYFP': '051',
         'GEOID': '13051',
         'GTFSFOLDERS': 'Georgia/Chatham-GTFS',
         'MODEL': 'None',
         'NAME': 'Chatham',
         'NAMELSAD': 'Chatham County',
         'STATE': 'Georgia',
         'STATECODE': 'GA',
         'TYPE': 'Main'
         },
        {'COUNTYFP': '199',
         'GEOID': '48199',
         'GTFSFOLDERS': None,
         'MODEL': 'None',
         'NAME': 'Hardin',
         'NAMELSAD': 'Hardin County',
         'STATE': 'Texas',
         'STATECODE': 'TX',
         'TYPE': 'Extra'
         },
        {'COUNTYFP': '121',
         'GEOID': '13121',
         'GTFSFOLDERS': 'Georgia/atlanta-grta',
         'MODEL': 'None',
         'NAME': 'Fulton',
         'NAMELSAD': 'Fulton County',
         'STATE': 'Georgia',
         'STATECODE': 'GA',
         'TYPE': 'Main'
         },
        {'COUNTYFP': '121',
         'GEOID': '13121',
         'GTFSFOLDERS': 'Georgia/atlanta-gtfs_ASC',
         'MODEL': 'None',
         'NAME': 'Fulton',
         'NAMELSAD': 'Fulton County',
         'STATE': 'Georgia',
         'STATECODE': 'GA',
         'TYPE': 'Main'
         },
        {'COUNTYFP': '121',
         'GEOID': '13121',
         'GTFSFOLDERS': 'Georgia/atlanta-marta',
         'MODEL': 'None',
         'NAME': 'Fulton',
         'NAMELSAD': 'Fulton County',
         'STATE': 'Georgia',
         'STATECODE': 'GA',
         'TYPE': 'Main'
         }
    ]


@pytest.fixture
def combined_data():
    return [
        {'NAME': 'Chatham',
         'STATECODE': 'GA',
         'STATE': 'Georgia',
         'COUNTYFP': '051',
         'GEOID': '13051',
         'GTFSFOLDERS': ['Georgia/Chatham-GTFS']},
        {'NAME': 'Fulton',
         'STATECODE': 'GA',
         'STATE': 'Georgia',
         'COUNTYFP': '121',
         'GEOID': '13121',
         'GTFSFOLDERS': ['Georgia/atlanta-grta', 'Georgia/atlanta-gtfs_ASC', 'Georgia/atlanta-marta']},
        {'COUNTYFP': '199',
         'GEOID': '48199',
         'GTFSFOLDERS': [],
         'NAME': 'Hardin',
         'STATE': 'Texas',
         'STATECODE': 'TX'},
    ]


def test_combine(processed_data, combined_data):
    assert combine(processed_data) == combined_data


def test_generate_config_data(csv_file, processed_data):
    with StringIO(csv_file) as f:
        actual = read_csv(f)
        assert actual == processed_data


def test_generate_state_configs(csv_file, tmp_path):
    expected_georgia_config = """\"\"\"
GTFS processing script- GA
\"\"\"

STATE_PREFIX = "GA"
COUNTY_SETS = [

    {
        'name': "Chatham",
        'fipscode': "051",
        'gtfsfolders': [
            'Georgia/Chatham-GTFS',
        ],
    },
    {
        'name': "Fulton",
        'fipscode': "121",
        'gtfsfolders': [
            'Georgia/atlanta-grta',
            'Georgia/atlanta-gtfs_ASC',
            'Georgia/atlanta-marta',
        ],
    },
]
"""
    with io.StringIO(csv_file) as f:
        configs = generate_state_configs(f)

    # expect TX and GA
    assert len(configs) == 2
    assert configs['georgia-gfts-conf.py'] == expected_georgia_config
