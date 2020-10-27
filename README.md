# autogen-countyset-config
An example module to autogenerate configs from csv files. See example data for the expected input format.

### Requirements
* [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html)

### Setup 
```
pipenv install
```

### Usage
```
usage: main.py [-h] --input-file INPUT_FILE --output-dir OUTPUT_DIR

Autogenerate config file based on county data

optional arguments:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        csv file with county name and fips data
  --output-dir OUTPUT_DIR
                        output directory location
```

### Example 
```
python main.py --input-file=./example_data/multiple-states.csv --output-dir=./example_data/configs
```
