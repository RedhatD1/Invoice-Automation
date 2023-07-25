import os

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