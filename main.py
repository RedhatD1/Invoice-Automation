from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.regex_algorithm import details_utils, reader, extractor, utils
from backend.regex_algorithm_sunjid_bhai import regex2
from backend.other import template
from fastapi.staticfiles import StaticFiles

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
    default_response = {
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
            json_data = regex2.extract_information_from_invoice(file_name)
        elif algorithm == "ocr":
            json_data = template.other(file_name)  # template, does error handling
        elif algorithm == "dl":
            json_data = template.other(file_name)
        else:
            json_data = extractor.get_json_formatted(file_name)  # new regex, does error handling

        return JSONResponse(content=json_data)
    except Exception as e:
        # print(e)
        return JSONResponse(content=default_response)
