import re


class Digger:

    def __init__(self, args):
        self.__query_pat = re.compile(args.query)
        self.__exclude_pat = re.compile(args.exclude) if hasattr(
            args, 'exclude'
        ) and args.exclude != None else None
        self.query = re.compile(args.query)

    def is_matched(self, key):
        if self.__query_pat.search(key) == None:
            return False

        if self.__exclude_pat == None:
            return True

        return self.__exclude_pat.search(key) == None

    def dig_model(self, model, models):
        if 'allOf' in model:
            for item in model['allOf']:
                if self.dig_model(item, models):
                    return True

            return False

        if '$ref' in model:
            ref_name = model['$ref'].replace('#/definitions/', '')
            if ref_name in models:
                return self.dig_model(models[ref_name], models)

            return False

        if 'items' in model:
            return self.dig_model(model['items'], models)

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

    def dig_param(self, param, models):
        if 'name' in param and self.is_matched(param['name']):
            return True

        if 'schema' in param:
            return self.dig_param(param['schema'], models)

        if '$ref' in param:
            ref_name = param['$ref'].replace('#/definitions/', '')
            return ref_name in models or self.is_matched(param['$ref'].replace('#/parameters/', ''))

        if 'allOf' in param:
            for item in param['allOf']:
                if self.dig_param(item, models):
                    return True

            return False

        if 'items' in param:
            if '$ref' in param['items']:
                return self.dig_param(param['items'], models)

            if 'properties' in param['items']:
                return self.dig_param(param['items'], models)

            return False

        if 'properties' in param:
            for key in param['properties']:
                if self.is_matched(key):
                    return True
                if self.dig_param(param['properties'][key], models):
                    return True

            return False

        return False

    METHODS = ['get', 'post', 'put', 'delete']

    def get_apis(self, models, obj):
        apis = []
        for path in obj['paths']:

            hit_common_param = False
            for key in obj['paths'][path]:
                if key == 'parameters':
                    for param in obj['paths'][path][key]:
                        if self.dig_param(param, models):
                            hit_common_param = True
                elif key in self.METHODS:
                    if 'parameters' not in obj['paths'][path][key]:
                        continue

                    hit_param = False
                    for param in obj['paths'][path][key]['parameters']:
                        if self.dig_param(param, models):
                            hit_param = True

                    if hit_common_param or hit_param:
                        apis.append(path + '@' + key)

        return apis
