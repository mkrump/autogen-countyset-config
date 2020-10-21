import argparse
import csv

from jinja2 import Environment, select_autoescape, FileSystemLoader

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
    parser.add_argument('--output-file', dest='output_file', required=True, type=str, help='output file name')

    args = parser.parse_args()
    county_sets = read_csv(args.input_file)

    # TODO would need to add state prefix to spreadsheet
    rendered_template = CONFIG_TEMPLATE.render(county_sets=county_sets, state_prefix='GA')
    with open(args.output_file, "w") as f:
        f.write(rendered_template)
