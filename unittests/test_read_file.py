import unittest
import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import generate
from utils import get_random_str


class TestReadFile(unittest.TestCase):
    """ Class that tests read_file() function """

    def setUp(self):
        while True:
            self.inexistent_path = get_random_str()
            if not os.path.exists(self.inexistent_path):
                break
        self.path_to_file = get_random_str()
        os.mkdir(self.path_to_file)
        self.filename = get_random_str()
        with open(os.path.join(self.path_to_file, self.filename), 'w') as f:
            f.write("Something that doesn't have the expected format")

    def tearDown(self):
        shutil.rmtree(self.path_to_file)

    def test_read_file_inexistent_path(self):
        actual = generate.read_file(self.inexistent_path)
        expected = {}, ''
        self.assertEqual(actual, expected)

    def test_read_file_incorrect_file_format(self):
        actual = generate.read_file(os.path.join(self.path_to_file,
                                                 self.filename))
        expected = {}, ''
        self.assertEqual(actual, expected)

    def test_read_file_correct_input(self):
        input = 'test/source/contact.rst'
        actual = generate.read_file(input)
        expected = {u"title": u"Contact us!", u"layout": u"base.html"}, \
            "\nWrite an email to contact@example.com.\n"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main(exit=False)
