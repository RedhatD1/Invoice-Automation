from datetime import datetime

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
        return round(fraction_of_year, 2)  # Round the result to two decimal places
    except ValueError:
        # If the input date_string is in an invalid format, handle the error as needed
        return 0

# Example usage:
date_string = "December 2021"
result = convert_to_fraction_of_year(date_string)
print(result)  # Output: 0.66
