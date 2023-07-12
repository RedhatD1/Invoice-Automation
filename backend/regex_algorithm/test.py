# For testing purposes only
from scripts import reader, utils, details_utils
import re


def extract_address(text, patterns):
    for pattern in patterns:
        match = re.search(r'{}(\s*(.*))'.format(pattern), text, re.IGNORECASE)
        if match:
            address = match.group(2)
            return address.strip()  # Return the extracted shipping address
    return ""  # Return None if no shipping address is found

def extract_shipping_address(text):
    pattern = ['shipping address', 'ship to',  "delivery address", "receiver address", "customer address"]
    shipping_address = extract_address(text=text, patterns=pattern)
    return shipping_address

def extract_billing_address(text):
    pattern = ['billing address', 'bill to']
    billing_address = extract_address(text=text, patterns=pattern)
    return billing_address
