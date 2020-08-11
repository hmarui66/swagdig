# swagdig

Path extractor of swagger.yml by a key name of paramters or definitions model

## How to use

```bash
cat swagger.yml | pipenv run python swagdig.py -q foo_id
```

## Command options

```
optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filepath FILEPATH
                        yaml file path
  -q QUERY, --query QUERY
                        query string(regex can be used)
  -e EXCLUDE, --exclude EXCLUDE
                        exclude query string(regex can be used)
```