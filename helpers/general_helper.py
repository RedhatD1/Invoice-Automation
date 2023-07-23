import re


def remove_space_from_text(text: str):
    print(text)
    if isinstance(text, str):
        # sanitized_text = text.replace(" ", "")
        sanitized_text = re.sub(r"\s+", "", text)
        print(sanitized_text)
        return sanitized_text
    else:
        return text

