import unittest

import textkit
import textkit.core
from textkit import dot_case, snake_case


class DotCaseTest(unittest.TestCase):
    def test_cases(self):
        cases = {
            "HTTPServer error": "http.server.error",
            "hello-World_fooBar baz": "hello.world.foo.bar.baz",
            "http server": "http.server",
            "kebab-case-input": "kebab.case.input",
            "snake_case_input": "snake.case.input",
            "  foo   bar  ": "foo.bar",
            "fooBar": "foo.bar",
            "FooBar": "foo.bar",
            "HTTPServer": "http.server",
            "parseXMLFile": "parse.xml.file",
            "ABC": "abc",
            "version2Update": "version2.update",
            "HTTP2Server": "http2.server",
            "2fast cars": "2fast.cars",
            "a1b2": "a1b2",
            "": "",
            "--__  ": "",
            "  -_ ": "",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(dot_case(text), expected)
                self.assertEqual(dot_case(text), snake_case(text).replace("_", "."))

    def test_importable_from_core(self):
        self.assertIs(textkit.dot_case, textkit.core.dot_case)


if __name__ == "__main__":
    unittest.main()
