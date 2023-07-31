# only for reading the pdf file
import pdfplumber
from camelot import read_pdf
from camelot.core import TableList


def read_invoice(file_path: str) -> str:
    # Open the PDF file in binary mode
    with pdfplumber.open(file_path) as pdf:
        text_content = ""

        # Iterate over each page and extract the text
        for page in pdf.pages:
            text = page.extract_text()
            text_content += text
    return text_content


def read_tables(file_path: str) -> TableList:
    tables = read_pdf(filepath=file_path, pages="all", flavor='stream')
    return tables
