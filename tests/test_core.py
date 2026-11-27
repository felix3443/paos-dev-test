import unittest

from textkit.core import slugify, truncate


class SlugifyTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_strips_edges(self):
        self.assertEqual(slugify("  Hi! "), "hi")

    def test_collapses_separator_runs(self):
        for text in ("Hello,  World", "Hello   World", "Hello---World", "Hello,_! World"):
            with self.subTest(text=text):
                self.assertEqual(slugify(text), "hello-world")


class TruncateTest(unittest.TestCase):
    def test_short_text_unchanged(self):
        self.assertEqual(truncate("abc", 10), "abc")

    def test_long_text_cut(self):
        self.assertEqual(truncate("abcdefghij", 8), "abcde...")


if __name__ == "__main__":
    unittest.main()
