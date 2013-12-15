import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import generate


class TestBeautify(unittest.TestCase):
    """ Class that tests beautify() function """

    def test_beautify_empty_string(self):
        input = ''
        actual = generate.beautify(input)
        expected = ''
        self.assertEqual(actual, expected)

    def test_beautify_all_newlines(self):
        input = '\n\n\n\n\n'
        actual = generate.beautify(input)
        expected = '\n'
        self.assertEqual(actual, expected)

    def test_beautify_mixed_input(self):
        input = ('No newlines allowed!\n\n\nNot more than two, anyways.\n'
                 'And the end of the text...\n\n\n\n\nis clean.\n\n\n')
        actual = generate.beautify(input)
        expected = ('No newlines allowed!\n\nNot more than two, anyways.\n'
                    'And the end of the text...\n\nis clean.\n')
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main(exit=False)
