import spacy

# Replace 'path_to_saved_model' with the actual path where you saved the model
def ner_extraction(text):
    nlp = spacy.load('backend/regex_algorithm/ML_Entity_Detection/model')
    doc = nlp(text)
    dict = {
        'name': '',
        'shop_name': '',
        'shipping_address': '',
    }
    for ent in doc.ents:
        dict[ent.label_]= ent.text

    return dict
