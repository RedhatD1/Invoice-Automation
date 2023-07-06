from read_pdf import read_pdf
import re
import pandas as pd
import json
import spacy

def extract_lines(text):
    total_line_number = None
    description_line_number = None

    lines = text.split('\n')

    # Find the line number of the line containing "total"
    for i, line in enumerate(lines):
        if 'total' in line.lower():
            total_line_number = i

    # Find the line number of the line containing "description"
    for i, line in enumerate(lines):
        if 'description' in line.lower():
            description_line_number = i

    # Check if "description" is found
    if description_line_number is None:
        # Find the line number of the line containing "price"
        for i, line in enumerate(lines):
            if 'price' in line.lower():
                description_line_number = i
                break

    # Append the lines between "description" and "total"
    appended_lines = []
    if description_line_number is not None and total_line_number is not None:
        appended_lines = lines[description_line_number:total_line_number + 1]

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

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    result['phone']= extract_contact_numbers(text)


    for token in doc:
        if token.like_email:
            result["email"] = token.text
            break

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


def parse_table_data(table_data):
    rows = text.split('\n')
    headers = rows[0].split()
    data_rows = [row.split() for row in rows[1:]]

    # Fill empty cells with NaN
    max_length = max(len(row) for row in data_rows)
    data_rows = [row + [''] * (max_length - len(row)) for row in data_rows]

    df = pd.DataFrame(data_rows, columns=headers)
    df = df.replace('', float('nan'))

    print(df)
    return df

for i in range(1,13):
    text = read_pdf(f'invoices/{i}.pdf')
    # print(extract_information(text))
    print(i)
    table_field = extract_lines(text)
    # parse_table_data(table_field)
    print('\n')
