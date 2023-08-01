# Some utility functions for the main script
# Used only for writing minor functions for cleanup
from camelot.core import TableList
from extraction_algorithms.invoice.helpers.format_dataframe import crop_table, extract_table
import pandas as pd


def result(tables: TableList) -> pd.DataFrame:
    header_keywords = ["item", "product", "description", "quantity", "discount", "unit", "price", "amount", "total",
                       "s.n", "product name", "unit price"]
    item_table, starting_index, starting_column, ending_column = extract_table(tables, header_keywords)
    result_table = crop_table(item_table, starting_index, starting_column, ending_column)

    return result_table
