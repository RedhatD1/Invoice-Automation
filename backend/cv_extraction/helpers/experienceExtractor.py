import re
def extractDateRanges(input_text):
    date_range_pattern = r"\d{2}/\d{4}\s*-\s*(?:present|\d{2}/\d{4})"
    month_year_pattern = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b\s*(?:\d{4})?\s*-\s*present"

    combined_pattern = rf"{date_range_pattern}|{month_year_pattern}"

    matches = re.findall(combined_pattern, input_text, re.IGNORECASE)
    return matches

#
# input_text = """
# 09/2018 - 08/2019
# 09/2018 - present
# Sep 2018 - present
# September 2018 - present
# Sep 2018 - Aug 2019
# Sep, 2018 - Aug, 2019
# Sep, 2018 - present
# September, 2018 - present
# September 2018 - present
# September, 2018 - August, 2019
# September 2018 - August 2019
# """
# matches = extractDateRanges(input_text)
# print(matches)