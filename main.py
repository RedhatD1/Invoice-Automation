from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.regex_algorithm import details_utils, reader, extractor, utils
from backend.regex_algorithm_sunjid_bhai import regex2
from backend.other import template
from fastapi.staticfiles import StaticFiles
import json
from helpers.date_manipulator import get_date
from helpers.log import log_write


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


@app.get("/")
def sample_api():
    return {"message": "hello world"}


@app.get("/items/")
async def get_items(request: Request):
    response = {
        "customer_info": {
            "name": "",
            "phone": "",
            "email": "",
            "billing_address": "",
            "shipping_address": ""
        },
        "item_details": [
            {
                "name": "",
                "description": "",
                "quantity": "",
                "unit_price": "",
                "amount": "",
                "currency": ""
            }
        ],
        "total_amount": "",
        "note": "",
        "invoice_info": {
            "date": "",
            "number": ""
        }
    }

    # Get the query parameters from the request
    params = request.query_params

    # Extract specific query parameters
    file_name = params.get("pdfFileName")
    algorithm = params.get("algorithm")
    try:

        if algorithm == "regex2":
            response = regex2.extract_information_from_invoice(file_name)
        elif algorithm == "ocr":
            response = template.other(file_name)  # template, does error handling
        elif algorithm == "dl":
            response = template.other(file_name)
        else:
            response = extractor.get_json_formatted(file_name)  # new regex, does error handling

        return JSONResponse(content=response)
    except Exception as e:
        # print(e)
        return JSONResponse(content=response)
    finally:
        file_name = f"./logs/document_extraction_req_res_{get_date('%d-%m-%Y')}.txt"
        log_content = f"{get_date('%d-%m-%Y %H:%I:%S')} | req_url {str(request.url)} | res {json.dumps(response)} \n"
        log_write(file_name, log_content)

