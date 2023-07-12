# Used for extracting information other than table data

from datetime import datetime
import re

import nltk


def extract_invoice_number(text):
    # Define patterns or keywords for invoice number extraction
    patterns = ['Invoice No.', 'Order No.', 'Invoice Number', 'Order #']
    for pattern in patterns:
        match = re.search(r'{}(\s*:\s*|\s+)(\w+)'.format(pattern), text, re.IGNORECASE)
        # The code searches for specific patterns ('Invoice No.', 'Order No.', 'Invoice Number', 'Order #')
        # followed by a colon or whitespace, followed by one or more word characters
        # The code ignores case sensitivity
        if match:
            return match.group(2)
        else:
            try:
                text = text.lower()
                patterns = [
                    r'\binv-\w+\b',  # Matches words starting with "INV-" followed by one or more word characters
                    # Matches words containing at least one alphabetical character, one or more digits, and a combination of alphabetical characters and digits
                    r'\b[a-z]+\d+[a-z\d]+\b',
                    # Matches "Invoice No" followed by a colon or period, optional whitespace, and captures a single word, including characters, numbers and hyphens
                    r'(?i)invoice no[:.]\s*(\w+(?:[\w-]*\w)?)',
                    r'(?<=#)\d+',  # Matches one or more digits preceded by a hash symbol (#)
                    # Matches one or more word characters preceded by a hash symbol (#) and a whitespace character
                    r'(?<=#\s)\w+'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    if matches:
                        return matches[0].upper()

            except IndexError:
                return ""
    return ""

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
            month = date_obj.month
            year = date_obj.year
            formatted_date = f'{day}-{month}-{year}'
            return formatted_date

    except Exception as e:
        return ""

def extract_date(text):
    # Define patterns or keywords for invoice date extraction
    patterns = ['Invoice Date', 'Date of Issue', 'Billing Date', 'Order Date', 'Date']

    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            pattern = r'\b(?:\d{1,2}(?:-|\/)\d{1,2}(?:-|\/)\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4})\b'
            matches = re.findall(pattern, text)
            if not matches:
                today = datetime.today()
                formatted_date = today.strftime("%d-%m-%Y")
            else:
                return matches[0]
    return ""


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
        else:
            numbers = re.findall(r'Total\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
            if numbers:
                return numbers[-1]
            else:
                numbers = re.findall(
                    r'Total\s+Amount\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
                if numbers:
                    return numbers[-1]
                else:
                    return ""
    return ""

def extract_phone(text):
    pattern = r"(?:(?:\+|00)88|01)?\d{11}"
    matches = re.findall(pattern, text)
    matches = list(set(matches))
    if matches:
        return matches[-1]
    else:
        return ""


def extract_email(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    matches = re.findall(pattern, text)
    if not matches:
        return ""
    else:
        email = matches[-1]
        return email

def extract_name(text):
    email = extract_email(text)
    username = email.split('@')[0]
    return username
def extract_address(text, patterns):
    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            address = match.group(2)
            return address.strip()  # Return the extracted shipping address
    return ""  # Return "" if no shipping address is found

def extract_shipping_address(text):
    pattern = ['shipping address', 'ship to',  "delivery address", "receiver address", "customer address"]
    shipping_address = extract_address(text=text, patterns=pattern)
    return shipping_address

def extract_billing_address(text):
    pattern = ['billing address', 'bill to']
    billing_address = extract_address(text=text, patterns=pattern)
    return billing_address
