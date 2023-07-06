import os
from pdf2image import convert_from_path

def pdf_to_jpg(input_pdf_path, output_jpg_path):
    images = convert_from_path(input_pdf_path, poppler_path=r'C:/Program Files/poppler-23.05.0/Library/bin')
    filename = os.path.splitext(os.path.basename(input_pdf_path))[0]

    for i, image in enumerate(images):
        jpg_path = os.path.join(output_jpg_path, f'{filename}_page_{i+1}.jpg')
        image.save(jpg_path, 'JPEG')


def convert_pdfs_in_directory(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of all PDF files in the input directory
    pdf_files = [file for file in os.listdir(input_dir) if file.lower().endswith('.pdf')]

    # Process each PDF file
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)

        pdf_to_jpg(pdf_path, output_dir)


def main():

    input_directory = 'E:\Reddot\invoice_extraction\invoices'
    output_directory = 'E:\Reddot\invoice_extraction\invoices_img'
    convert_pdfs_in_directory(input_directory, output_directory)


if __name__=="__main__":
    main()