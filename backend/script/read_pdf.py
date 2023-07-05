import PyPDF2

def read_pdf(file_path):
    # Open the PDF file in binary mode
    with open(file=file_path, mode='rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)
        text_content = ""

        # Iterate over each page and extract the text
        for page in reader.pages:
            text = page.extract_text()
            text_content+=text

    return text_content

# # Usage
# text = read_pdf('invoices/3.pdf')
# print(text)