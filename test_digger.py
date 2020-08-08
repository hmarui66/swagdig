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


if __name__ == "__main__":
    unittest.main()
