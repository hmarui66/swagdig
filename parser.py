#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import yaml
import sys

args = {}

def load_yaml():
    try:
        with open('/Users/hirotsugumarui/go/src/github.com/bitkey-platform/appgate/swagger/swagger.yml') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print('Exception occurred while loading YAML...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

def is_matched(key):
    return key.find(args.query) >= 0 and (args.exclude == None or key.find(args.exclude) < 0)

def dig_model(model):
    if 'allOf' in model:
        for item in model['allOf']:
            if dig_model(item):
                return True
        return False

    if 'type' not in model or model['type'] != 'object':
        return False

    for key in model['properties']:
        if is_matched(key):
            return True

        if dig_model(model['properties'][key]):
            return True

    return False

def get_models(obj):
    models = []
    for key in obj['definitions']:
        if is_matched(key):
            models.append(key)
            continue

        if dig_model(obj['definitions'][key]):
            models.append(key)
            continue

    return models

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='argparse sample.')
    parser.add_argument('-q','--query', type=str, help='query string')
    parser.add_argument('-e','--exclude', type=str, help='exclude query string')
    args = parser.parse_args()

    if args.query == None:
        print('query argument required', file=sys.stderr)
        exit(1)

    obj = load_yaml()

    models = get_models(obj)

    print(models)
