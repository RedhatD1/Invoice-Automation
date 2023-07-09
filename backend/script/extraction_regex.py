from read_pdf import *
import re
import tabula
from datetime import datetime

def extract_invoice_number(text):
    try:
        text = text.lower()
        patterns = [
            r'\binv-\w+\b',  # Matches words starting with "INV-" followed by one or more word characters
            r'\b[a-z]+\d+[a-z\d]+\b',  # Matches words containing at least one alphabetical character, one or more digits, and a combination of alphabetical characters and digits
            r'(?i)invoice no[:.]\s*(\w+(?:[\w-]*\w)?)',  # Matches "Invoice No" followed by a colon or period, optional whitespace, and captures a single word, including characters, numbers and hyphens
            r'(?<=#)\d+',  # Matches one or more digits preceded by a hash symbol (#)
            r'(?<=#\s)\w+'  # Matches one or more word characters preceded by a hash symbol (#) and a whitespace character
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].upper()
            
    except IndexError:
        return None

def create_json(df):
    # Convert DataFrame to JSON for each row
    json_objects = []
    for _, row in df.iterrows():
        json_objects.append(row.to_json())

    return json_objects

def clean_header(df):
    # Check if any of the desired column names exist in the DataFrame
    if not any(col_name in df.columns for col_name in ["Description", "Quantity", "Unit Price", "Amount"]):
        # Replace column names with values from the first row
        df.columns = df.iloc[0]
        # Reset index
        df.reset_index(drop=False, inplace=True)
        
    return df

def remove_currency(text):
    # Remove currency symbols
    text = re.sub(r'\$|\£|\€|\¥|\₹', '', text)
    # Remove commas
    text = re.sub(r',', '', text)
    return text

def clean_tables(df):
    df = df.dropna(thresh=df.shape[1]-1)
    # df = clean_header(df) # Use with caution
    return df

def extract_table(file_path):
    tables1 = tabula.read_pdf(file_path, stream=True, pages='all', multiple_tables=False)
    if len(tables1) > 0:
        table = clean_tables(tables1[0])
        if 'currency' not in table.columns:
            # Add the column with default value to all rows
            table['currency'] = 'taka'
        current_column_names = table.columns.tolist()
        # Create a dictionary to map index to new column names
        new_column_names = {0: 'name', 1: 'description', 2: 'quantity', 3: 'unit_price', 4: 'amount', 5: 'currency'}

        # Rename columns based on index
        table = table.set_axis([new_column_names.get(idx, col) for idx, col in enumerate(current_column_names)], axis=1)
        # Remove currency symbols and commas
        table['amount'] = table['amount'].apply(remove_currency)
        return table
    else:
        return []

import spacy
def extract_addresses(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    addresses = set()  # Use a set instead of a list

    for ent in doc.ents:
        if ent.label_ == "GPE":
            addresses.add(ent.text)

    concatenated_addresses = ', '.join(addresses)
    return concatenated_addresses

def remove_non_alphanumeric(text):
    # Remove brackets
    text = re.sub(r'\[|\]|\(|\)', '', text)
    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def extract_total_numbers(text):
    numbers = re.findall(r'Total\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
    if numbers:
        return numbers[-1]
    else:
        numbers = re.findall(r'Total\s+Amount\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if numbers:
            return numbers[-1]
        else:
            return None
def extract_date(input_string):
    pattern = r'\b(?:\d{1,2}(?:-|\/)\d{1,2}(?:-|\/)\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4})\b'
    matches = re.findall(pattern, input_string)
    if not matches:
        today = datetime.today()
        formatted_date = today.strftime("%d-%m-%Y")
    else:
        return matches[0]

def extract_phone(text):
    pattern = r"(\+?88)?01[3-9]\d{8}"
    matches = re.findall(pattern, text)
    if not matches:
        return "None"
    else:
        return matches[0]

def extract_email(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    matches = re.findall(pattern, text)
    if not matches:
        return "None"
    else:
        return matches[0]



def execute_script(input_path):
    invoice_path = f'invoices/{input_path}'
    invoice = read_pdf(invoice_path)
    invoice_number = extract_invoice_number(invoice)
    invoice_addresses = extract_addresses(invoice)
    invoice_table = extract_table(invoice_path)
    invoice_amount = extract_total_numbers(remove_non_alphanumeric(invoice))
    invoice_amount = remove_currency(invoice_amount)
    invoice_phone = extract_phone(invoice)
    invoice_email = extract_email(invoice)
    invoice_dict = invoice_table.to_dict(orient="records")
    invoice_name = input_path.split(".")[0]
    
    invoice_date = extract_date(invoice)
    data = {
        "customer_info": {
            "name": invoice_name,
            "phone": invoice_phone,
            "email": invoice_email,
            "billing_address": invoice_addresses,
            "shipping_address": invoice_addresses,
        },
        "item_details": invoice_dict,
        "total_amount": invoice_amount,
        "note": "Thank you.",
        "invoice_info": {
            "date": invoice_date,
            "number": invoice_number,
        },
    }
    return data

def main():
    # Execute the script
    json_data = execute_script('invoices/2.pdf')
    print(json_data)

if __name__ == "__main__":
    main()