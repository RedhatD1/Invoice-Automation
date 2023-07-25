from langchain.document_loaders import PDFMinerPDFasHTMLLoader


def read(pdf_file):
    # Using PDFminer, we are extracting the PDF as a HTML file
    # This process retains the necessary formatting info of the original PDF
    # Now we can use features like checking font size, style etc
    loader = PDFMinerPDFasHTMLLoader(pdf_file)

    # loader expects multiple PDF; since we are using 1 pdf, we want the first item of the list.
    # The first item is stored at the 0th index
    data = loader.load()[0]
    return data
