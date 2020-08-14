# swagdig

Path extractor of swagger.yml by a key name of paramters or definitions model

## How to use

```bash
$ curl -s https://petstore.swagger.io/v2/swagger.json | pipenv run python swagdig.py -q "category|quantity" -i json
# => models:  ['Pet', 'Order']
# => post	/pet
# => put	/pet
# => post	/store/order
```

## Command options

```
usage: swagdig.py [-h] [-i INPUT] [-f FILEPATH] [-q QUERY] [-e EXCLUDE]

swagdig.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file type.(yaml|json). default yaml.
  -f FILEPATH, --filepath FILEPATH
                        yaml file path
  -q QUERY, --query QUERY
                        query string(regex can be used)
  -e EXCLUDE, --exclude EXCLUDE
                        exclude query string(regex can be used)
```