import unittest

import textkit
import textkit.core
from textkit import constant_case, snake_case


class ConstantCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "http server": "HTTP_SERVER",
            "hello-World_fooBar baz": "HELLO_WORLD_FOO_BAR_BAZ",
            "kebab-case-input": "KEBAB_CASE_INPUT",
            "snake_case_input": "SNAKE_CASE_INPUT",
            "  foo   bar  ": "FOO_BAR",
            "fooBar": "FOO_BAR",
            "FooBar": "FOO_BAR",
            "HTTPServer": "HTTP_SERVER",
            "parseXMLFile": "PARSE_XML_FILE",
            "ABC": "ABC",
            "version2Update": "VERSION2_UPDATE",
            "HTTP2Server": "HTTP2_SERVER",
            "2fast cars": "2FAST_CARS",
            "a1b2": "A1B2",
            "": "",
            "--__  ": "",
            "  -_ ": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(constant_case(text), expected)
                self.assertEqual(constant_case(text), snake_case(text).upper())

    def test_importable_from_core(self):
        self.assertIs(textkit.constant_case, textkit.core.constant_case)


if __name__ == "__main__":
    unittest.main()
