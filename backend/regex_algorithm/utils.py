# Some utility functions for the main script
# Used only for writing minor functions for cleanup

import re
import pandas as pd

def count_max_matches(df, keywords):
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
            first_match_column = matches.idxmax() # Find first match column
            last_match_column = matches[::-1].idxmax()  # Find last match column

    return max_matches, max_match_index, first_match_column, last_match_column


def lru_crop_df(df, row, first_column, last_column): # Left Right Up crop DataFrame
    df = df.iloc[row:, first_column:last_column+1]
    df = df.reset_index(drop=True)
    return df

def lower_crop_df(df):
    column_data = df.iloc[:, 0]
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

def df_first_row_to_header(df):
    # df.loc[len(df)] = pd.Series() # Add empty row at the end
    new_header = df.iloc[0] #grab the first row for the header
    new_header = pd.Series([re.sub(r'[^a-zA-Z]', '', name) for name in
                            new_header])  # Convert the list to a Pandas Series and remove non-alphabetic characters

    df = df[1:] #take the data less the header row
    df.columns = new_header.str.lower() #set the header row as the df header
    df.columns = df.columns.str.replace('\n', '\\') # Remove newline characters from header
    df = df.replace('\n', ' ', regex=True)
    df = df.reset_index(drop=True)
    return df

def extract_table(tables, header_keywords):
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

def crop_table(table, top_index, left_index, right_index):
    left_right_up_cropped_table = lru_crop_df(table, top_index, left_index, right_index)
    left_right_up_down_cropped_table = lower_crop_df(left_right_up_cropped_table)
    result_table = df_first_row_to_header(left_right_up_down_cropped_table)
    return result_table

def extract_item_table(tables):
    header_keywords = ["item", "product", "description", "quantity", "discount", "unit", "price", "amount", "total"]
    item_table, starting_index, starting_column, ending_column = extract_table(tables, header_keywords)
    result_table = crop_table(item_table, starting_index, starting_column, ending_column)
    return result_table
