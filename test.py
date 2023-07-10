from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
import json
from datetime import datetime


def extract_invoice_details(extracted_data):
    invoice_json = {
        "customer_info": {
            "name": extracted_data.get("issuer", ""),
            "phone": extracted_data.get("phone", ""),
            "email": extracted_data.get("email", ""),
            # "billing_address": extracted_data.get("billing_address", ""),
            # "shipping_address": extracted_data.get("shipping_address", "")
        },
        "item_details": [],
        "total_amount": extracted_data.get("amount", ""),
        "note": extracted_data.get("note", ""),
        "invoice_info": {
            "date": extracted_data.get("date", ""),
            "number": extracted_data.get("invoice_number", "")
        }
    }

    items = extracted_data.get("lines", [])
    for item in items:
        item_detail = {
            "name": item.get("description", ""),
            "unit_price": item.get("unit_price", ""),
            "quantity": item.get("qty", "1"),
            "amount": item.get("price", ""),
            "currency": item.get("currency", "USD")
        }
        invoice_json["item_details"].append(item_detail)

    invoice_json = json.dumps(invoice_json, indent=4, default=str)

    return invoice_json

templates = read_templates('templates/')
#print(templates)
result = extract_data('invoices\p2.pdf', templates=templates)
result = extract_invoice_details(result)
print(result)
