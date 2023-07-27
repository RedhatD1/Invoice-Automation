import re
from datetime import datetime

def standardize_date(date_string):
    date_range_pattern = r"\s*\d{2}/\d{4}"
    month_year_pattern = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b"
    # Check if the input date is in the date_range_pattern format
    if re.match(date_range_pattern, date_string):
        month, year = date_string.split('/')
        month_name = datetime.strptime(month, '%m').strftime('%B')
        return f"{month_name} {year}"

    # Check if the input date is in the month_year_pattern format
    elif re.match(month_year_pattern, date_string):
        try:
            date_obj = datetime.strptime(date_string, '%b %Y')
        except ValueError:
            # If '%b %Y' format fails, try with '%B %Y' format
            date_obj = datetime.strptime(date_string, '%B %Y')
        return date_obj.strftime('%B %Y')

    # Return the original date if it doesn't match any of the patterns
    return date_string

def convert_to_fraction_of_year(date_string):
    try:
        # Parse the date string into a datetime object with format 'Month Year'
        date_obj = datetime.strptime(date_string, '%B %Y')
        # Create a reference datetime object for January 1st of the same year
        reference_date = datetime(date_obj.year, 1, 1)
        # Calculate the difference in months between the two dates
        months_difference = (date_obj.year - reference_date.year) * 12 + (date_obj.month - reference_date.month)
        # Calculate the fraction of a year
        fraction_of_year = months_difference / 12.0 + date_obj.year
        return fraction_of_year  # Round the result to two decimal places
    except ValueError:
        # If the input date_string is in an invalid format, handle the error as needed
        return 0

def preprocess(date_string):
    date_format = "%B %Y"
    if "-" in date_string:
        start_date, end_date = date_string.split("-")
        start_date = start_date.strip()
        end_date = end_date.strip()

        if start_date.lower() == "present":
            start_date = datetime.now().strftime(date_format)
        if end_date.lower() == "present":
            end_date = datetime.now().strftime(date_format)

        start_date = standardize_date(start_date)
        end_date = standardize_date(end_date)

        start_date_frac = convert_to_fraction_of_year(start_date)
        end_date_frac = convert_to_fraction_of_year(end_date)
        exp = end_date_frac - start_date_frac
        if exp < 0:
            return 0
        else:
            return exp
    else:
        return 0

def sum_experience(experience_list):
    sum = 0
    for exp in experience_list:
        sum += exp
    return sum

def extractDateRanges(input_text):
    input_text = input_text.replace('\xa0', ' ')
    date_range_pattern = r"\d{2}/\d{4}\s*-\s*(?:present|\d{2}/\d{4})"
    month_year_pattern = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b\s*-\s*(?:present|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b)"
    combined_pattern = rf"{date_range_pattern}|{month_year_pattern}"

    matches = re.findall(combined_pattern, input_text, re.IGNORECASE)
    print(input_text)
    standardMatches = [preprocess(match) for match in matches]
    expYears = sum_experience(standardMatches)
    return round(expYears,2)

# input_text = """
# 09/2018 - 08/2019
# 09/2018 - present
# Sep 2018 - present
# September 2018 - present
# Sep 2018 - Aug 2019
# Sep, 2018 - Aug, 2019
# Sep, 2018 - present
# September, 2018 - present
# September, 2018 - August, 2019
# December 2019 - March 2021
# September 2018 - August 2019
# December 2018 - present
# """
# matches = extractDateRanges(input_text)
# standardMatches = [replace_present(match) for match in matches]
# print(standardMatches)