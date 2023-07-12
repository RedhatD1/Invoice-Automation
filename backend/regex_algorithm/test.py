# For testing purposes only
from datetime import datetime

# getting the current date and time
date_strings = ["23 May, 2023", "May 23, 2023", "13-5-2023", "13-05-2023", "13-5-23", "13/5/2023", "13/05/2023", "13/5/23", "Jul 4, 2023"]
for date_string in date_strings:
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
                date_obj = datetime.strptime(date_string, format_string)
                break  # Exit the loop if a valid date format is found
            except ValueError:
                continue  # Continue to the next format if the current one raises an exception

        if date_obj is None:
            print("Invalid date format")
        else:
            day = date_obj.day
            month = date_obj.month
            year = date_obj.year
            print("Day:", day)
            print("Month:", month)
            print("Year:", year)

    except Exception as e:
        print("An exception occurred:", str(e))


# Format codes:
# - `%a`: Weekday name, abbreviated (e.g., Mon, Tue, etc.)
# - `%A`: Weekday name, full (e.g., Monday, Tuesday, etc.)
# - `%b`: Month name, abbreviated (e.g., Jan, Feb, etc.)
# - `%B`: Month name, full (e.g., January, February, etc.)
# - `%c`: Locale's appropriate date and time representation
# - `%d`: Day of the month as a zero-padded decimal number (e.g., 01, 02, ..., 31)
# - `%H`: Hour in 24-hour format as a zero-padded decimal number (e.g., 00, 01, ..., 23)
# - `%I`: Hour in 12-hour format as a zero-padded decimal number (e.g., 01, 02, ..., 12)
# - `%j`: Day of the year as a zero-padded decimal number (e.g., 001, 002, ..., 366)
# - `%m`: Month as a zero-padded decimal number (e.g., 01, 02, ..., 12)
# - `%M`: Minute as a zero-padded decimal number (e.g., 00, 01, ..., 59)
# - `%p`: Locale's equivalent of either AM or PM
# - `%S`: Second as a zero-padded decimal number (e.g., 00, 01, ..., 59)
# - `%U`: Week number of the year (Sunday as the first day of the week) as a zero-padded decimal number (e.g., 00, 01, ..., 53)
# - `%w`: Weekday as a decimal number, where 0 represents Sunday and 6 represents Saturday
# - `%W`: Week number of the year (Monday as the first day of the week) as a zero-padded decimal number (e.g., 00, 01, ..., 53)
# - `%x`: Locale's appropriate date representation
# - `%X`: Locale's appropriate time representation
# - `%y`: Year without century as a zero-padded decimal number (e.g., 00, 01, ..., 99)
# - `%Y`: Year with century as a decimal number (e.g., 0001, 0002, ..., 2019, 2020, etc.)
# - `%z`: UTC offset in the form +HHMM or -HHMM (empty string if the object is naive)
# - `%Z`: Time zone name (empty string if the object is naive)
# - `%%`: A literal '%' character
