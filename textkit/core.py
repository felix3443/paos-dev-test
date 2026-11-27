import re


def slugify(text: str) -> str:
    """Lowercase, replace runs of non-alphanumerics with a single dash, strip dashes."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]", "-", text)
    return text.strip("-")


def truncate(text: str, width: int) -> str:
    """Cut text to at most width characters, ending with '...' when cut."""
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."
