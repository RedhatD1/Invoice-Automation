import sys
sys.path.append('backend/script')
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from extraction_regex import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.regex_algorithm import details_utils, reader, extractor, utils


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def sample_api():
    return {"message": "hello world"}


@app.get("/items/")
async def get_items(request: Request):

    default_response = {
        "customer_info": {
            "name": "None",
            "phone": "None",
            "email": "None",
            "billing_address": "None",
            "shipping_address": "None"
        },
        "item_details": [
            {
                "name": "None",
                "description": "None",
                "quantity": 0,
                "unit_price": 0,
                "amount": "0",
                "currency": "0"
            }
        ],
        "total_amount": "0",
        "note": "None",
        "invoice_info": {
            "date": "None",
            "number": "None"
        }
    }

    # Get the query parameters from the request
    params = request.query_params
    
    # Extract specific query parameters
    file_name = params.get("pdfFileName")
    # algo_name = params.get("algo_name")
    try: 
        # json_data = execute_script(file_name) # old regex, gives errors
        json_data = extractor.get_json_formatted(file_name) # new regex, does error handling
        return JSONResponse(content=json_data)
    except Exception as e:
        return JSONResponse(content=default_response)
