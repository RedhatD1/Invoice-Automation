# Invoice Extraction Module
Takes a PDF as an input and returns a form with the extracted data. It scans the PDF and uses pattern matching and machine learning to extract the data.

## Where to put the files
Put invoices in "assets/invoices/" directory --> PDF File  <br>
Put cv.pdf in "assets/cv" directory --> PDF File  <br>
Job description will be provided on the API end. <br>

**You must have 
- /logs
- /assets/invoices
- /assets/cv
- /assets/dump
directories in the root folder. <br>**

# Setup
**Create and activate virtual environment**
```bash
python3 -m venv env
source env/bin/activate
```
make sure it is python 3.11.4 or better<br>
**Generate ML Model:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
python 'extraction_algorithms/invoice/helpers/ML_Entity_Detection/trainer.py'
```
Here, training_data.json contains the training data, increase dataset size for better results
**Installing requirements**
```bash
pip install certifi
pip install --use-pep517 -r requirements.txt
pip install 'fastapi[all]'

pip3 install 'camelot-py[cv]'
pip3 install bs4, pdfplumber, langchain, scikit-learn, pandas
```
For uvicorn error:
```bash
pip3 install uvicorn
pip3 install pydantic==1.10.11
```

Install any missing packages if any error occurs
# Running the server
_You might need to have Java runtime installed (Check if it runs without it)._
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


