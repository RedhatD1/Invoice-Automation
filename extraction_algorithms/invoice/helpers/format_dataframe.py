import pandas as pd
from helpers import general_helper


def rename_df_name_column(df: pd.DataFrame) -> pd.DataFrame:
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


def rename_unit_price_column(df: pd.DataFrame) -> pd.DataFrame:
    if 'unit_price' not in df.columns:
        # Check if 'items' column exists
        if 'price' in df.columns:
            df = df.rename(columns={'price': 'unit_price'})
        elif 'unitprice' in df.columns:
            df = df.rename(columns={'unitprice': 'unit_price'})
        else:
            df.rename(columns=lambda x: 'unit_price' if 'unit_price' in x else x, inplace=True)
    return df


def rename_df_quantity_column(df: pd.DataFrame) -> pd.DataFrame:
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


def rename_df_amount_column(df: pd.DataFrame) -> pd.DataFrame:
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


def rename_df_discount_column(df: pd.DataFrame) -> pd.DataFrame:
    if 'discount' not in df.columns:
        # Check if 'items' column exists
        if 'discount amount' in df.columns:
            df = df.rename(columns={'discount amount': 'discount'})
        elif 'discount %' in df.columns:
            df = df.rename(columns={'discount %': 'discount'})
        else:
            df.rename(columns=lambda x: 'discount' if 'discount' in x else x, inplace=True)
    return df


def standardize_df(df: pd.DataFrame, currency="Taka") -> pd.DataFrame:
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

    # Space cleaning
    df['unit_price'] = df['unit_price'].apply(lambda x: general_helper.remove_space_from_text(x))
    df['quantity'] = df['quantity'].apply(lambda x: general_helper.remove_space_from_text(x))
    df['amount'] = df['amount'].apply(lambda x: general_helper.remove_space_from_text(x))

    return df


def get_item_list(df: pd.DataFrame) -> list:
    item_list = df.to_dict('records')
    return item_list
