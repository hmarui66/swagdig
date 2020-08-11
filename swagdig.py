import os
import sys
import argparse
import yaml
from digger import Digger


def load_yaml(filepath):
    if filepath == None or filepath == '':
        return yaml.load(sys.stdin, Loader=yaml.SafeLoader)

    try:
        with open(filepath) as file:
            return yaml.safe_load(file)

    except Exception as e:
        print('Exception occurred while loading YAML...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='argparse sample.')
    parser.add_argument('-f', '--filepath', type=str, help='yaml file path')
    parser.add_argument('-q', '--query', type=str,
                        help='query string(regex can be used)')
    parser.add_argument('-e', '--exclude', type=str,
                        help='exclude query string(regex can be used)')
    args = parser.parse_args()

    if args.query == None:
        print('query argument required', file=sys.stderr)
        exit(1)

    obj = load_yaml(args.filepath)

    digger = Digger(args)

    models = digger.get_models(obj)
    print('models: ', models)

    apis = digger.get_apis(models, obj)
    for api in apis:
        path, method = api.split('@')
        print('{}\t{}'.format(method, path))
