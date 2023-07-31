import os
import re

"""
This module extracts the name, email and phone number of a candidate from a CV
"""

"""
Function: def clip_string(input_string):

A candidate name can get captured as a paragraph if the font size is 
not much different from nearby text. This can also happen if the paragraphs are very
close in the document. In order to clip only the name, we need to check for the
first occurrence of name because usually a name is the title or a one line text
"""


def clip_string(input_string):
    # Find the index from the first occurrence of "\n"
    newline_index = input_string.find("\n")

    # If "\n" is found, take the substring from the start to the first "\n"
    if newline_index != -1:
        clipped_string = input_string[:newline_index]
    else:
        # If no "\n" is found, take the whole string
        clipped_string = input_string

    return clipped_string


"""
Function: def get_file_name(pdf_file_path):

This is a backup method in case we couldn't detect the name from the PDF
The logic is that most people will have their name in the file name
So we can extract the name from the file name
"""


def get_file_name(pdf_file_path):
    file_name = os.path.basename(pdf_file_path)
    if file_name is None:
        file_name = ""
    return file_name


def get_name(sectioned_document, pdf_file_path):
    if sectioned_document:
        sorted_headings = sorted(sectioned_document, key=lambda x: x.metadata['heading_font'], reverse=True)
        largest_heading_font = sorted_headings[0].metadata['heading_font']
        largest_headings = [heading for heading in sorted_headings if
                            heading.metadata['heading_font'] == largest_heading_font]
        applicant_name = largest_headings[0].metadata['heading']  # Font will usually be the largest text in CV
    else:
        applicant_name = get_file_name(pdf_file_path)

    if applicant_name is None:
        applicant_name = ""
    applicant_name = applicant_name.lstrip("\n")
    applicant_name = clip_string(applicant_name)
    return applicant_name.strip()


def get_email(cv_text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    match = re.search(email_regex, cv_text)
    if match:
        return match.group()
    else:
        return ''


def get_phone(cv_text):
    phone_regex = r"(?:(?:\+|00)88|01)?\d{11}"
    match = re.search(phone_regex, cv_text)
    if match:
        return match.group()
    else:
        return ''


"""
Parsing all the extracted text from the CV
"""


def get_candidate_info(sectioned_document: list, cv_text: str, pdf_file_path: str):
    applicant_name = get_name(sectioned_document, pdf_file_path)
    applicant_email = get_email(cv_text)
    applicant_phone = get_phone(cv_text)
    return applicant_name, applicant_phone, applicant_email
