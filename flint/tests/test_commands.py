import unittest

from flint.tests import execute


class TestCommands(unittest.TestCase):
    def test_register(self):
        execute(["flint", "--help"])


if __name__ == "__main__":
    unittest.main()
