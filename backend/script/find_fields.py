from read_pdf import read_pdf
import re
import pandas as pd
import json
import spacy

def extract_lines(text):
    last_digit_line_number = None
    description_line_number = None

    lines = text.split('\n')

    # Find the line number of the last available digit
    for i, line in enumerate(lines):
        if any(char.isdigit() for char in line):
            last_digit_line_number = i

    # Find the line number of the line containing "description"
    for i, line in enumerate(lines):
        if 'description' in line.lower():
            description_line_number = i

    # Append the lines between "description" and the last available digit
    appended_lines = []
    if description_line_number is not None and last_digit_line_number is not None:
        appended_lines = lines[description_line_number:last_digit_line_number + 1]

    table_field = '\n'.join(appended_lines)

    print('\n')
    print(table_field)
    return table_field


def extract_contact_numbers(text):
    pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    matches = re.findall(pattern, text)
    if not matches:
      return "No matches"
    return matches[0]


def create_dataframe(text):
    lines = text.split('\n')
    headers = lines[0].split()
    
    table_data = []
    for line in lines[1:]:
        if line:
            table_data.append(line.split())
    
    df = pd.DataFrame(table_data, columns=headers)
    print(df)
    return df

def extract_information(text):
    result = {}

    # Load the Spacy English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the text with Spacy
    doc = nlp(text)

    # Extract phone number
    result['phone']= extract_contact_numbers(text)

    # Extract email address
    for token in doc:
        if token.like_email:
            result["email"] = token.text
            break

    # Extract billing and shipping addresses
    addresses = []
    for i, token in enumerate(doc[:-1]):
        if token.text == "Address":
            address = {
                "address": doc[i+1].text,
                "city": doc[i+2].text,
                "state": doc[i+3].text,
                "zipcode": doc[i+4].text
            }
            addresses.append(address)

    if len(addresses) >= 2:
        result["billing_address"] = addresses[0]
        result["shipping_address"] = addresses[1]

    return json.dumps(result, indent=4)

text = read_pdf('invoices/8.pdf')
print(extract_information(text))
table_field = extract_lines(text)
