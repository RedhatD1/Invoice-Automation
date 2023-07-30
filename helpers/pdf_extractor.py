from extraction_algorithms.regex_algorithm_sunjid_bhai import regex2
from extraction_algorithms.other import template
from extraction_algorithms.invoice import extract

def process_pdf(file_name: str, algorithm: str):
    if algorithm == "regex2":
        response = regex2.extract_information_from_invoice(file_name)
    elif algorithm == "ocr":
        response = template.other(file_name)  # template, does error handling
    elif algorithm == "dl":
        response = template.other(file_name)
    else:
        response = extract.get_json_formatted(file_name)  # new regex, does error handling
    return response
