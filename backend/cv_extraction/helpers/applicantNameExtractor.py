import os

def getFileName(directory_path):
    file_name = os.path.basename(directory_path)
    return file_name

def getName(semantic_snippets, pdf_file):
    applicant_name = ''

    if semantic_snippets:
        largest_headings = sorted(semantic_snippets, key=lambda x: x.metadata['heading_font'], reverse=True)
        largest_heading_font = largest_headings[0].metadata['heading_font']
        largest_headings = [heading for heading in largest_headings if
                            heading.metadata['heading_font'] == largest_heading_font]

        # print("Largest Headings: ")
        # for heading in largest_headings:
        #     print(heading.metadata['heading'])
        applicant_name = largest_headings[0].metadata['heading']
    else:
        # print("No headings found.")
        applicant_name = getFileName(pdf_file)

    # print(f'Applicant Name: {applicant_name}')
    return applicant_name
