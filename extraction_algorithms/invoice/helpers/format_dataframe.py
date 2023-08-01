import re

import pandas as pd
from camelot.core import TableList

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


def lru_crop_df(df, row, first_column, last_column) -> pd.DataFrame:  # Left Right Up crop DataFrame
    df = df.iloc[row:, first_column:last_column + 1]
    df = df.reset_index(drop=True)
    return df


def lower_crop_df(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Assuming df is your DataFrame
        column_data = df.iloc[:, 0]
    except IndexError:
        # Handle the case when the DataFrame is empty or the column index is out of range
        column_data = pd.DataFrame()
    index = 0
    # Printing all rows of the column
    for row in column_data:
        if not row:
            # print(f'End row: {index}') # debug
            break
        else:
            # print(row)
            index += 1
    df = df.iloc[:index, :]
    return df


def df_first_row_to_header(df: pd.DataFrame) -> pd.DataFrame:
    try:
        if df.empty:
            # Handle the case when the DataFrame is empty
            return pd.DataFrame()

        new_header = df.iloc[0]  # grab the first row for the header
        new_header = pd.Series([re.sub(r'[^a-zA-Z]', '', name) for name in new_header])

        df = df[1:]  # take the data less the header row
        df.columns = new_header.str.lower()  # set the header row as the df header
        df.columns = df.columns.str.replace('\n', '\\')  # Remove newline characters from header
        df = df.replace('\n', ' ', regex=True)
        df = df.reset_index(drop=True)
        return df
    except IndexError:
        # Handle any other potential errors here if needed
        return pd.DataFrame()


def extract_table(tables: TableList, header_keywords: list) -> (pd.DataFrame, int, int, int):
    max_keyword_matches = 0
    best_table = pd.DataFrame()  # Empty DataFrame by default in case no match
    best_table_index = 0
    best_table_first_column = 0
    best_table_last_column = 0
    for table in tables:
        df = table.df
        no_of_matches, match_index, first_match_column, last_match_column = count_max_matches(df,
                                                                                              header_keywords)  # Count number of keywords found in table header
        # print(f'Number of keywords found: {no_of_matches}')  # Debug
        # print(f'Table:\n{df}')  # Debug
        if no_of_matches > max_keyword_matches:  # If more keywords found than previous table
            max_keyword_matches = no_of_matches  # Update max_keyword_matches
            best_table = df  # Update best_table
            best_table_index = match_index  # Update best_table_index
            best_table_first_column = first_match_column  # Update best_table_column
            best_table_last_column = last_match_column  # Update best_table_column
    return best_table, best_table_index, best_table_first_column, best_table_last_column


def crop_table(table: pd.DataFrame, top_index: int, left_index: int, right_index: int) -> pd.DataFrame:
    left_right_up_cropped_table = lru_crop_df(table, top_index, left_index, right_index)
    left_right_up_down_cropped_table = lower_crop_df(left_right_up_cropped_table)
    result_table = df_first_row_to_header(left_right_up_down_cropped_table)
    return result_table


def count_max_matches(df: pd.DataFrame, keywords: list) -> (int, int, int, int):
    max_matches = 0
    max_match_index = 0
    first_match_column = 0
    last_match_column = 0

    for index, row in df.iterrows():
        matches = row.str.contains('|'.join(keywords), case=False)
        num_matches = matches.sum()

        if num_matches > max_matches:
            max_matches = num_matches
            max_match_index = index
            first_match_column = matches.idxmax()  # Find first match column
            last_match_column = matches[::-1].idxmax()  # Find last match column

    return max_matches, max_match_index, first_match_column, last_match_column
