# autogen-countyset-config
### Requirements
* [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html)

### Setup 
```
pipenv install
```

### Usage
```
usage: main.py [-h] --input-file INPUT_FILE --output-file OUTPUT_FILE

Autogenerate config file based on county data

optional arguments:
  -h, --help            show this help message and exit
  --input-file INPUT_FILE
                        csv file with county name and fips data
  --output-file OUTPUT_FILE
                        output file name
```

### Example 
```
python main.py --input-file=./example_data/georgia-counties.csv --output-file=example_data/georgia-gtfs-config-auto.py
```