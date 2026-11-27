import unittest

from textkit.core import slugify, truncate, word_count


class WordCountTest(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(word_count(""), 0)

    def test_whitespace_only(self):
        self.assertEqual(word_count(" \t\n\r\v\f"), 0)

    def test_single_word(self):
        self.assertEqual(word_count("hello"), 1)

    def test_mixed_whitespace(self):
        self.assertEqual(word_count("  a b\tc\n"), 3)

    def test_punctuation_does_not_separate_words(self):
        self.assertEqual(word_count("hello,world foo-bar"), 2)

    def test_unicode_whitespace(self):
        self.assertEqual(word_count("a\u00a0b\u2003c"), 3)


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
