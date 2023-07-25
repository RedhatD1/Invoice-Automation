from backend.regex_algorithm import extractor
from backend.regex_algorithm_sunjid_bhai import regex2
from backend.other import template


def process_pdf(file_name: str, algorithm: str):
    if algorithm == "regex2":
        response = regex2.extract_information_from_invoice(file_name)
    elif algorithm == "ocr":
        response = template.other(file_name)  # template, does error handling
    elif algorithm == "dl":
        response = template.other(file_name)
    else:
        response = extractor.get_json_formatted(file_name)  # new regex, does error handling
    return response
