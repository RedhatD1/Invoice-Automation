import sys
sys.path.append('backend/script')
from fastapi import FastAPI
from extraction_regex import *

app = FastAPI()

@app.get("/")
def read_root():
    json_data = execute_script('invoices/2.pdf')
    return {
    "invoice_number": "INV-001",
    "invoice_amount": "1000",
    "invoice_address": "New York, United States",
    "invoice_table": {
        "column1": [1, 2, 3],
        "column2": ["A", "B", "C"],
        "column3": [10.5, 20.3, 15.2]
    }
}


