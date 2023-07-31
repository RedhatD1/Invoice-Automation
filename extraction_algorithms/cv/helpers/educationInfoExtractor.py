import re


def detect_university(education_text: str) -> list:
    education_text = " ".join(
        education_text.replace('&', 'and').replace(',', ' ').replace('.', ' ').replace('-', ' ').split())
    education_text = education_text.lower()

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
            match_index = education_text.find(f" {institution.lower()} ", start_index)
            if match_index == -1:
                break
            match_info = {
                "institution": institution,
                "startIndex": match_index
            }
            matches.append(match_info)
            start_index = match_index + 1

    return matches


def detect_major(education_text: str) -> str:
    # Read the institution names from the txt file and store them in a list
    with open('extraction_algorithms/cv/helpers/majorList.txt', 'r') as file:
        major_list = [line.strip() for line in file]

        # Convert major_list to lowercase
        lowercase_major_list = [department.lower() for department in major_list]

        # Convert cv_text to lowercase for case-insensitive matching
        cv_text_lower = education_text.lower()

        # Check each major in the list and see if it's present in the text
        for major in lowercase_major_list:

            if major in cv_text_lower:
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
    if len(detected_universities) > 1:
        for i in range(len(detected_universities) - 1):
            start_index = detected_universities[i]["startIndex"]
            end_index = detected_universities[i + 1]["startIndex"]
            university_context = education_text[start_index:end_index].replace('&', 'and').replace(',', ' ').strip()
            university_context = " ".join(university_context.split())
            cgpa = detect_cgpa(university_context)
            detected_universities[i]["cgpa"] = cgpa
            # print(f'University context: {startIndex} to {endIndex} : {universityContext}')
            department = detect_major(university_context)
            detected_universities[i]["department"] = department

        university_context = education_text[detected_universities[-1]["startIndex"]:].replace('&', 'and').replace(',',
                                                                                                                  ' ').strip()
        university_context = " ".join(university_context.split())
        cgpa = detect_cgpa(university_context)
        detected_universities[-1]["cgpa"] = cgpa
        department = detect_major(university_context)
        detected_universities[-1]["department"] = department
    elif len(detected_universities) == 1:
        university_context = education_text[detected_universities[0]["startIndex"]:].replace('&', 'and').replace(',',
                                                                                                                 ' ').strip()
        university_context = " ".join(university_context.split())
        cgpa = detect_cgpa(university_context)
        detected_universities[0]["cgpa"] = cgpa
        department = detect_major(university_context)
        detected_universities[0]["department"] = department
    return detected_universities


def get(education_text: str) -> list:
    detected_universities = detect_university(education_text)
    detected_universities = detect_between_matches(detected_universities, education_text)
    return detected_universities