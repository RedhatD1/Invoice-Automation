from extraction_algorithms.invoice.helpers.ML_Entity_Detection import runner
from extraction_algorithms.invoice.helpers.format_dataframe import standardize_df, get_item_list
from extraction_algorithms.invoice.helpers.format_date import get_formatted_date
from extraction_algorithms.invoice.helpers import pdf_reader_modes, extract_table, invoice_details_extraction
from helpers.general_helper import remove_space_from_text


def get(file_name: str) -> dict:
    file_path = "assets/invoices/" + file_name
    invoice_text = pdf_reader_modes.read_invoice(file_path)
    # Plaintext extraction
    ml_dict = runner.ner_extraction(invoice_text)
    # name, shop_name and shipping_address extraction based on ML
    # Can be improved by training model on a larger dataset
    # Current model was trained on only 3 Invoices
    invoice_tables = pdf_reader_modes.read_tables(file_path)
    # Using camelot we extract the table-like part only
    result_table = extract_table.result(invoice_tables)
    """
    A camelot extraction can result in multiple tables
    From pattern matching on the dataframe, we can target tables containing
    specific keywords like 'item', 'product', 'description', 'quantity' etc
    which are usually present in invoice tables
    """
    result_table = standardize_df(result_table)
    # Clean the dataframe to handle invalid cells

    try: # try catch block for ML, to handle KeyError
        if ml_dict['CUSTOMER'] != '':
            name = ml_dict['CUSTOMER']
        else:
            name = invoice_details_extraction.extract_name(invoice_text)
    except KeyError:
        name = ''

    try:
        shop_name = ml_dict['SHOP']
    except KeyError:
        shop_name = ''

    try:
        if ml_dict['SHIPPING_ADDRESS'] != '':
            shipping_address = ml_dict['SHIPPING_ADDRESS']
        else:
            shipping_address = invoice_details_extraction.extract_shipping_address(invoice_text)
    except KeyError:
        shipping_address = ''

    billing_address = invoice_details_extraction.extract_billing_address(invoice_text)
    # ReGeX based extraction
    # Usually if more than one address is present in the invoice, the billing address is separately mentioned
    return {
        "customer_info": {
            "name": name,
            "phone": invoice_details_extraction.extract_phone(invoice_text),
            "email": invoice_details_extraction.extract_email(invoice_text),
            "billing_address": billing_address,
            "shipping_address": shipping_address
        },
        "item_details": get_item_list(result_table),
        "total_amount": remove_space_from_text(invoice_details_extraction.extract_total_amount(invoice_text)),
        "note": '',
        "invoice_info": {
            "shop_name": shop_name,
            "date": get_formatted_date(invoice_text),
            "number": invoice_details_extraction.extract_invoice_number(invoice_text),
        }
    }
