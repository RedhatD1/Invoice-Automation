from extraction_algorithms.invoice import extract


def process_pdf(file_name: str) -> dict:
    # regardless of algorith, we use the regex method
    return extract.get_json(file_name)  # new regex, does error handling
