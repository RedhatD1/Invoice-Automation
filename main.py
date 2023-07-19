from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from backend.regex_algorithm import extractor
from backend.regex_algorithm_sunjid_bhai import regex2
from backend.other import template
from fastapi.staticfiles import StaticFiles
import json
from helpers.date_manipulator import get_date
from helpers.log import log_write
from schemas.invoice import InvoiceExtractionFormat, WelcomeMessage
from general_response import general_response


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = "invoices"
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/", response_model=WelcomeMessage, status_code=status.HTTP_200_OK)
def sample_api():
    return {"name": "FastAPI", "version": "0.99.1"}


@app.get("/invoice-extraction/{file_name}", response_model=InvoiceExtractionFormat)
async def get_items(request: Request, file_name: str, algorithm: str = 'regex'):
    response = general_response
    try:
        if algorithm == "regex2":
            response = regex2.extract_information_from_invoice(file_name)
        elif algorithm == "ocr":
            response = template.other(file_name)  # template, does error handling
        elif algorithm == "dl":
            response = template.other(file_name)
        else:
            response = extractor.get_json_formatted(file_name)  # new regex, does error handling
        return response
    except Exception as e:
        # print(e)
        return response
    finally:
        file_name = f"./logs/document_extraction_req_res_{get_date('%d-%m-%Y')}.txt"
        log_content = f"{get_date('%d-%m-%Y %H:%I:%S')} | req_url {str(request.url)} | res {json.dumps(response)} \n"
        log_write(file_name, log_content)

