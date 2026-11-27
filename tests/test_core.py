import unittest

from textkit import camel_case, capitalize_words, chunk, kebab_case, snake_case, truncate
from textkit.core import _split_words, slugify, word_count
from textkit.core import camel_case as core_camel_case
from textkit.core import kebab_case as core_kebab_case
from textkit.core import snake_case as core_snake_case


class CapitalizeWordsTest(unittest.TestCase):
    def test_capitalizes_first_character_and_preserves_rest(self):
        self.assertEqual(capitalize_words("hello wORLD"), "Hello WORLD")

    def test_preserves_spaces(self):
        self.assertEqual(capitalize_words("  hello   world  "), "  Hello   World  ")

    def test_empty_and_spaces_only(self):
        for text in ("", " ", "   "):
            with self.subTest(text=text):
                self.assertEqual(capitalize_words(text), text)

    def test_single_character_words(self):
        self.assertEqual(capitalize_words("a b C"), "A B C")

    def test_only_spaces_separate_words(self):
        self.assertEqual(capitalize_words("hello\tworld foo\nbar"), "Hello\tworld Foo\nbar")

    def test_unicode_letters(self):
        self.assertEqual(capitalize_words("école über"), "École Über")


class ChunkTest(unittest.TestCase):
    def test_equal_sized_pieces(self):
        self.assertEqual(chunk("abcdef", 2), ["ab", "cd", "ef"])

    def test_shorter_last_piece(self):
        self.assertEqual(chunk("abcde", 2), ["ab", "cd", "e"])

    def test_empty_text(self):
        self.assertEqual(chunk("", 2), [])

    def test_size_one(self):
        self.assertEqual(chunk("abc", 1), ["a", "b", "c"])

    def test_size_larger_than_text(self):
        self.assertEqual(chunk("abc", 5), ["abc"])

    def test_unicode_characters(self):
        self.assertEqual(chunk("你好吗🌍!", 2), ["你好", "吗🌍", "!"])

    def test_non_positive_size(self):
        for text in ("ab", ""):
            for size in (0, -1, -10):
                with self.subTest(text=text, size=size):
                    with self.assertRaises(ValueError):
                        chunk(text, size)

    def test_non_integer_size(self):
        for text in ("ab", ""):
            for size in (1.5, 2.0, "2", None, [], {}):
                with self.subTest(text=text, size=size):
                    with self.assertRaises(TypeError):
                        chunk(text, size)

    def test_boolean_size(self):
        for text in ("ab", ""):
            for size in (True, False):
                with self.subTest(text=text, size=size):
                    with self.assertRaises(TypeError):
                        chunk(text, size)

    def test_non_string_text(self):
        for text in (None, 123, True, b"ab", ["a", "b"], {}):
            with self.subTest(text=text):
                with self.assertRaises(TypeError):
                    chunk(text, 2)


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

    def test_exact_width_unchanged(self):
        self.assertEqual(truncate("abc", 3), "abc")

    def test_custom_suffix(self):
        self.assertEqual(truncate("abcdefghij", 8, "!"), "abcdefg!")

    def test_empty_suffix(self):
        self.assertEqual(truncate("abcdefghij", 8, ""), "abcdefgh")

    def test_suffix_fills_width(self):
        self.assertEqual(truncate("abcdefghij", 3), "...")

    def test_default_suffix_exceeds_width(self):
        self.assertEqual(truncate("abcdefghij", 2), "..")

    def test_custom_suffix_exceeds_width(self):
        self.assertEqual(truncate("abcdefghij", 5, "abcdef"), "abcde")

    def test_zero_width(self):
        self.assertEqual(truncate("abcdefghij", 0), "")


class SplitWordsTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "foo bar": ["foo", "bar"],
            "foo-bar": ["foo", "bar"],
            "foo_bar": ["foo", "bar"],
            "fooBar": ["foo", "bar"],
            "FooBar": ["foo", "bar"],
            "HTTPServer": ["http", "server"],
            "parseXMLFile": ["parse", "xml", "file"],
            "hello-World_fooBar baz": ["hello", "world", "foo", "bar", "baz"],
            "__Hello--World__": ["hello", "world"],
            "  foo   bar  ": ["foo", "bar"],
            "": [],
            "--__  ": [],
            "version2Update": ["version2", "update"],
            "version2beta": ["version2beta"],
            "HTTP2Server": ["http2", "server"],
            "HTTP2server": ["http2server"],
            "AB12cd34": ["ab12cd34"],
            "XML2": ["xml2"],
            "42abc": ["42abc"],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(_split_words(text), expected)


class SnakeCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello-World_fooBar baz": "hello_world_foo_bar_baz",
            "HTTPServer": "http_server",
            "version2Update": "version2_update",
            "version2beta": "version2beta",
            "HTTP2Server": "http2_server",
            "HTTP2server": "http2server",
            "AB12cd34": "ab12cd34",
            "XML2": "xml2",
            "__Hello--World__": "hello_world",
            "-_ -_": "",
            "": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(snake_case(text), expected)


class KebabCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello-World_fooBar baz": "hello-world-foo-bar-baz",
            "parseXMLFile": "parse-xml-file",
            "  foo   bar  ": "foo-bar",
            "--__  ": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(kebab_case(text), expected)


class CamelCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello-World_fooBar baz": "helloWorldFooBarBaz",
            "HTTPServer": "httpServer",
            "parseXMLFile": "parseXmlFile",
            "FooBar": "fooBar",
            "version2Update": "version2Update",
            "": "",
            "--__  ": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(camel_case(text), expected)

    def test_importable_from_core(self):
        self.assertIs(core_camel_case, camel_case)
        self.assertIs(core_snake_case, snake_case)
        self.assertIs(core_kebab_case, kebab_case)


if __name__ == "__main__":
    unittest.main()
