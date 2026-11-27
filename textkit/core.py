import re


def capitalize_words(text: str) -> str:
    return " ".join(word[:1].upper() + word[1:] for word in text.split(" "))


def chunk(text: str, size: int) -> list[str]:
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if isinstance(size, bool) or not isinstance(size, int):
        raise TypeError("size must be an int")
    if size <= 0:
        raise ValueError("size must be greater than 0")
    return [text[start : start + size] for start in range(0, len(text), size)]


def word_count(text: str) -> int:
    return len(text.split())


def slugify(text: str) -> str:
    """Lowercase, replace runs of non-alphanumerics with a single dash, strip dashes."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def truncate(text: str, width: int, suffix: str = "...") -> str:
    """Cut text to at most width characters, ending with suffix when cut.

    If suffix exceeds width, return its first width characters.
    """
    if len(text) <= width:
        return text
    if width < len(suffix):
        return suffix[:width]
    return text[: width - len(suffix)] + suffix


def fixture_fn_16(text: str) -> str:
    """Conflict fixture: lands on main while #16 is in review."""
    return text[::-1]
