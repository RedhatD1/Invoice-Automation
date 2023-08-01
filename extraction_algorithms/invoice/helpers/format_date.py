# Used for formatting the DataFrame and creating JSON
from datetime import datetime

from extraction_algorithms.invoice.helpers import invoice_details_extraction
from extraction_algorithms.invoice.helpers import format_dataframe


def standardize_date(text: str) -> str:
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
            month = date_obj.strftime("%B")
            year = date_obj.year
            formatted_date = f'{day} {month}, {year}'
            return formatted_date

    except Exception as e:
        return ""


def get_formatted_date(text: str) -> str:
    raw_data = invoice_details_extraction.extract_date(text)
    formatted_date = standardize_date(raw_data)
    return formatted_date
