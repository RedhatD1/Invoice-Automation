import re

def detect_university(cvText):
    cvText = " ".join(cvText.replace('&', 'and').replace(',', ' ').replace('.',' ').split())
    cvText = cvText.lower()
    # Read the university names from the txt file and store them in a list
    with open('backend/cv_extraction/helpers/ugcList.txt', 'r') as file:
        universities_list = [line.strip() for line in file]

    # Initialize an empty list to store matched universities and their indices
    matches = []

    # Check each university name in the list and see if it's partially present in the text
    for university in universities_list:
        # Create a regex pattern to allow partial matches within the university names
        regex_pattern = re.compile(rf'(?i)\b.*{re.escape(university)}.*\b')
        for match in re.finditer(regex_pattern, cvText):
            match_info = {
                "university": university,
                "startIndex": match.start()
            }
            matches.append(match_info)

    return matches


def detectMajor(cvText):
    # Read the university names from the txt file and store them in a list
    with open('backend/cv_extraction/helpers/majorList.txt', 'r') as file:
        major_list = [line.strip() for line in file]

        # Convert major_list to lowercase
        lowercased_major_list = [major.lower() for major in major_list]

        # Convert cv_text to lowercase for case-insensitive matching
        cv_text_lower = cvText.lower()

        # Create a regex pattern to match each major in the lowercased_major_list
        regex_pattern = re.compile(rf'(?i)\b(?:{"|".join(map(re.escape, lowercased_major_list))})\b')

        # Find the first major that matches the regex pattern
        match = regex_pattern.search(cv_text_lower)
        if match:
            return match.group()

        return ""  # Return empty string if no match is found


def detect_cgpa(cvText):
    # extract cgpa from the text
    pattern = r'\b\d\.\d{2}\b'
    cgpa = re.findall(pattern, cvText)
    if len(cgpa) > 0 and float(cgpa[0])<4.00:
        return cgpa[0]
    else:
        return 0.00


def detect_cgpa_between_matches(detectedUniversities, cvText):

    if len(detectedUniversities) > 1:
        for i in range(len(detectedUniversities) - 1):
            startIndex = detectedUniversities[i]["startIndex"]
            endIndex = detectedUniversities[i + 1]["startIndex"]
            universityContext = cvText[startIndex:endIndex].replace('&', 'and').replace(',', ' ').strip()
            universityContext = " ".join(universityContext.split())
            cgpa = detect_cgpa(universityContext)
            detectedUniversities[i]["cgpa"] = cgpa
            major = detectMajor(universityContext)
            detectedUniversities[i]["major"] = major

        universityContext = cvText[detectedUniversities[-1]["endIndex"]:].replace('&', 'and').replace(',', ' ').strip()
        universityContext = " ".join(universityContext.split())
        cgpa = detect_cgpa(universityContext)
        detectedUniversities[-1]["cgpa"] = cgpa
        major = detectMajor(universityContext)
        detectedUniversities[-1]["major"] = major
    elif len(detectedUniversities) == 1:
        universityContext = cvText[detectedUniversities[0]["startIndex"]:].replace('&', 'and').replace(',', ' ').strip()
        universityContext = " ".join(universityContext.split())
        cgpa = detect_cgpa(universityContext)
        detectedUniversities[0]["cgpa"] = cgpa
        major = detectMajor(universityContext)
        detectedUniversities[0]["major"] = major
    return detectedUniversities

#  Example usage
#  Sample string to search for universities
cvText = """
EDUCATION
Bachelor of Business Administration (BBA) (Undergraduate)
Institution: Independent University , Bangladesh. Department: Human Resources Management Higher Secondary Certificate (H.S.C.) Institution: Adamjee Cantonment College , Dhaka Group: Business Studies (4.25 out of 5.00)
Passing Year: 2017"""
#  Detect universities in the sample string
detected_universities = detect_university(cvText)
detected_universities = detect_cgpa_between_matches(detected_universities, cvText)
print("Detected universities:")
print(detected_universities)

