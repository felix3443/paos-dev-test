import unittest

from textkit import pascal_case
from textkit.core import pascal_case as core_pascal_case


class PascalCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello-World_fooBar baz": "HelloWorldFooBarBaz",
            "HTTPServer": "HttpServer",
            "parseXMLFile": "ParseXmlFile",
            "fooBar": "FooBar",
            "version2Update": "Version2Update",
            "  foo   bar  ": "FooBar",
            "": "",
            "--__  ": "",
            "http server": "HttpServer",
            "ABC": "Abc",
            "HTTP2Server": "Http2Server",
            "2fast cars": "2fastCars",
            "a1b2": "A1b2",
            "FooBar": "FooBar",
            "  -_ ": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(pascal_case(text), expected)

    def test_importable_from_core(self):
        self.assertIs(core_pascal_case, pascal_case)


if __name__ == "__main__":
    unittest.main()
