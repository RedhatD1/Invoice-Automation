from extraction_algorithms.invoice import extract


def process_pdf(file_name: str, algorithm: str):
    # regardless of algorith, we use the regex method
    response = extract.get_json(file_name)  # new regex, does error handling
    return response
