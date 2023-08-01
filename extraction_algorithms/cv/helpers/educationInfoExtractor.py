import re

"""
To detect the university we are using a UGC approved university list.
We are using a list of majors to detect the major.
We are using a regex to detect the cgpa.
"""


def detect_university(education_text: str) -> list:
    education_text = \
        " ".join(education_text.replace(',', ' ').replace('.', ' ').replace('-', ' ').split())

    # Reading the institution names from the txt file and storing them in a list
    with open('extraction_algorithms/cv/helpers/ugcList.txt', 'r') as file:
        universities_list = [line.strip() for line in file]

    # Initialize an empty list to store matched universities and their indices
    matches = []

    # Check each institution name in the list and see if it's fully present in the text
    for institution in universities_list:
        # Search for the institution as a full word in the lowercase cvText
        start_index = 0
        while True:
            match_index = education_text.find(f" {institution} ", start_index)
            if match_index == -1:
                break
            match_info = {
                "institution": institution,
                "startIndex": match_index
            }
            matches.append(match_info)
            start_index = match_index + 1
    # Storing the start index helps us to segment different institutions
    # This way we can detect the major and cgpa for each institution
    return matches


def detect_major(education_text: str) -> str:
    # Read the institution names from the txt file and store them in a list
    with open('extraction_algorithms/cv/helpers/majorList.txt', 'r') as file:
        major_list = [line.strip() for line in file]

        # Check each major in the list and see if it's present in the text
        for major in major_list:
            if major in education_text:
                return major
        return ""  # Return empty string if no match is found


def detect_cgpa(education_text: str) -> float:
    # extract cgpa from the text
    pattern = r'\b\d\.\d{2}\b'
    cgpa = re.findall(pattern, education_text)
    if len(cgpa) > 0 and float(cgpa[0]) < 4.00:
        return cgpa[0]
    else:
        return 0.00


def detect_between_matches(detected_universities: list, education_text: str) -> list:
    for i, university in enumerate(detected_universities):
        start_index = university["startIndex"]
        end_index = detected_universities[i + 1]["startIndex"] if i < len(detected_universities) - 1 else len(
            education_text)
        university_context = education_text[start_index:end_index].replace(',', ' ').strip()
        university_context = " ".join(university_context.split())
        university["cgpa"] = detect_cgpa(university_context)
        university["department"] = detect_major(university_context)

    return detected_universities


def get(education_text: str) -> list:
    education_text = education_text.lower().replace('&', 'and')
    # Some university writes 'and' and others use '&' in the name
    # So we are replacing '&' with 'and' to make it generic,
    # We are also converting the text to lowercase to make it case-insensitive
    detected_universities = detect_university(education_text)
    detected_universities = detect_between_matches(detected_universities, education_text)
    return detected_universities
