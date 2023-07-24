# Invoice Extraction Module
Takes a PDF as an input and returns a form with the extracted data.

### Usage
Put invoices in "/invoices/" directory
Put cv in "/cv/" directory

### Setup
python3 -m venv env <br>
source venv/bin/activate <br>
pip3 install -r requirements.txt <br>


uvicorn main:app --reload <br>

You need to have java runtime installed
Run the trainer.py to generate the model
"python -m spacy download en_core_web_sm" to manually download pretrained model
for camelot error, use "pip3 install 'camelot-py[cv]'" with the '' quotation
for ssl error, "pip install certifi" and "pip install --use-pep517 -r requirements.txt" can help

### Parameters
pdfFileName: invoice.pdf
algorithm: "regex", "regex2", "ocr", "dl"

### Installing new libraries
pip3 install <library_name>

### Updating requirements.txt
pip3 freeze > requirements.txt
