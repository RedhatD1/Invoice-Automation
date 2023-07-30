from extraction_algorithms.invoice.helpers.ML_Entity_Detection import runner
from extraction_algorithms.invoice.helpers.json_helper import standardize_df, get_json, get_formatted_date
from extraction_algorithms.invoice.helpers import reader, utils, details_utils
from helpers.general_helper import remove_space_from_text


def get(file_name):
    file_path = "documents/invoices/" + file_name
    invoice_text = reader.read_invoice(file_path)
    ml_dict = runner.ner_extraction(invoice_text)
    invoice_tables = reader.read_tables(file_path)
    result_table = utils.extract_item_table(invoice_tables)
    result_table = standardize_df(result_table)

    # try catch block for ML
    try:
        if ml_dict['CUSTOMER'] != '':
            name = ml_dict['CUSTOMER']
        else:
            name = details_utils.extract_name(invoice_text)
    except Exception as e:
        name = ''

    try:
        shop_name = ml_dict['SHOP']
    except Exception as e:
        shop_name = ''

    try:
        if ml_dict['SHIPPING_ADDRESS'] != '':
            shipping_address = ml_dict['SHIPPING_ADDRESS']
        else:
            shipping_address = details_utils.extract_shipping_address(invoice_text)
    except Exception as e:
        shipping_address = ''

    billing_address = details_utils.extract_billing_address(invoice_text)

    return {
        "customer_info": {
            "name": name,
            "phone": details_utils.extract_phone(invoice_text),
            "email": details_utils.extract_email(invoice_text),
            "billing_address": billing_address,
            "shipping_address": shipping_address
        },
        "item_details": get_json(result_table),
        "total_amount": remove_space_from_text(details_utils.extract_total_amount(invoice_text)),
        "note": '',
        "invoice_info": {
            "shop_name": shop_name,
            "date": get_formatted_date(invoice_text),
            "number": details_utils.extract_invoice_number(invoice_text),
        }
    }
