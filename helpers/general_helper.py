import re
from os import unlink


def remove_space_from_text(text: str):
    # print(text)
    if isinstance(text, str):
        # sanitized_text = text.replace(" ", "")
        sanitized_text = re.sub(r"\s+", "", text)
        # print(sanitized_text)
        return sanitized_text
    else:
        return text


def unlink_file(file_name: str):
    try:
        unlink(f"invoices/{file_name}")
        return True
    except Exception as e:
        print(e)
        return False


