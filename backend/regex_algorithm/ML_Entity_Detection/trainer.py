import random
import spacy
import json
from spacy.training.example import Example
import os

print(os.getcwd())

# Assuming your JSON file is named 'training_data.json'
json_file_path = 'ML_Entity_Detection/training_data.json'

with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the language model
nlp = spacy.load('en_core_web_sm')

# Add the entity recognizer to the pipeline if it's not already there
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)

# Assuming your data is in the format you provided

training_data = []
for example in data:
    text = example['text']
    entities = [(int(ent['start']), int(ent['end']), ent['label']) for ent in example['entities']]
    training_data.append((text, {'entities': entities}))

# Train the entity recognizer
n_iter = 100
for _ in range(n_iter):
    for example in training_data:
        text, entities = example
        doc = nlp.make_doc(text)
        gold = Example.from_dict(doc, entities)
        nlp.update([gold], drop=0.3)


output_dir = 'ML_Entity_Detection/model'
nlp.to_disk(output_dir)
