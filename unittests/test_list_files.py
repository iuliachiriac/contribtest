import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import generate
from utils import get_random_str


class TestListFiles(unittest.TestCase):
    """ Class that tests list_files() function """

    def setUp(self):
        while True:
            self.inexistent_path = get_random_str()
            if not os.path.exists(self.inexistent_path):
                break
        self.path_with_no_rst = get_random_str()
        if not os.path.exists(self.path_with_no_rst):
            os.mkdir(self.path_with_no_rst)

    def tearDown(self):
        os.rmdir(self.path_with_no_rst)

    def test_list_files_inexistent_path(self):
        actual = list(generate.list_files(self.inexistent_path))
        expected = []
        self.assertEqual(actual, expected)

    def test_list_files_no_rst_files(self):
        actual = list(generate.list_files(self.path_with_no_rst))
        expected = []
        self.assertEqual(actual, expected)

    def test_list_files_correct_source_dir(self):
        input = 'test/source'
        actual = list(generate.list_files(input))
        expected = ['test/source/contact.rst', 'test/source/index.rst']
        self.assertItemsEqual(actual, expected)


if __name__ == '__main__':
    unittest.main(exit=False)
