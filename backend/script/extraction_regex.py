from read_pdf import *
import re
import tabula

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


def extract_table(file_path, output_path):
    
    tables = tabula.read_pdf(file_path, stream=True, pages='all', multiple_tables=False)
    if len(tables) > 0:
        return tables[0]
    else:
        return None

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

def main():
    for i in range(1, 13):
        invoice_path = 'invoices/' + str(i) + '.pdf'
        csv_path = 'invoices/' + str(i) + '.csv'
        invoice = read_pdf(invoice_path)
        # print(invoice)
        invoice_number = extract_invoice_number(invoice)
        invoice_addresses = extract_addresses(invoice)
        invoice_table = extract_table(invoice_path, csv_path)

        print(f'\n\n\n\n\n')
        print(f'Invoice {i} -> ')
        print(f'Invoice Number: {invoice_number}')
        print(f'Invoice Addresses: {invoice_addresses}')
        if invoice_table is not None:
            # print(f'{invoice_path} has {len(invoice_table)} table(s)')
            print(f"The table is:")
            print(invoice_table)
            print("------------------------------------------------")
            print(f"The table in JSON format is:")
            table = create_json(invoice_table)
            for row in table:
                print(row)
            
        else:
            print(f'{invoice_path} has no readable tables')
        
        print(f'\n\n\n\n\n')


if __name__ == "__main__":
    main()