import unittest

from textkit.core import stub_fn_16


class T(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(stub_fn_16("a b c"), "C B A")


if __name__ == "__main__":
    unittest.main()
