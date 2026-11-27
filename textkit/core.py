import re


def word_count(text: str) -> int:
    return len(text.split())


def slugify(text: str) -> str:
    """Lowercase, replace runs of non-alphanumerics with a single dash, strip dashes."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def truncate(text: str, width: int, suffix: str = "...") -> str:
    if len(text) <= width:
        return text
    return text[: width - len(suffix)] + suffix
