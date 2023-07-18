from PIL import Image
import pytesseract as pt
from pdf2image import convert_from_path

def pdf2txt(pdf_file_path):
  images = convert_from_path(pdf_file_path,500)
  extracted_text = ''
  for image in images:
      text = pt.image_to_string(image)
      extracted_text += text
  return extracted_text

import spacy
import re
# Load spaCy model for English language
nlp = spacy.load("en_core_web_sm")

# Regular expression pattern for detecting names
name_pattern = re.compile(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)*$")

def detect_names(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    names = [token.text for token in doc if name_pattern.match(token.text)]
    detected_names = entities + names
    if detected_names:
        return detected_names[0]
    else:
        return 'no name'

def detect_company(text):
    doc = nlp(text)
    company_names = [entity.text for entity in doc.ents if entity.label_ == 'ORG']
    c_name = []
    for name in company_names:
        if(name.lower() != 'company'):
            c_name.append(name)
    if c_name:
        return c_name[0]
    else:
        return 'company'

def table(text):
    text = text.splitlines()
    text = [element.strip() for element in text if element.strip()]
    end = ['sub-total' , 'subtotal' , 'sub total' , 'total']
    p_name = ['description', 'name', 'items', 'item', 'quantity', 'unit price', 'amount', 'total']
    #lines = text.split('\n')
    max_matches = 0
    max_matches_line = None
    for line in text:
        matches = sum([1 for name in p_name if name.lower() in line.lower()])
        if matches > max_matches:
            max_matches = matches
            max_matches_line = line
    matches = re.findall('|'.join(p_name), max_matches_line.lower(), flags=re.IGNORECASE)
    #print(matches)
    updated_matches = []
    for element in matches:
        if element.lower() == 'unit price' or element.lower() == 'unitprice':
            updated_matches.append('unit_price')
        elif element.lower() == 'description' or element.lower() == 'descriptions' or element.lower() == 'name' or element.lower() == 'names':
            updated_matches.append('description')
        elif element.lower() == 'total' or element.lower() == 'totals' or element.lower() == 'price' or element.lower() == 'prices':
            updated_matches.append('price')
        elif element.lower() == 'quantity' or element.lower() == 'quantitys' or element.lower() == 'unit' or element.lower() == 'units':
            updated_matches.append('qty')
    updated_matches = [x for i, x in enumerate(updated_matches) if x not in updated_matches[:i]]
    return max_matches_line , updated_matches
    
def table_pattern(updated_matches):
    s = '\s*'
    for i in range(len(updated_matches)):
        if updated_matches[i] == 'description':
            s+= '(?P<' + 'description'+ '>.+)'
        elif updated_matches[i] == 'qty':
            s+= '(?P<' + 'qty'+ '>\d+[,\d+]*[.\d+]*)'
        elif updated_matches[i] == 'unit_price':
            s+= '(?P<' + 'unit_price'+ '>\d+[,\d+]*[.\d+]*)'
        elif updated_matches[i] == 'price':
            s+= '(?P<' + 'price'+ '>\$?\d+[,\d+]*[.\d+]*\$?)'
        if i < len(updated_matches)-1:
            s+='\s+'
        else:
            s+='\s*'
    if s:
        return s
    else:
        return ''
    
import yaml

def create_yml(text):
    x,y = table(text)
    s = table_pattern(y)
    name = detect_names(text)
    company = detect_company(text)
    data = {
        'issuer': [name],
        'keywords': [company],
        'fields': {
            'email': ['\\w+@\\w+.\\w+'],
            'phone': [
                '\\(\\d{3}\\)\\s+\\d{3}-\\d{4}',
                '(\\+?8?8?01[3-9]\\d{8})',
                '(\\+?8?8?01[3-9]\\d{8})'
            ],
            'amount': [
                '\\s*Total:\\s+(\\d+)',
                '\\s*Grand\\sTotal\\s+(\\d+.\\d+)',
                '\\s*TOTAL\\s+(\\d+,\\d+.\\d+)',
                # '\\s*Sub Total:\\s+(\\d+)',
                # '\\s*Sub-Total:\\s+(\\d+)',
            ],
            'date': [
                '\\s+(\\d{1,2}/\\d{1,2}/\\d{4})',
                '\\d{2}-[A-Za-z]{3}-\\d{4}'
            ],
            'invoice_number': [
                '\\s+(\\w{2}\\d{6})',
                'Invoice\\s+No.\\s+(\\d{7})',
                'Order # (\\d{10})'
            ],
        },
        'lines': {
            'start': [x],
            'end': '\\s+Total:\\s',
            'first_line': [s],
            'line': '^\\s+(?P<desc>.+)$',
            'types': {
                'qty': 'float',
                'unit_price': 'float'
            }
        },
        'options': {
            'remove_whitespace': False,
            'currency': '',
            'date_formats': ['%d/%m/%y'],
        },
        'languages': ['en']
    }
    #print(data)
    with open('data.yaml', 'w') as file:
        yaml.dump(data, file)