import argparse
import csv
import itertools
import logging
from typing import TypedDict, List, io, Dict

from jinja2 import Environment, select_autoescape, PackageLoader

logging.basicConfig(level=logging.INFO)
ENV = Environment(
    loader=PackageLoader('autogen_configs', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
CONFIG_TEMPLATE = ENV.get_template('config_template.jinja2')


class CountySet(TypedDict):
    NAME: str
    STATECODE: str
    STATE: str
    COUNTYFP: str
    GEOID: str
    GTFSFOLDERS: List[str]


Config = Dict[str, str]


def generate_state_configs(csvfile: io.TextIO) -> Config:
    county_sets = read_csv(csvfile)
    expected_headers = {'NAME', 'STATECODE', 'STATE', 'COUNTYFP', 'GEOID', 'GTFSFOLDERS'}
    file_headers = county_sets[0].keys()
    if len(expected_headers.intersection(file_headers)) != len(expected_headers):
        logging.error(f"input input file headers"
                      f"\n\texpected to contain: {','.join(expected_headers)}"
                      f"\n\tfound: {','.join(file_headers)}"
                      )
        raise ValueError("invalid input file")

    county_sets = combine(county_sets)
    county_sets = sorted(county_sets, key=lambda x: x['STATE'])
    states = itertools.groupby(county_sets, key=lambda x: x['STATE'])
    configs = {}
    for state_name, state in states:
        filename = f"{state_name.lower()}-gfts-conf.py"
        configs[filename] = CONFIG_TEMPLATE.render(county_sets=list(state))
    return configs


def read_csv(csvfile: io.TextIO) -> List[CountySet]:
    reader = csv.DictReader(csvfile)
    county_sets = []
    for row in reader:
        row["COUNTYFP"] = row['COUNTYFP'].zfill(3)
        county_sets.append(row)
    return county_sets


def combine(county_sets: List[CountySet]) -> List[CountySet]:
    def sort_key(x):
        return x['STATE'], x['COUNTYFP'], x['GEOID']

    county_sets = sorted(county_sets, key=sort_key)
    grouped_data = itertools.groupby(county_sets, key=sort_key)
    template_data = []
    for key, group in grouped_data:
        group = list(group)
        first_record = group[0]
        row = {
            'NAME': first_record['NAME'],
            'STATECODE': first_record['STATECODE'],
            'STATE': first_record['STATE'],
            'COUNTYFP': first_record['COUNTYFP'],
            'GEOID': first_record['GEOID'],
            'GTFSFOLDERS': [i['GTFSFOLDERS'] for i in group] if first_record['GTFSFOLDERS'] else []
        }
        template_data.append(row)
    return template_data


def read_write(input_file: str, output_dir: str) -> None:
    with open(input_file) as f:
        configs = generate_state_configs(f)
    for filename, content in configs.items():
        with open(f'{output_dir}/{filename}', 'w+') as outfile:
            logging.info(f'generating: {outfile.name}')
            outfile.write(content)


def main():
    parser = argparse.ArgumentParser(description='Autogenerate config file based on county data')
    parser.add_argument('--input-file', dest='input_file', required=True, type=str,
                        help='csv file with county name and fips data')
    parser.add_argument('--output-dir', dest='output_dir', required=True, type=str, help='output directory location')

    args = parser.parse_args()
    output_dir = args.output_dir
    input_file = args.input_file

    read_write(input_file, output_dir)


if __name__ == '__main__':
    main()
