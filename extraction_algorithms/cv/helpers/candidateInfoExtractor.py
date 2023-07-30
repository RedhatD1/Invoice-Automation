import os

"""
A candidate name can get captured as a paragraph if the font size is 
not much different from nearby text. This can also happen if the paragraphs are very
close in the document. In order to clip only the name, we need to check for the
first occurrence of name because usually a name is the title or a one line text
"""
def clip_string(input_string):
    # Find the index of the first occurrence of "\n"
    newline_index = input_string.find("\n")

    # If "\n" is found, take the substring from the start to the first "\n"
    if newline_index != -1:
        clipped_string = input_string[:newline_index]
    else:
        # If no "\n" is found, take the whole string
        clipped_string = input_string

    return clipped_string

"""
This is a backup method in case we couldnt detect the name from the PDF
The logic is that most people will have their name in the file name
So we can extract the name from the file name
"""
def getFileName(pdfFilePath):
    file_name = os.path.basename(pdfFilePath)
    return file_name

def getName(sectionedDocument, pdfFilePath):
    applicant_name = ''

    if sectionedDocument:
        largest_headings = sorted(sectionedDocument, key=lambda x: x.metadata['heading_font'], reverse=True)
        largest_heading_font = largest_headings[0].metadata['heading_font']
        largest_headings = [heading for heading in largest_headings if
                            heading.metadata['heading_font'] == largest_heading_font]

        # print("Largest Headings: ")
        # for heading in largest_headings:
        #     print(heading.metadata['heading'])
        applicant_name = largest_headings[0].metadata['heading']
    else:
        # print("No headings found.")
        applicant_name = getFileName(pdfFilePath)

    # print(f'Applicant Name: {applicant_name}')
    applicant_name = applicant_name.lstrip("\n")
    applicant_name = clip_string(applicant_name)
    return applicant_name.strip()

import re
def getEmail(cvText):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    match = re.search(email_regex, cvText)
    if match:
        return match.group()
    else:
        return ''
def getPhone(cvText):
    phone_regex = r"(?:(?:\+|00)88|01)?\d{11}"
    match = re.search(phone_regex, cvText)
    if match:
        return match.group()
    else:
        return ''


def getcandidateinfo(sectionedDocument, cvText, pdfFilePath):
    applicantName = getName(sectionedDocument, pdfFilePath)
    applicantEmail = getEmail(cvText)
    applicantPhone = getPhone(cvText)
    return applicantName, applicantPhone, applicantEmail