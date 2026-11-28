# superagent-dev-test

Toy Python package used to test an automated development loop. Run tests with `python -m unittest discover -s tests -v`.

## Naming-style conversion

`textkit` provides `snake_case`, `kebab_case`, `camel_case`, `pascal_case`, `constant_case`, `dot_case` and `train_case`. Input is split into words on spaces, `-`, `_`, camelCase boundaries and acronym boundaries; digits stay attached to the preceding word. Empty or separator-only input returns `""`.

```python
from textkit import camel_case, constant_case, dot_case, kebab_case, pascal_case, snake_case, train_case

snake_case("hello-World_fooBar baz")  # -> "hello_world_foo_bar_baz"
snake_case("HTTPServer")              # -> "http_server"
snake_case("version2Update")          # -> "version2_update"
kebab_case("parseXMLFile")            # -> "parse-xml-file"
kebab_case("  foo   bar  ")           # -> "foo-bar"
camel_case("hello-World_fooBar baz")  # -> "helloWorldFooBarBaz"
camel_case("parseXMLFile")            # -> "parseXmlFile"
camel_case("FooBar")                  # -> "fooBar"
pascal_case("hello-World_fooBar baz") # -> "HelloWorldFooBarBaz"
pascal_case("parseXMLFile")           # -> "ParseXmlFile"
pascal_case("http server")            # -> "HttpServer"
constant_case("http server")          # -> "HTTP_SERVER"
dot_case("HTTPServer error")          # -> "http.server.error"
dot_case("hello-World_fooBar baz")    # -> "hello.world.foo.bar.baz"
train_case("hello world")            # -> "Hello-World"
train_case("hello-World_fooBar baz") # -> "Hello-World-Foo-Bar-Baz"
train_case("parseXMLFile")           # -> "Parse-Xml-File"
train_case("version2Update")         # -> "Version2-Update"
```

## Word order

`reverse_words` splits input on any whitespace, reverses the order of the resulting tokens and joins them with single ASCII spaces. Punctuation stays attached to its token. Empty or whitespace-only input returns `""`.

```python
from textkit import reverse_words

reverse_words("hello world foo") # -> "foo world hello"
reverse_words("  a\tb\n c  ")    # -> "c b a"
reverse_words("Hello, world!")   # -> "world! Hello,"
```
