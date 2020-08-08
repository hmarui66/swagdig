import re


class Digger:

    def __init__(self, args):
        self.__query_pat = re.compile(args.query)
        self.__exclude_pat = re.compile(
            args.exclude) if hasattr(args, 'exclude') and args.exclude != None else None
        self.query = re.compile(args.query)

    def is_matched(self, key):
        if self.__query_pat.search(key) == None:
            return False

        if self.__exclude_pat == None:
            return True

        return self.__exclude_pat.search(key) == None

    def dig_model(self, model, models):
        if 'allOf' in model:
            for key in model['allOf']:
                if self.dig_model({key: model['allOf'][key]}, models):
                    return True
            return False

        if '$ref' in model:
            ref_name = model['$ref'].replace('#/definitions/', '')
            if ref_name in models:
                return self.dig_model(models[ref_name], models)

            return False

        if 'properties' not in model:
            return False

        for key in model['properties']:
            if self.is_matched(key):
                return True

            if self.dig_model(model['properties'][key], models):
                return True

        return False

    def get_models(self, obj):
        models = []
        for key in obj['definitions']:
            if self.is_matched(key):
                models.append(key)
                continue

            if self.dig_model(obj['definitions'][key], obj['definitions']):
                models.append(key)
                continue

        return models

    def get_apis(self, models, obj):
        apis = []
        for path in obj['paths']:
            hit_param = False
            for key in obj['paths'][path]:
                if key == 'parameters':
                    for param in obj['paths'][path][key]:
                        print(param)
                        if self.is_matched(param):
                            hit_param = True
                else:
                    print(key, '->', obj['paths'][path],
                          'hit param: ', hit_param)

        return apis