import unittest
from digger import Digger


class TestDigger(unittest.TestCase):

    def test_is_matched(self):

        testcases = [
            {
                'name': 'matched',
                'init_args': type('', (object,), {'query': 'abc'})(),
                'args': 'abc',
                'want': True,
            },
            {
                'name': 'not_matched',
                'init_args': type('', (object,), {'query': 'abc'})(),
                'args': 'def',
                'want': False,
            },
            {
                'name': 'regex_matched',
                'init_args': type('', (object,), {'query': 'zz|ab.'})(),
                'args': 'abc',
                'want': True,
            },
            {
                'name': 'regex_not_matched',
                'init_args': type('', (object,), {'query': '.+ab'})(),
                'args': 'abc',
                'want': False,
            },
        ]

        for case in testcases:
            digger = Digger(case['init_args'])
            actual = digger.is_matched(case['args'])
            self.assertEqual(
                case['want'],
                actual,
                'failed test {}: expected {}, actual {}'.format(
                    case['name'],
                    case['want'],
                    actual,
                ))

    def test_dig_model(self):

        testcases = [
            {
                'name': 'matched',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'foo_id': {
                            'type': 'string',
                        }
                    }
                }, {}),
                'want': True,
            },
            {
                'name': 'not_matched',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'bar_id': {
                            'type': 'string',
                        }
                    }
                }, {}),
                'want': False,
            },
            {
                'name': 'matched_with_allOf',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'allOf': [
                        {'$ref': '#/definitions/baz_model'},
                        {'properties': {
                            'foo_id': {
                                'type': 'string',
                            },
                        }},
                    ],
                }, {}),
                'want': True,
            },
            {
                'name': 'not_matched_with_allOf',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'allOf': [
                        {'$ref': '#/definitions/baz_model'},
                        {'properties': {
                            'baz_id': {
                                'type': 'string',
                            },
                        }},
                    ],
                }, {}),
                'want': False,
            },
            {
                'name': 'matched_with_refs',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'baz': {
                            '$ref': '#/definitions/baz_model',
                        }
                    }
                }, {
                    'baz_model': {
                        'type': 'object',
                        'properties': {
                            'foo_id': {
                                'type': 'string',
                            }
                        }
                    },
                }),
                'want': True,
            },
            {
                'name': 'not_matched_with_refs',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'baz': {
                            '$ref': '#/definitions/baz_model',
                        }
                    }
                }, {
                    'baz_model': {
                        'type': 'object',
                        'properties': {
                            'bar_id': {
                                'type': 'string',
                            }
                        }
                    },
                }),
                'want': False,
            },
            {
                'name': 'matched_with_items',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'foo_id': {
                            'type': 'array',
                            'items': {'type': 'string'},
                        }
                    }
                }, {}),
                'want': True,
            },
            {
                'name': 'not_matched_with_items',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'baz_id': {
                            'type': 'array',
                            'items': {'type': 'string'},
                        }
                    }
                }, {}),
                'want': False,
            },
            {
                'name': 'matched_with_items_ref',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'bazs': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/baz_model'},
                        }
                    }
                }, {
                    'baz_model': {
                        'type': 'object',
                        'properties': {
                            'foo_id': {
                                'type': 'string',
                            }
                        }
                    },
                }),
                'want': True,
            },
            {
                'name': 'not_matched_with_items_ref',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'type': 'object',
                    'properties': {
                        'bazs': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/baz_model'},
                        }
                    }
                }, {
                    'baz_model': {
                        'type': 'object',
                        'properties': {
                            'bar_id': {
                                'type': 'string',
                            }
                        }
                    },
                }),
                'want': False,
            },
            {
                'name': 'matched_with_allOf_refs',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'allOf': [
                        {'$ref': '#/definitions/baz_model'},
                        {'properties': {
                            'bar_id': {
                                'type': 'string',
                            },
                        }},
                    ],
                }, {
                    'baz_model': {
                        'type': 'object',
                        'properties': {
                            'foo_id': {
                                'type': 'string',
                            }
                        }
                    },
                }),
                'want': True,
            },
            {
                'name': 'not_matched_with_allOf_refs',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'allOf': [
                        {'$ref': '#/definitions/baz_model'},
                        {'properties': {
                            'bar_id': {
                                'type': 'string',
                            },
                        }},
                    ],
                }, {
                    'baz_model': {
                        'type': 'object',
                        'properties': {
                            'bar_id': {
                                'type': 'string',
                            }
                        }
                    },
                }),
                'want': False,
            },
        ]

        for case in testcases:
            digger = Digger(case['init_args'])
            actual = digger.dig_model(*case['args'])
            self.assertEqual(
                case['want'],
                actual,
                'failed test {}: expected {}, actual {}'.format(
                    case['name'],
                    case['want'],
                    actual,
                ))

    def test_dig_param(self):

        testcases = [
            {
                'name': 'matched',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    '$ref': '#/parameters/foo_id'
                }, []),
                'want': True,
            },
            {
                'name': 'not_matched',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    '$ref': '#/parameters/bar_id'
                }, []),
                'want': False,
            },
            {
                'name': 'matched_by_model',
                'init_args': type('', (object,), {'query': 'baz'})(),
                'args': ({
                    '$ref': '#/definitions/foo'
                }, ['foo']),
                'want': True,
            },
            {
                'name': 'not_matched_by_model',
                'init_args': type('', (object,), {'query': 'baz'})(),
                'args': ({
                    '$ref': '#/definitions/foo'
                }, ['bar']),
                'want': False,
            },
            {
                'name': 'matched_by_param_name',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'name': 'foo_id'
                }, []),
                'want': True,
            },
            {
                'name': 'not_matched_by_param_name',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'name': 'bar_id'
                }, []),
                'want': False,
            },
            {
                'name': 'matched_by_schema_props',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'schema': {'properties': {'foo_id': {'type': 'string'}}},
                }, []),
                'want': True,
            },
            {
                'name': 'not_matched_by_schema_props',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'schema': {'properties': {'bar_id': {'type': 'string'}}},
                }, []),
                'want': False,
            },
            {
                'name': 'matched_by_schema_ref_model',
                'init_args': type('', (object,), {'query': 'baz_id'})(),
                'args': ({
                    'schema': {'$ref': '#/definitions/foo'},
                }, ['foo']),
                'want': True,
            },
            {
                'name': 'not_matched_by_schema_ref_model',
                'init_args': type('', (object,), {'query': 'baz_id'})(),
                'args': ({
                    'schema': {'$ref': '#/definitions/foo'},
                }, ['bar']),
                'want': False,
            },
            {
                'name': 'matched_by_schema_ref_param',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'schema': {'$ref': '#/parameters/foo_id'},
                }, []),
                'want': True,
            },
            {
                'name': 'not_matched_by_schema_ref_param',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'schema': {'$ref': '#/parameters/bar_id'},
                }, []),
                'want': False,
            },
            {
                'name': 'matched_by_schema_allOf_ref',
                'init_args': type('', (object,), {'query': 'baz'})(),
                'args': ({
                    'schema': {'allOf': [
                        {
                            '$ref': '#/definitions/foo',
                        }
                    ]},
                }, ['foo']),
                'want': True,
            },
            {
                'name': 'not_matched_by_schema_allOf_ref',
                'init_args': type('', (object,), {'query': 'baz'})(),
                'args': ({
                    'schema': {'allOf': [
                        {
                            '$ref': '#/definitions/foo',
                        }
                    ]},
                }, ['bar']),
                'want': False,
            },
            {
                'name': 'matched_by_schema_allOf_props',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'schema': {'allOf': [
                        {
                            'properties': {'foo_id': {'type': 'string'}},
                        }
                    ]},
                }, []),
                'want': True,
            },
            {
                'name': 'not_matched_by_schema_allOf_props',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'schema': {'allOf': [
                        {
                            'properties': {'bar_id': {'type': 'string'}},
                        }
                    ]},
                }, []),
                'want': False,
            },
            {
                'name': 'matched_by_schema_props_ref',
                'init_args': type('', (object,), {'query': 'baz'})(),
                'args': ({
                    'schema': {'properties': {'foo': {'$ref': '#/definitions/foo_model'}}, }
                }, ['foo_model']),
                'want': True,
            },
            {
                'name': 'not_matched_by_schema_props_ref',
                'init_args': type('', (object,), {'query': 'baz'})(),
                'args': ({
                    'schema': {'properties': {'foo': {'$ref': '#/definitions/foo_model'}}, }
                }, ['bar_model']),
                'want': False,
            },
        ]

        for case in testcases:
            digger = Digger(case['init_args'])
            actual = digger.dig_param(*case['args'])
            self.assertEqual(
                case['want'],
                actual,
                'failed test {}: expected {}, actual {}'.format(
                    case['name'],
                    case['want'],
                    actual,
                ))


if __name__ == "__main__":
    unittest.main()
