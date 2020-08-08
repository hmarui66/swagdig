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
                    'allOf': {
                        '$ref': '#/definitions/baz_model',
                        'properties': {
                            'foo_id': {
                                'type': 'string',
                            },
                        },
                    },
                }, {}),
                'want': True,
            },
            {
                'name': 'not_matched_with_allOf',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'allOf': {
                        '$ref': '#/definitions/baz_model',
                        'properties': {
                            'bar_id': {
                                'type': 'string',
                            },
                        },
                    },
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
                'name': 'matched_with_allOf_refs',
                'init_args': type('', (object,), {'query': 'foo_id'})(),
                'args': ({
                    'allOf': {
                        '$ref': '#/definitions/baz_model',
                        'properties': {
                            'bar_id': {
                                'type': 'string',
                            },
                        },
                    },
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
                    'allOf': {
                        '$ref': '#/definitions/baz_model',
                        'properties': {
                            'bar_id': {
                                'type': 'string',
                            },
                        },
                    },
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


if __name__ == "__main__":
    unittest.main()
