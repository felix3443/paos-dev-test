import unittest

import textkit
import textkit.core


class ReverseWordsTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello world foo": "foo world hello",
            "": "",
            "   \t\n  ": "",
            "hello": "hello",
            "  hello   world  ": "world hello",
            "  a\tb\n c  ": "c b a",
            "one\ttwo\nthree\r\nfour": "four three two one",
            "a　b": "b a",
            "a b c": "c b a",
            "你好 世界 Ünïcödé": "Ünïcödé 世界 你好",
            "Hello, world!": "world! Hello,",
            "foo-bar baz_qux (x)": "(x) baz_qux foo-bar",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(textkit.reverse_words(text), expected)

    def test_package_export(self):
        self.assertIs(textkit.reverse_words, textkit.core.reverse_words)


if __name__ == "__main__":
    unittest.main()
