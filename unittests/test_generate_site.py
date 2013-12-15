import unittest
import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import generate
from utils import get_random_str


class TestGenerateSite(unittest.TestCase):
    """ Class that tests generate_site() function """

    def setUp(self):
        self.input_path = get_random_str()
        self.output_path = get_random_str()
        os.mkdir(self.input_path)

    def tearDown(self):
        shutil.rmtree(self.input_path)

    def test_generate_site_no_layout_in_metadata(self):
        file_without_layout = get_random_str() + '.rst'
        with open(os.path.join(self.input_path, file_without_layout), 'w') as f:
            f.write("""{"title": "Test"}
                    ---
                    something something""")
        generate.generate_site(self.input_path, self.output_path)
        self.assertFalse(os.path.exists(self.output_path))

    def test_generate_site_wrong_template_name(self):
        file_wrong_template = get_random_str() + '.rst'
        with open(os.path.join(self.input_path, file_wrong_template), 'w') as f:
            f.write("""{"title": "Test", "layout": "wrong.html"}
                    ---
                    something something""")
        generate.generate_site(self.input_path, self.output_path)
        self.assertFalse(os.path.exists(self.output_path))

    def test_generate_site_correct_params(self):
        generate.generate_site('test/source', 'output')
        with open('test/expected_output/contact.html') as ec, \
                open('test/expected_output/index.html') as ei, \
                open('output/contact.html') as c, \
                open('output/index.html') as i:
            self.assertEqual(ec.read() + ei.read(), c.read() + i.read())


if __name__ == '__main__':
    unittest.main(exit=False)
