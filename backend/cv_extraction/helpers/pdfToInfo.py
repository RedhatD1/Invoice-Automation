from backend.cv_extraction.helpers import pdfReader, htmlParser, \
    parsedHtmlToSectionedDocument, candidateInfoExtractor, sectionExtractor, \
    sectionToDict, cvScoring, educationInfoExtractor

def extractInfo(pdfFilePath, jobDescription):
    html = pdfReader.readAsHTML(pdfFilePath)
    parsedHtml = htmlParser.parse(html)
    sectionedDocument = parsedHtmlToSectionedDocument.convert(parsedHtml, html)
    cvTextOnly = pdfReader.readAsText(pdfFilePath)
    # print(f'{cvTextOnly}')
    applicantName, applicantPhone, applicantEmail = candidateInfoExtractor.getcandidateinfo(sectionedDocument, cvTextOnly, pdfFilePath)
    sections = sectionExtractor.extract_sections(sectionedDocument, parsedHtml)

    dict = sectionToDict.extract(sections)

    # Uncomment to see which values are being extracted properly
    # for key, value in dict.items():
    #     print(f'{key}: {value}')
    score = cvScoring.generate_match_score(dict['experience'] + dict['skills'] +
                                           dict['projects'] + dict['course'], jobDescription)
    education = educationInfoExtractor.get(dict['education'])
    return {
        "candidate_info": {
            "name": applicantName,
            "phone": applicantPhone,
            "email": applicantEmail,
            "present_address": "",
            "permanent_address": ""
        },
        "education_info": education,
        "experience": 0.0,
        "score": score,
        "rank": "--"
    }
