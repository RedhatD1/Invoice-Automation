import math

from extraction_algorithms.cv.helpers import pdfReader, htmlParser, \
    parsedHtmlToSectionedDocument, candidateInfoExtractor, sectionExtractor, \
    sectionToDict, cvScoring, educationInfoExtractor, experienceExtractor

def extractInfo(pdfFilePath, jobDescription):
    html = pdfReader.readAsHTML(pdfFilePath)
    parsedHtml = htmlParser.parse(html)
    sectionedDocument = parsedHtmlToSectionedDocument.convert(parsedHtml, html)
    cvTextOnly = pdfReader.readAsText(pdfFilePath)
    # print(f'{cvTextOnly}')
    applicantName, applicantPhone, applicantEmail = candidateInfoExtractor.getcandidateinfo(sectionedDocument, cvTextOnly, pdfFilePath)
    sections = sectionExtractor.extract_sections(sectionedDocument, parsedHtml)

    dict = sectionToDict.extract(sections)

    # # Uncomment to see which values are being extracted properly
    # for key, value in dict.items():
    #     print(f'{key}: {value}')
    score = cvScoring.generate_match_score(dict['experience'] + dict['skills'] +
                                           dict['projects'] + dict['course'] +
                                           dict['summary'], jobDescription)

    education = educationInfoExtractor.get(dict['education'])
    experience = experienceExtractor.extractDateRanges(dict['experience'])
    score = math.sqrt(score * experience) + score
    if score > 100.0:
        score = 100.0

    return {
        "candidate_info": {
            "name": applicantName,
            "phone": applicantPhone,
            "email": applicantEmail,
            "present_address": "",
            "permanent_address": ""
        },
        "education_info": education,
        "experience": experience,
        "score": score,
        "rank": "--"
    }
