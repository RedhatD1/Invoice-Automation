from typing import Dict

import spacy

# Replace 'path_to_saved_model' with the actual path where you saved the model
def ner_extraction(text: str) -> Dict:
    nlp = spacy.load('extraction_algorithms/invoice/helpers/ML_Entity_Detection/model')
    doc = nlp(text)
    target_attribute = {
        'name': '',
        'shop_name': '',
        'shipping_address': '',
    }
    for ent in doc.ents:
        target_attribute[ent.label_] = ent.text

    return target_attribute
