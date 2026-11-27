import re


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
