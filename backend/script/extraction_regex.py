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


def extract_table(file_path):
    
    tables = tabula.read_pdf(file_path, stream=True, pages='all', multiple_tables=False)
    
    if len(tables) > 0:
        return tables[0]
    else:
        return None

def main():
    for i in range(1, 13):
        path = 'invoices/' + str(i) + '.pdf'
            # path = 'invoices/8.pdf'
        invoice = read_pdf(path)
        # print(invoice)
        invoice_number = extract_invoice_number(invoice)
        invoice_tables = extract_table(path)
        print(f'Invoice {i} -> Invoice Number: {invoice_number}')
        if invoice_tables is not None:
            print(f'{path} has {len(invoice_tables)} table(s)')
            print(invoice_tables)
        else:
            print(f'{path} has no readable tables')
        print("-----------------------")
if __name__ == "__main__":
    main()