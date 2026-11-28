import unittest

import textkit
import textkit.core
from textkit import kebab_case, train_case


class TrainCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "hello world": "Hello-World",
            "hello-World_fooBar baz": "Hello-World-Foo-Bar-Baz",
            "kebab-case-input": "Kebab-Case-Input",
            "snake_case_input": "Snake-Case-Input",
            "  foo   bar  ": "Foo-Bar",
            "fooBar": "Foo-Bar",
            "FooBar": "Foo-Bar",
            "HTTPServer": "Http-Server",
            "HTTPServer error": "Http-Server-Error",
            "parseXMLFile": "Parse-Xml-File",
            "http server": "Http-Server",
            "ABC": "Abc",
            "hello": "Hello",
            "version2Update": "Version2-Update",
            "HTTP2Server": "Http2-Server",
            "2fast cars": "2fast-Cars",
            "a1b2": "A1b2",
            "": "",
            "--__  ": "",
            "  -_ ": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(train_case(text), expected)
                self.assertEqual(train_case(text).lower(), kebab_case(text))

    def test_importable_from_core(self):
        self.assertIs(textkit.train_case, textkit.core.train_case)


if __name__ == "__main__":
    unittest.main()
