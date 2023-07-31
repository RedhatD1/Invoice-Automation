from typing import Dict

from extraction_algorithms.cv.helpers import pdfToInfo


def get_json(pdf_file_name: str, job_description: str, algorithm='default') -> Dict:
    pdf_file_path = f"documents/cv/{pdf_file_name}"
    return pdfToInfo.extract_info(pdf_file_path, job_description)