# autogen-countyset-config
An example module to autogenerate configs from csv files. See example data for the expected input format.

### Requirements
* [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html) (optional)

### Setup 
```
pip install .
```
or 
```
pip install -r requirements.txt
```


### Tests
```
python -m pytest
```
### Usage
```
usage: generate_configs [-h] --input-file INPUT_FILE --output-dir OUTPUT_DIR

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
generate_configs \
    --input-file=./autogen_configs/example_data/multiple-states.csv \
    --output-dir=./autogen_configs/example_data/configs
```
