from PyPDF2 import PdfFileReader
from wand.image import Image

def pdf_to_jpg(input_pdf_path, output_jpg_path):
    with open(input_pdf_path, 'rb') as pdf_file:
        pdf = PdfFileReader(pdf_file)
        num_pages = pdf.numPages

        with Image() as img:
            for page_num in range(num_pages):
                pdf_page = pdf.getPage(page_num)
                img.from_bytes(pdf_page.extractImages()[0][7]['/Filter'][1]).save(filename=output_jpg_path.format(page_num))

import os

def convert_pdfs_in_directory(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of all PDF files in the input directory
    pdf_files = [file for file in os.listdir(input_dir) if file.lower().endswith('.pdf')]

    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        jpg_file = os.path.splitext(pdf_file)[0] + '.jpg'
        jpg_path = os.path.join(output_dir, jpg_file)

        # Call the pdf_to_jpg function to convert the current PDF to JPG
        pdf_to_jpg(pdf_path, jpg_path)



def main():

    input_directory = 'E:\Reddot\invoice_extraction\invoices'
    output_directory = 'E:\Reddot\invoice_extraction\invoices_img'
    convert_pdfs_in_directory(input_directory, output_directory)


if __name__=="__main__":
    main()