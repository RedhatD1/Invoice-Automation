# Used for formatting the DataFrame and creating JSON

from extraction_algorithms.invoice.helpers import details_utils


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
        elif 'product' in df.columns:
            df = df.rename(columns={'product': 'name'})
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


from helpers import general_helper


def standardize_df(df, currency="Taka"):
    df = rename_df_name_column(df)
    df = rename_unit_price_column(df)
    df = rename_df_quantity_column(df)
    df = rename_df_amount_column(df)
    df = rename_df_discount_column(df)
    df['currency'] = currency

    # Adding empty columns if they don't exist
    columns_to_fill = ['unit_price', 'quantity', 'amount', 'discount']
    for column in columns_to_fill:
        if column not in df.columns:
            # If the column doesn't exist, create it with empty strings as default value
            df[column] = ''

    if df['unit_price'].dtype == 'object':
        df['unit_price'] = df['unit_price'].str.replace(r'[^\d.,]+', '', regex=True)

    df[['unit_price', 'quantity', 'amount', 'discount']] = df[['unit_price', 'quantity', 'amount', 'discount']].replace(
        '', 0)

    # Converting all cells to string datatype for streamlining the process
    df = df.astype(str)

    # Cleaning multiple entries in the dataframe
    df['unit_price'] = df['unit_price'].str.split().str[0]
    df['quantity'] = df['quantity'].str.split().str[0]
    df['amount'] = df['amount'].str.split().str[0]

    # Whitespace cleaning
    df['unit_price'] = df['unit_price'].apply(lambda x: general_helper.remove_space_from_text(x))
    df['quantity'] = df['quantity'].apply(lambda x: general_helper.remove_space_from_text(x))
    df['amount'] = df['amount'].apply(lambda x: general_helper.remove_space_from_text(x))

    return df


def get_json(df):
    json = df.to_dict('records')
    return json


def get_formatted_date(text):
    raw_data = details_utils.extract_date(text)
    formatted_date = details_utils.standardize_date(raw_data)
    return formatted_date
