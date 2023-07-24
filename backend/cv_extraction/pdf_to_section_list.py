from langchain.document_loaders import PDFMinerPDFasHTMLLoader


def pdf_to_html(pdf_file):
    # Using PDFminer, we are extracting the PDF as a HTML file
    # This process retains the necessary formatting info of the original PDF
    # Now we can use features like checking font size, style etc
    loader = PDFMinerPDFasHTMLLoader(pdf_file)

    # loader expects multiple PDF, since we are using 1 pdf, we want the first item of the list.
    # The first item is stored at the 0th index
    data = loader.load()[0]
    return data


import re
from bs4 import BeautifulSoup


def html_parser(data):
    # We are using bs4 for parsing our extracted html file
    soup = BeautifulSoup(data.page_content,'html.parser')
    # all elements are inside a div, so we are finding all the divs first and those divs contain
    # the information about the CV (title, subsections etc. all text)
    # other parts like <html><title> etc. are discarded in this way

    total_content = soup.find_all('div')
    current_font_size = None

    # current_text contains the text written inside our currently processing tag
    current_text = ''

    # for collecting all snippets that have the same font size
    snippets = []
    for content in total_content:
        span_tag = content.find('span')
        # Attempts to find the <span> element within the current content object.
        # It appears to look for specific HTML elements with the tag

        if not span_tag:
            continue
            # if no <span> element is found within the current content object,
            # the code moves to the next iteration, skipping the rest of the loop for this content.

        style_tag = span_tag.get('style')
        # Retrieves the 'style' attribute from the found <span> element, if it exists
        if not style_tag:
            continue
        # If the 'style' attribute is not found in the <span> element,
        # the code moves to the next iteration, skipping the rest of the loop for this content.

        font_attribute = re.findall('font-size:(\d+)px', style_tag)
        # It looks for a pattern in the style_tag
        # matching 'font-size:' followed by digits (\d+) and 'px' (indicating pixels)
        if not font_attribute:
            continue
            # If the font size information is not found in the 'style' attribute,
            # the code moves to the next iteration, skipping the rest of the loop for this content.

        font_attribute = int(font_attribute[0])
        # Converts the first match (font size) found by the regular expression
        # search into an integer and stores it in the variable

        if not current_font_size:
            # It's the first time encountering a font size in the content.
            current_font_size = font_attribute

        if font_attribute == current_font_size:
            # This means it's part of the same text snippet of the font size
            current_text += content.text
        else:
            # it means a new text snippet is starting. So, it appends the current text snippet
            # (cur_text) and its corresponding font size (cur_fs) as a tuple to the snippets list.
            snippets.append((current_text, current_font_size))

            current_font_size = font_attribute
            current_text = content.text
            # Initializing the new snippet

    snippets.append((current_text, current_font_size))
    # For the last snippet, since we wont see any change in snippet font size,
    # Our previous appending wont trigger because of this.
    return snippets
