"""
This module is only used during development when css needs to be
compressed when injected into the python code as string.
"""

with open("style.css", "r", encoding="UTF-8") as file:
    """Opens the style.css file which needs to be compressed (where whitespaces will be removed)"""
    text = file.read()
    text = text.replace("  ", "")
    text = text.replace("\n", "")
    with open("comporessed_style.css", "w", encoding="UTF-8") as out_file:
        out_file.write(text)
