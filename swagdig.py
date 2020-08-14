import os
import sys
import argparse
import yaml
import json
from digger import Digger


def is_specified(path):
    return path != None and path != ''


def load_yaml(file_type, filepath):
    file = sys.stdin
    if is_specified(filepath):
        file = open(filepath)

    try:
        res = None
        if input == 'json':
            res = json.load(file)
        else:
            res = yaml.safe_load(file)

        if is_specified(filepath):
            file.close()

        return res
    except Exception as e:
        print('Exception occurred while loading YAML...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='swagdig.')
    parser.add_argument('-i', '--input', type=str,
                        help='input file type.(yaml|json). default yaml.')
    parser.add_argument('-f', '--filepath', type=str, help='yaml file path')
    parser.add_argument('-q', '--query', type=str,
                        help='query string(regex can be used)')
    parser.add_argument('-e', '--exclude', type=str,
                        help='exclude query string(regex can be used)')
    args = parser.parse_args()

    if args.query == None:
        print('query argument required', file=sys.stderr)
        exit(1)

    obj = load_yaml(args.input, args.filepath)

    digger = Digger(args)

    models = digger.get_models(obj)
    print('models: ', models)

    apis = digger.get_apis(models, obj)
    for api in apis:
        path, method = api.split('@')
        print('{}\t{}'.format(method, path))
