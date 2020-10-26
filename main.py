import argparse
import csv
import itertools
import logging
import os

from jinja2 import Environment, select_autoescape, FileSystemLoader

logging.basicConfig(level=logging.INFO)
ENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
CONFIG_TEMPLATE = ENV.get_template('config_template.jinja2')


def read_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        county_sets = []
        for row in reader:
            row["COUNTYFP"] = row['COUNTYFP'].zfill(3)
            county_sets.append(row)
        return county_sets


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Autogenerate config file based on county data')
    parser.add_argument('--input-file', dest='input_file', required=True, type=str,
                        help='csv file with county name and fips data')
    parser.add_argument('--output-dir', dest='output_dir', required=True, type=str, help='output directory location')

    args = parser.parse_args()
    output_dir = args.output_dir
    county_sets = read_csv(args.input_file)
    expected_headers = {'State', 'COUNTYFP', 'StateCode'}
    file_headers = county_sets[0].keys()
    if len(expected_headers.intersection(file_headers)) != 3:
        logging.error(f"input input file headers"
                      f"\n\texpected to contain: {','.join(expected_headers)}"
                      f"\n\tfound: {','.join(file_headers)}"
                      )
        raise ValueError("invalid input file")

    county_sets = sorted(county_sets, key=lambda x: (x['State'], x['COUNTYFP']))
    states = itertools.groupby(county_sets, key=lambda x: x['State'])
    for state_name, state in states:
        rendered_template = CONFIG_TEMPLATE.render(county_sets=list(state))
        filename = f'{output_dir}/{state_name.lower()}-gfts-conf.py'
        with open(filename, "w") as f:
            logging.info(f'generating: {filename}')
            f.write(rendered_template)
