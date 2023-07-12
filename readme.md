# Invoice Extraction Module
Takes a PDF as an input and returns a form with the extracted data.

### Usage
Put invoices in "/invoices/" directory

### Setup
python3 -m venv env <br>
source venv/bin/activate <br>
pip3 install -r requirements.txt <br>
uvicorn fast_api:app --reload <br>

You need to have java runtime installed

### Parameters
pdfFileName: invoice.pdf
algorithm: "regex", "regex2", "ocr", "dl"

### Installing new libraries
pip3 install <library_name>

### Updating requirements.txt
pip3 freeze > requirements.txt
