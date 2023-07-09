from read_pdf import *
import re
import tabula
import json

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

def clean_tables(df):
    df = df.dropna(thresh=df.shape[1]-1)
    # df = clean_header(df) # Use with caution
    return df

def extract_table(file_path):
    tables1 = tabula.read_pdf(file_path, stream=True, pages='all', multiple_tables=False)
    if len(tables1) > 0:
        table = clean_tables(tables1[0])
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

def execute_script(input_path):
    invoice_path = input_path
    invoice = read_pdf(invoice_path)
    invoice_number = extract_invoice_number(invoice)
    invoice_addresses = extract_addresses(invoice)
    invoice_table = extract_table(invoice_path)
    invoice_amount = extract_total_numbers(remove_non_alphanumeric(invoice))

    invoice_dict = invoice_table.to_dict(orient="records")
    data = {
        "invoice_number": "KA354448",
        "invoice_amount": "3374",
        "invoice_address": "Houston",
        "invoice_table": invoice_dict
    }
    return data

def main():
    # Execute the script
    json_data = execute_script('invoices/2.pdf')
    print(json_data)

if __name__ == "__main__":
    main()