from backend.cv_extraction.helpers import pdfToHtml, htmlParser, \
    parsedHtmlToSectionedDocument, applicantNameExtractor, sectionExtractor
pdfFile = '/Users/tariq/Documents/Reddot/Invoice Automation/cv/cv.pdf'
html = pdfToHtml.read(pdfFile)
parsedHtml = htmlParser.parse(html)
sectionedDocument = parsedHtmlToSectionedDocument.convert(parsedHtml, html)
name = applicantNameExtractor.getName(sectionedDocument, pdfFile)
print(f'Name: {name}')
sections = sectionExtractor.extract_sections(sectionedDocument, parsedHtml)
print(f'Sections:\n {sections}')