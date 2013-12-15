import unittest
import sys
import os
import shutil
from os import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import generate
from utils import get_random_str


class TestWriteOutput(unittest.TestCase):
    """ Class that tests write_output() function """

    def setUp(self):
        while True:
            self.inexistent_path = get_random_str()
            if not os.path.exists(self.inexistent_path):
                break
        self.existing_path = get_random_str()
        os.mkdir(self.existing_path)

    def tearDown(self):
        if os.path.exists(self.inexistent_path):
            shutil.rmtree(self.inexistent_path)
        shutil.rmtree(self.existing_path)

    def test_write_output_inexistent_dir(self):
        generate.write_output(self.inexistent_path, get_random_str(),
                              get_random_str())
        self.assertTrue(path.isdir(self.inexistent_path))

    def test_write_output_creates_file(self):
        filename = get_random_str()
        content = get_random_str()
        generate.write_output(self.existing_path, filename, content)
        self.assertTrue(path.isfile(os.path.join(
            self.existing_path, filename + '.html')))

    def test_write_output_correct_output(self):
        filename = get_random_str()
        content = get_random_str()
        generate.write_output(self.existing_path, filename, content)
        with open(os.path.join(self.existing_path, filename + '.html')) as f:
            self.assertEqual(f.read(), content)


if __name__ == '__main__':
    unittest.main(exit=False)
