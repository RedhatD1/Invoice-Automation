from backend.cv_extraction.helpers import pdfToInfo

def getJSON(pdfFileName, jobDescriptionFileName):
    pdfFile = 'backend/cv_extraction/cv/' + pdfFileName
    jobDescriptionFile = "backend/cv_extraction/jobDescriptions/" + jobDescriptionFileName
    output = pdfToInfo.extractInfo(pdfFile, jobDescriptionFile)
    return output

# Example Usage
# pdfFileName = 'anirudh.pdf'
# jobDescriptionFileName = "webDeveloper.txt"
# output = getJSON(pdfFileName, jobDescriptionFileName)
#
# for key, value in output.items():
#     print(f'{key}: {value}')