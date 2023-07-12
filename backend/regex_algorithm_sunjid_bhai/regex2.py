import PyPDF2
import json
import numpy as np
import tempfile
import re
import tabula
from camelot import read_pdf
import pandas as pd


# Create your views here.


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    text = ''
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text


# Extract Invoice Number

def extract_invoice_number(text):
    # Define patterns or keywords for invoice number extraction
    patterns = ['Invoice No.', 'Order No.', 'Invoice Number', 'Order #']
    for pattern in patterns:
        match = re.search(r'{}(\s*:\s*|\s+)(\w+)'.format(pattern), text, re.IGNORECASE)
        if match:
            return match.group(2)
    return None


# Extract Invoice Date
def extract_invoice_date(text):
    # Define patterns or keywords for invoice date extraction
    patterns = ['Invoice Date', 'Date of Issue', 'Billing Date', 'Order Date', 'Date']
    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


# Extract Total Amount
def extract_total_amount(text):
    # Define patterns or keywords for total amount extraction
    patterns = ['Total', 'TOTAL', 'Amount Due', 'Total Payable', 'Grand Total']
    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            line = match.group(2).replace(',', '')
            pattern = r'(\d+\.\d+)'
            match = re.search(pattern, line)
            if match:
                result = match.group(1)
                return result
    return None


# Extract List of Ordered Items

def extract_table_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    table_label = [table.columns.tolist() for table in tables]
    table_header = None  # Initialize the result variable

    for sublist in table_label:
        lowercase_sublist = [item.lower() for item in sublist]  # Convert sublist elements to lowercase
        if 'item' in lowercase_sublist or 'product' in lowercase_sublist or 'product name' in lowercase_sublist or 'item name' in lowercase_sublist:
            table_header = sublist
            break
    table_data = [table.values.tolist() for table in tables]
    clean_table = []
    for data in table_data[1]:
        # clean_list = [x for x in data if str(x).lower() != 'nan']
        # dic = {}
        # if len(clean_list) >= 2:
        #     dic[clean_list[0]] = clean_list[1]
        #     clean_table.append(dic)
        # else:
        #     clean_table.append(clean_list)
        if len(data) == len(table_header):
            my_dict = {k: v for k, v in zip(table_header, data)}
            clean_table.append(my_dict)
    return clean_table


def extract_table_using_camelot(pdf_path):
    tables = read_pdf(pdf_path, pages="all", flavor='stream')
    allin = []
    last_table_index = tables.n - 1  # last table grab kortese

    last_table = tables[last_table_index]

    table_data = last_table.df
    table_data = table_data.iloc[3:]  # Extra info remove kortese

    allin.append(table_data)
    df = pd.concat(allin)
    df = df.reset_index(drop=True)
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.reset_index(drop=True)
    df = df.replace('', np.nan)
    df = df.dropna(how='any')
    dict_list = []
    for index, row in df.iterrows():
        dict_list.append(row.to_dict())
    return dict_list


def standardize_date(text):
    try:
        date_obj = None
        date_formats = [
            "%d-%m-%y",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%d/%m/%y",
            "%d.%m.%Y",
            "%d%m%Y",
            "%d %b, %Y",
            "%d %b %Y",
            "%d %B, %Y",
            "%d %B %Y",
            "%B %d, %Y",
            "%m-%d-%Y",
            "%m/%d/%Y",
            "%m-%d-%y",
            "%B %d %Y",
            "%b %d, %Y",
            "%b %d %Y",
            "%m%Y",

            "%Y/%m/%d",
            "%Y.%m.%d",
            "%Y%m%d",
            "%Y/%m/%d",
            "%Y%m",
            "%Y-%m-%d",
            "%Y-%d-%m",
            "%Y",
            "%y",
        ]

        for format_string in date_formats:
            try:
                date_obj = datetime.strptime(text, format_string)
                break  # Exit the loop if a valid date format is found
            except ValueError:
                continue  # Continue to the next format if the current one raises an exception

        if date_obj is None:
            return ""
        else:
            day = date_obj.day
            month = date_obj.strftime("%B")
            year = date_obj.year
            formatted_date = f'{day} {month}, {year}'
            return formatted_date

    except Exception as e:
        return ""


# Main function
def extract_information_from_invoice(pdf_path):
    # Step 1: Preprocessing
    pdf_path = 'invoices/' + pdf_path
    extracted_text = extract_text_from_pdf(pdf_path)
    invoice_number = extract_invoice_number(extracted_text)
    invoice_date = extract_invoice_date(extracted_text)
    total_amount = extract_total_amount(extracted_text)
    # ordered_items = extract_ordered_items(extracted_text)
    # table_data = extract_table_from_pdf(pdf_path)
    table = extract_table_using_camelot(pdf_path)
    item_details = []
    for dict in table:
        new_dict = {(
                        "item" if key.lower() == "items" or key.lower() == "item" or key.lower() == "product" or key.lower() == "products" or key.lower() == "item name" or key.lower() == "product name" else key): value if value is not None else ""
                    for key, value in dict.items()}
        new_dict = {("unit_price" if "unit" in key.lower() else key): value if value is not None else "" for key, value
                    in new_dict.items()}
        new_dict = {(
                        "quantity" if key.lower() == "quantity" or key.lower() == "qty" else key): value if value is not None else ""
                    for key, value in new_dict.items()}
        new_dict = {("amount" if "amount" in key.lower() else key): value if value is not None else "" for key, value in
                    new_dict.items()}
        new_dict = {("discount" if "discount" in key.lower() else key): value if value is not None else "" for
                    key, value in new_dict.items()}
        new_dict["currency"] = "taka"
        item_details.append(new_dict)

        invoice_info = {
            "invoice_info": {
                "date": standardize_date(str(invoice_date)),
                "number": str(invoice_number)
            },
            "total_amount": str(total_amount),
            "item_details": item_details,
            "note": "",
            "customer_info": {
                "name": "",
                "phone": "",
                "email": "",
                "billing_address": "",
                "shipping_address": ""
            }

        }
    return invoice_info
