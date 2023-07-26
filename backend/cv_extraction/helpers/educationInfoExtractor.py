import re

def detect_university(cvText):
    cvText = " ".join(cvText.replace('&', 'and').replace(',', ' ').replace('.',' ').split())
    cvText = cvText.lower()
    # Read the institution names from the txt file and store them in a list
    with open('backend/cv_extraction/helpers/ugcList.txt', 'r') as file:
        universities_list = [line.strip() for line in file]

    # Initialize an empty list to store matched universities and their indices
    matches = []

    # Check each institution name in the list and see if it's partially present in the text
    for institution in universities_list:
        # Create a regex pattern to allow partial matches within the institution names
        regex_pattern = re.compile(rf'(?i)\b.*{re.escape(institution)}.*\b')
        for match in re.finditer(regex_pattern, cvText):
            match_info = {
                "institution": institution,
                "startIndex": match.start()
            }
            matches.append(match_info)

    return matches


def detectMajor(cvText):
    print("detecting major")
    print(cvText)
    # Read the institution names from the txt file and store them in a list
    with open('backend/cv_extraction/helpers/majorList.txt', 'r') as file:
        major_list = [line.strip() for line in file]

        # Convert major_list to lowercase
        lowercased_major_list = [department.lower() for department in major_list]

        # Convert cv_text to lowercase for case-insensitive matching
        cv_text_lower = cvText.lower()

        # Check each major in the list and see if it's present in the text
        for major in lowercased_major_list:

            if major in cv_text_lower:
                print(major)
                return major
        return ""  # Return empty string if no match is found


def detect_cgpa(cvText):
    # extract cgpa from the text
    pattern = r'\b\d\.\d{2}\b'
    cgpa = re.findall(pattern, cvText)
    if len(cgpa) > 0 and float(cgpa[0])<4.00:
        return cgpa[0]
    else:
        return 0.00


def detect_between_matches(detectedUniversities, cvText):

    if len(detectedUniversities) > 1:
        for i in range(len(detectedUniversities) - 1):
            startIndex = detectedUniversities[i]["startIndex"]
            endIndex = detectedUniversities[i + 1]["startIndex"]
            universityContext = cvText[startIndex:endIndex].replace('&', 'and').replace(',', ' ').strip()
            universityContext = " ".join(universityContext.split())
            cgpa = detect_cgpa(universityContext)
            detectedUniversities[i]["cgpa"] = cgpa
            print(f'University context: {startIndex} to {endIndex} : {universityContext}')
            department = detectMajor(universityContext)
            detectedUniversities[i]["department"] = department

        universityContext = cvText[detectedUniversities[-1]["startIndex"]:].replace('&', 'and').replace(',', ' ').strip()
        universityContext = " ".join(universityContext.split())
        cgpa = detect_cgpa(universityContext)
        detectedUniversities[-1]["cgpa"] = cgpa
        department = detectMajor(universityContext)
        detectedUniversities[-1]["department"] = department
    elif len(detectedUniversities) == 1:
        universityContext = cvText[detectedUniversities[0]["startIndex"]:].replace('&', 'and').replace(',', ' ').strip()
        universityContext = " ".join(universityContext.split())
        cgpa = detect_cgpa(universityContext)
        detectedUniversities[0]["cgpa"] = cgpa
        department = detectMajor(universityContext)
        detectedUniversities[0]["department"] = department
    return detectedUniversities

def get(cvText):
    detected_universities = detect_university(cvText)
    detected_universities = detect_between_matches(detected_universities, cvText)
    return detected_universities

#  Example usage
#  Sample string to search for universities
cvText = """
EDUCATION
Bachelor of Business Administration (BBA) (Undergraduate)
Institution: Independent University , Bangladesh. Department: Human Resources Management Higher Secondary Certificate (H.S.C.) Institution: Adamjee Cantonment College , Dhaka Group: Business Studies (4.25 out of 5.00)
Passing Year: 2017
EDUCATION
Bachelor of Business Administration (BBA) (Undergraduate)
Institution: Dhaka University , Bangladesh. Department: Human Resources Management Higher Secondary Certificate (H.S.C.) Institution: Adamjee Cantonment College , Dhaka Group: Business Studies (4.25 out of 5.00)
Passing Year: 2017"""
#  Detect universities in the sample string
education = get(cvText)
print("Detected education:")
print(education)

