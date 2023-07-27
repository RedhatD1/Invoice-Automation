from backend.cv_extraction.helpers import pdfToInfo


def getJSON(pdfFileName, jobDescription, algorithm='default'):
    pdfFilePath = f"documents/cv/{pdfFileName}"
    response = pdfToInfo.extractInfo(pdfFilePath, jobDescription)
    return response