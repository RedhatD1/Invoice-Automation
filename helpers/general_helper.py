import re
from os import unlink, path
from typing import Union


def remove_space_from_text(text: Union[str, float]):
    # print(text)
    if isinstance(text, str):
        # sanitized_text = text.replace(" ", "")
        sanitized_text = re.sub(r"\s+", "", text)
        # print(sanitized_text)
        return sanitized_text
    else:
        return text


def unlink_file(file_path: str):
    try:
        unlink(file_path)
        return True
    except Exception as e:
        print(e)
        return False


def check_file_existence(file_path: str):
    return path.exists(file_path)
