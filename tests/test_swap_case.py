import unittest

import textkit
import textkit.core


class SwapCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello": "HELLO",
            "WORLD": "world",
            "Hello World": "hELLO wORLD",
            "fooBar_BAZ-qux": "FOObAR_baz-QUX",
            "": "",
            "123 !@# _-": "123 !@# _-",
            "中文 123": "中文 123",
            "Ünïcödé": "üNÏCÖDÉ",
            "ß": "SS",
            "Straße": "sTRASSE",
            "ΣΑΣ": "σας",
            "İ": "i̇",
            "ǅ": "ǅ",
            "a\tB\n": "A\tb\n",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(textkit.swap_case(text), expected)

    def test_ascii_round_trip(self):
        for text in ["hello", "Hello World", "fooBar_BAZ-qux", "a\tB\n", ""]:
            with self.subTest(text=text):
                self.assertEqual(textkit.swap_case(textkit.swap_case(text)), text)

    def test_package_export(self):
        self.assertIs(textkit.swap_case, textkit.core.swap_case)


if __name__ == "__main__":
    unittest.main()
