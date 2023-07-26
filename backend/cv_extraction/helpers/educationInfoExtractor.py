import re


def detect_university(cvText):
    # Read the university names from the txt file and store them in a list
    with open('backend/cv_extraction/helpers/ugcList.txt', 'r') as file:
        universities_list = [line.strip() for line in file]

    # Initialize an empty list to store matched universities and their indices
    matches = []

    # Check each university name in the list and see if it's present in the text
    for university in universities_list:
        regex_pattern = re.compile(re.escape(university), re.IGNORECASE)
        for match in re.finditer(regex_pattern, cvText):
            match_info = {
                "university": university,
                "startIndex": match.start(),
                "endIndex": match.end()
            }
            matches.append(match_info)

    return matches


def detect_cgpa(cvText):
    # extract cgpa from the text
    print(f'Checking for: {cvText}')
    pattern = r'\b\d\.\d{2}\b'
    cgpa = re.findall(pattern, cvText)
    if len(cgpa) > 0:
        print(f'Found: {cgpa[0]}')
        return cgpa[0]
    else:
        print(f'Found: 0.00')
        return 0.00


def detect_cgpa_between_matches(detectedUniversities, cvText):
    if len(detectedUniversities) > 1:
        for i in range(len(detectedUniversities) - 1):
            startIndex = detectedUniversities[i]["endIndex"]
            endIndex = detectedUniversities[i + 1]["startIndex"]
            cgpa = detect_cgpa(cvText[startIndex:endIndex])
            detectedUniversities[i]["cgpa"] = cgpa
        cgpa = detect_cgpa(cvText[detectedUniversities[-1]["endIndex"]:])
        detectedUniversities[-1]["cgpa"] = cgpa
    elif len(detectedUniversities) == 1:
        cgpa = detect_cgpa(cvText[detectedUniversities[0]["endIndex"]:])
        detectedUniversities[0]["cgpa"] = cgpa
    return detectedUniversities

#  Example usage
#  Sample string to search for universities
cvText = "I studied at University of Dhaka University with CGPA 3.68 and later pursued my PhD at the University of " \
         "Rajshahi with 3.78 ."
#  Detect universities in the sample string
detected_universities = detect_university(cvText)
detected_universities = detect_cgpa_between_matches(detected_universities, cvText)
print("Detected universities:")
print(detected_universities)
