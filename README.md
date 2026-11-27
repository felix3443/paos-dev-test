# paos-dev-test

Toy Python package used to test an automated development loop. Run tests with `python -m unittest discover -s tests -v`.

## Naming-style conversion

`textkit` provides `snake_case`, `kebab_case` and `camel_case`. Input is split into words on spaces, `-`, `_`, camelCase boundaries and acronym boundaries; digits stay attached to the preceding word. Empty or separator-only input returns `""`.

```python
from textkit import camel_case, kebab_case, snake_case

snake_case("hello-World_fooBar baz")  # -> "hello_world_foo_bar_baz"
snake_case("HTTPServer")              # -> "http_server"
snake_case("version2Update")          # -> "version2_update"
kebab_case("parseXMLFile")            # -> "parse-xml-file"
kebab_case("  foo   bar  ")           # -> "foo-bar"
camel_case("hello-World_fooBar baz")  # -> "helloWorldFooBarBaz"
camel_case("parseXMLFile")            # -> "parseXmlFile"
camel_case("FooBar")                  # -> "fooBar"
```
