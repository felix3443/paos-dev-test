import unittest

from textkit.core import stub_fn_15


class T(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(stub_fn_15("a b c"), "c b a")


if __name__ == "__main__":
    unittest.main()
