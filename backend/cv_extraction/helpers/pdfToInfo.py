from backend.cv_extraction.helpers import pdfToHtml, htmlParser, \
    parsedHtmlToSectionedDocument, applicantNameExtractor, sectionExtractor, \
    sectionToDict, cvScoring

def extractInfo(pdfFile, jobDescriptionFile):
    html = pdfToHtml.read(pdfFile)
    parsedHtml = htmlParser.parse(html)
    sectionedDocument = parsedHtmlToSectionedDocument.convert(parsedHtml, html)
    name = applicantNameExtractor.getName(sectionedDocument, pdfFile)
    print(f'Name: {name}')
    sections = sectionExtractor.extract_sections(sectionedDocument, parsedHtml)

    dict = sectionToDict.extract(sections)

    # Uncomment to see which values are being extracted properly
    # for key, value in dict.items():
    #     print(f'{key}: {value}')

    # Open the file in read mode
    with open(jobDescriptionFile, "r") as file:
        # Read the entire content of the file
        jd = file.read()

    # Display the content of the file
    # print(jd)

    score = cvScoring.generate_match_score(dict['experience'] + dict['skills'] +
                                           dict['projects'] + dict['course'], jd)

    return {
        "candidate_info": {
            "name": name,
            "phone": "",
            "email": "",
            "present_address": "",
            "permanent_address": ""
        },
        "education_info": {
                "institution": "",
                "department": "",
                "cgpa": 0.0
        },
        "experience": 0.0,
        "score": score,
        "rank": "--"
    }
