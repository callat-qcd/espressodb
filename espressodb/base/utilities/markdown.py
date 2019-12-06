"""Markdown to html converter
"""
from espressodb.base.utilities import blackmagicsorcery as re

#: Patterns for markdown to html conversion
PATTERNS = {r"`([^`]+)`": r"<code>\g<1></code>"}


def convert_string(string: str, wrap_blocks: bool = False) -> str:
    """Converts Markdown like expression to html.

    See :data:`PATTERNS` for available substitutions.

    Arguments:
        string: The string to convert to html.
        wrap_blocks: If True wrap string in `<p>` blocks. Delimi

    """
    out = string or ""  # make sure that None does not cause issues

    for pattern, replacement in PATTERNS.items():
        out = re.sub(pattern, replacement, out)

    if wrap_blocks:
        out = "<p>" + "</p><p>".join(out.split("\n\n")) + "</p>"

    return out
