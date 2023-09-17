import math
from typing import Dict

from extraction_algorithms.cv.helpers import pdfReader, htmlParser, \
    parsedHtmlToSectionedDocument, candidateInfoExtractor, sectionExtractor, \
    sectionToDict, cvScoring, educationInfoExtractor, experienceExtractor


def extract_info(pdf_file_path: str, job_description: str) -> Dict:
    # Font size is dynamically adjusted based on CV, no specific font size is targeted
    html = pdfReader.read_as_html(pdf_file_path)
    parsed_html = htmlParser.parse(html) # List of text:fontsize pairs
    sectioned_document = parsedHtmlToSectionedDocument.convert(parsed_html, html)

    cv_text_only = pdfReader.read_as_text(pdf_file_path) # Text only (non html)
    applicant_name, applicant_phone, applicant_email = \
        candidateInfoExtractor.get_candidate_info(sectioned_document,
                                                  cv_text_only, pdf_file_path)
    # Extraction logic for applicant name, phone, email based on html version font size+plain text
    sections = sectionExtractor.extract_sections(sectioned_document, parsed_html)
    # Extract all sections from the cv based on font size
    # This is different from applicant name extraction because target font size is different
    info_dict = sectionToDict.extract(sections)
    # From the extracted sections, extract the text for each section
    score = cvScoring.generate_match_score(info_dict['experience'] + info_dict['skills'] +
                                           info_dict['projects'] + info_dict['course'] +
                                           info_dict['summary'], job_description)
    # Calls the ML algorithm to generate a score based on the job description
    education = educationInfoExtractor.get(info_dict['education'])
    experience = experienceExtractor.extract_years_experience(info_dict['experience'])
    # Both of these are based on ReGeX
    mul = 0
    if experience > 10:
        mul = 10
    else:
        mul = experience
    # adjust to increase weight of experience
    score = score*(mul/25) + score*0.60
    # Score will be at max 100
    # A good candidate will have a score of 25+
    # A very good candidate will have a score of 40+
    # A perfect candidate will have a score of 50+
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
    # Json Response
