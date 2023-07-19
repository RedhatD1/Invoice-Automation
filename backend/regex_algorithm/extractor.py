# Used for formatting the DataFrame and creating JSON

from backend.regex_algorithm import details_utils, reader, utils
from backend.regex_algorithm.ML_Entity_Detection import runner
import re
def rename_df_name_column(df):
    if 'name' not in df.columns:
        # Check if 'items' column exists
        if 'items' in df.columns:
            df = df.rename(columns={'items': 'name'})
        elif 'item' in df.columns:
            df = df.rename(columns={'item': 'name'})
        # Check if 'description' column exists
        elif 'description' in df.columns:
            df = df.rename(columns={'description': 'name'})
        else:
            df.rename(columns=lambda x: 'name' if 'name' in x else x, inplace=True)
    return df

def rename_unit_price_column(df):
    if 'unit_price' not in df.columns:
        # Check if 'items' column exists
        if 'price' in df.columns:
            df = df.rename(columns={'price': 'unit_price'})
        elif 'unitprice' in df.columns:
            df = df.rename(columns={'unitprice': 'unit_price'})
        else:
            df.rename(columns=lambda x: 'unit_price' if 'unit_price' in x else x, inplace=True)
    return df

def rename_df_quantity_column(df):
    if 'quantity' not in df.columns:
        # Check if 'items' column exists
        if 'qty' in df.columns:
            df = df.rename(columns={'qty': 'quantity'})
        # Check if 'description' column exists
        elif 'unit' in df.columns:
            df = df.rename(columns={'unit': 'quantity'})
        else:
            df.rename(columns=lambda x: 'quantity' if 'quantity' in x else x, inplace=True)
    return df

def rename_df_amount_column(df):
    if 'amount' not in df.columns:
        # Check if 'items' column exists
        if 'total' in df.columns:
            df = df.rename(columns={'total': 'amount'})
        elif 'total price' in df.columns:
            df = df.rename(columns={'total price': 'amount'})
        elif 'total amount' in df.columns:
            df = df.rename(columns={'total amount': 'amount'})
        else:
            df.rename(columns=lambda x: 'amount' if 'amount' in x else x, inplace=True)
    return df

def rename_df_discount_column(df):

    if 'discount' not in df.columns:
        # Check if 'items' column exists
        if 'discount amount' in df.columns:
            df = df.rename(columns={'discount amount': 'discount'})
        elif 'discount %' in df.columns:
            df = df.rename(columns={'discount %': 'discount'})
        else:
            df.rename(columns=lambda x: 'discount' if 'discount' in x else x, inplace=True)
    return df
def standardize_df(df, currency="Taka"):
    df = rename_df_name_column(df)
    df = rename_unit_price_column(df)
    df = rename_df_quantity_column(df)
    df = rename_df_amount_column(df)
    df = rename_df_discount_column(df)
    df['currency'] = currency
    return df
def get_json(df):
    json = df.to_dict('records')
    return json

<<<<<<< Updated upstream
def convert_to_json_template(df, name="", phone="", email="", billing_address="", shipping_address="", items=[], total_amount=0, note="", date="", number=""):
=======
def get_formatted_date(text):
    raw_data = details_utils.extract_date(text)
    print(raw_data)
    formatted_date = details_utils.standardize_date(raw_data)
    return formatted_date

def convert_to_json_template(df, name="", shop_name="", phone="", email="", billing_address="", shipping_address="", items=[], total_amount=0, note="", date="", number=""):
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    items = get_json(df)
    json_data = {
        "customer_info": {
            "name": name,
            "phone": phone,
            "email": email,
            "billing_address": billing_address,
            "shipping_address": shipping_address
        },
        "item_details": items,
        "total_amount": total_amount,
        "note": note,
        "invoice_info": {
            "shop_name": shop_name,
            "date": date,
            "number": number,
            "shop_name": shop_name
        }
    }
    return json_data

def get_json_formatted(file_name):
    file_path = "invoices/" + file_name
    invoice_text = reader.read_invoice(file_path)
<<<<<<< Updated upstream
    # details_utils.ner_extraction(invoice_text)  # ML
=======
    ml_dict = runner.ner_extraction(invoice_text)
>>>>>>> Stashed changes
    invoice_tables = reader.read_tables(file_path)
    result_table = utils.extract_item_table(invoice_tables)
    result_table = standardize_df(result_table)

    if ml_dict['CUSTOMER'] != '':
        name = ml_dict['CUSTOMER']
    else:
        name = details_utils.extract_name(invoice_text)

    shop_name = ml_dict['SHOP']

    if ml_dict['SHIPPING_ADDRESS'] != '':
        shipping_address = ml_dict['SHIPPING_ADDRESS']
    else:
        shipping_address = details_utils.extract_shipping_address(invoice_text)

    billing_address = details_utils.extract_billing_address(invoice_text)

    json_data = convert_to_json_template(df=result_table,
<<<<<<< Updated upstream
                                         name=details_utils.extract_name(invoice_text),
                                         # shop_name=details_utils.extract_shop_name(invoice_text),
                                         phone=details_utils.extract_phone(invoice_text),
                                         email=details_utils.extract_email(invoice_text),
                                         date=details_utils.extract_date(invoice_text),
=======
                                         name=name,
                                         shop_name=shop_name,
                                         phone=details_utils.extract_phone(invoice_text),
                                         email=details_utils.extract_email(invoice_text),
                                         billing_address=billing_address,
                                         shipping_address=shipping_address,
                                         date=get_formatted_date(invoice_text),
>>>>>>> Stashed changes
                                         number=details_utils.extract_invoice_number(invoice_text))
    return json_data
