# Invoice Extraction Module
Takes a PDF as an input and returns a form with the extracted data. It scans the PDF and uses pattern matching and machine learning to extract the data.

## Where to put the files
Put invoices in "assets/invoices/" directory --> PDF File  
Put cv.pdf in "assets/cv" directory --> PDF File  
Job description will be provided on the API end.

# Setup
```bash
python3 -m venv env
source venv/bin/activate
pip3 install -r requirements.txt
```
For camelot error, use:
```bash
pip3 install 'camelot-py[cv]'
```
For SSL error:
```bash
pip install certifi
pip install --use-pep517 -r requirements.txt
```
Ignore spacy en_core_web_sm error for now

# Running the server
You might need to have Java runtime installed (Check if it runs without it).
**Generate ML Model:**
```bash
python -m spacy download en_core_web_sm
python trainer.py
```
**Run Server:**
```bash
uvicorn main:app --reload
```
# Installing new libraries to environment
```bash
pip3 install <library_name>
```
# Updating requirements.txt
```bash
pip3 freeze > requirements.txt
```
In case of some weird path instead of the package version:
```bash
pip list --format=freeze > requirements.txt
```

# FastAPI via POSTMAN
### CV Ranking
**POST Request:**
```link
http://127.0.0.1:8000/cv-extraction
```
**Body:**
```json
{
    "file_list": [
    "file1.pdf",
    "file2.pdf"
    ],
    "job_description": "Some job description"
}
```
### Invoice Extraction
**GET Request:**
```link
http://localhost:8000/invoice-extraction/file.pdf
```


