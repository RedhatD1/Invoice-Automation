import math
from typing import Dict

from extraction_algorithms.cv.helpers import pdfReader, htmlParser, \
    parsedHtmlToSectionedDocument, candidateInfoExtractor, sectionExtractor, \
    sectionToDict, cvScoring, educationInfoExtractor, experienceExtractor


def extract_info(pdf_file_path: str, job_description: str) -> Dict:
    html = pdfReader.read_as_html(pdf_file_path)
    parsed_html = htmlParser.parse(html)
    sectioned_document = parsedHtmlToSectionedDocument.convert(parsed_html, html)

    cv_text_only = pdfReader.read_as_text(pdf_file_path)
    applicant_name, applicant_phone, applicant_email = \
        candidateInfoExtractor.get_candidate_info(sectioned_document,
                                                  cv_text_only, pdf_file_path)

    sections = sectionExtractor.extract_sections(sectioned_document, parsed_html)
    info_dict = sectionToDict.extract(sections)

    score = cvScoring.generate_match_score(info_dict['experience'] + info_dict['skills'] +
                                           info_dict['projects'] + info_dict['course'] +
                                           info_dict['summary'], job_description)

    education = educationInfoExtractor.get(info_dict['education'])
    experience = experienceExtractor.extract_years_experience(info_dict['experience'])

    # adjust to increase weight of experience
    score = score*(experience/25) + score*0.95

    # adjust to increase penalty for no experience
    if experience == 0:
        score = score / 1.5

    # Clipping result to 100% max
    if score > 100.0:
        score = 100.0

    score = round(score, 2)

    return {
        "candidate_info": {
            "name": applicant_name,
            "phone": applicant_phone,
            "email": applicant_email,
            "present_address": "",
            "permanent_address": ""
        },
        "education_info": education,
        "experience": experience,
        "score": score,
        "rank": "--"
    }
