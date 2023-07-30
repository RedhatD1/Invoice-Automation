import re


def detect_university(cv_text):
    cv_text = " ".join(cv_text.replace('&', 'and').replace(',', ' ').replace('.', ' ').replace('-', ' ').split())
    cv_text = cv_text.lower()

    # Read the institution names from the txt file and store them in a list
    with open('extraction_algorithms/cv/helpers/ugcList.txt', 'r') as file:
        universities_list = [line.strip() for line in file]

    # Initialize an empty list to store matched universities and their indices
    matches = []

    # Check each institution name in the list and see if it's fully present in the text
    for institution in universities_list:
        # Search for the institution as a full word in the lowercase cvText
        start_index = 0
        while True:
            match_index = cv_text.find(f" {institution.lower()} ", start_index)
            if match_index == -1:
                break
            match_info = {
                "institution": institution,
                "startIndex": match_index
            }
            matches.append(match_info)
            start_index = match_index + 1

    return matches


def detect_major(cv_text):
    # Read the institution names from the txt file and store them in a list
    with open('extraction_algorithms/cv/helpers/majorList.txt', 'r') as file:
        major_list = [line.strip() for line in file]

        # Convert major_list to lowercase
        lowercased_major_list = [department.lower() for department in major_list]

        # Convert cv_text to lowercase for case-insensitive matching
        cv_text_lower = cv_text.lower()

        # Check each major in the list and see if it's present in the text
        for major in lowercased_major_list:

            if major in cv_text_lower:
                return major
        return ""  # Return empty string if no match is found


def detect_cgpa(cv_text):
    # extract cgpa from the text
    pattern = r'\b\d\.\d{2}\b'
    cgpa = re.findall(pattern, cv_text)
    if len(cgpa) > 0 and float(cgpa[0]) < 4.00:
        return cgpa[0]
    else:
        return 0.00


def detect_between_matches(detected_universities, cv_text):
    if len(detected_universities) > 1:
        for i in range(len(detected_universities) - 1):
            start_index = detected_universities[i]["startIndex"]
            end_index = detected_universities[i + 1]["startIndex"]
            university_context = cv_text[start_index:end_index].replace('&', 'and').replace(',', ' ').strip()
            university_context = " ".join(university_context.split())
            cgpa = detect_cgpa(university_context)
            detected_universities[i]["cgpa"] = cgpa
            # print(f'University context: {startIndex} to {endIndex} : {universityContext}')
            department = detect_major(university_context)
            detected_universities[i]["department"] = department

        university_context = cv_text[detected_universities[-1]["startIndex"]:].replace('&', 'and').replace(',',
                                                                                                        ' ').strip()
        university_context = " ".join(university_context.split())
        cgpa = detect_cgpa(university_context)
        detected_universities[-1]["cgpa"] = cgpa
        department = detect_major(university_context)
        detected_universities[-1]["department"] = department
    elif len(detected_universities) == 1:
        university_context = cv_text[detected_universities[0]["startIndex"]:].replace('&', 'and').replace(',', ' ').strip()
        university_context = " ".join(university_context.split())
        cgpa = detect_cgpa(university_context)
        detected_universities[0]["cgpa"] = cgpa
        department = detect_major(university_context)
        detected_universities[0]["department"] = department
    return detected_universities


def get(cv_text):
    detected_universities = detect_university(cv_text)
    detected_universities = detect_between_matches(detected_universities, cv_text)
    return detected_universities


#  Example usage
#  Sample string to search for universities
# cvText = """
# BSC United International University (UIU) Computer Science
# [2017] – [Continue]
# Fall 2017 -
# CGPA: 2.23 ( On scale of 4.00) Trimester: 11th
# Year: 4th
# Bachelor of Business Administration United International University
# • 1st Major - Human Resources Management • 2nd Major - Marketing
# • CGPA-3.50
# •
# From December 2017 to December 2022
# """
# # Detect universities in the sample string
# education = get(cvText)
# print(education)
