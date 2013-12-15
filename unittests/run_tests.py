import unittest
import pkgutil
from os import path


if __name__ == '__main__':
    """ Adds all test modules in unittests directory (except the current one)
    in a test suite and runs them all. """

    module_strings = [m for _, m, _ in pkgutil.iter_modules(['unittests'])
                      if m != path.splitext(path.basename(__file__))[0]]
    suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    text_runner = unittest.TextTestRunner().run(testSuite)
