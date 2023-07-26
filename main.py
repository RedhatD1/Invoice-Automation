from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from helpers.date_manipulator import get_date
from helpers.log import log_write
from schemas.invoice import InvoiceParsingResponse, WelcomeMessage
from schemas.cv import CvRequestModel, CvParsingResponse, ErrorResponse
from helpers.pdf_extractor import process_pdf
from helpers.general_helper import unlink_file, check_file_existence
from fastapi.encoders import jsonable_encoder
from typing import Union
from backend.cv_extraction.getCvResult import getJSON


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = "documents/invoices"
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/", response_model=WelcomeMessage, status_code=status.HTTP_200_OK, tags=['Welcome'], summary='Welcome API')
def sample_api():
    return {"name": "FastAPI", "version": "0.99.1"}


@app.get("/invoice-extraction/{file_name}", response_model=Union[InvoiceParsingResponse, ErrorResponse],
         tags=['Invoice Extraction'], summary='Extract data from invoice')
async def extract_invoice(request: Request, file_name: str, algorithm: str = 'regex'):
    response = {}
    try:
        print('file_name', file_name, 'algorithm', algorithm)
        file_path = f"documents/invoices/{file_name}"
        if check_file_existence(file_path):
            print('file is exists')
            pdf_response = process_pdf(file_name, algorithm)
            print(pdf_response)
            unlink_file(file_path)
            response = InvoiceParsingResponse(extract_data=pdf_response)
            return response
        else:
            response = ErrorResponse(message='File is not found')
            return response
    except Exception as e:
        print('internal error', e)
        response = ErrorResponse()
        return response
    finally:
        file_name = f"./logs/pdf_extraction_req_res_{get_date('%d-%m-%Y')}.txt"
        log_content = f"{get_date('%d-%m-%Y %H:%I:%S')} | req_url {str(request.url)} | " \
                      f"response {jsonable_encoder(response)}\n"
        log_write(file_name, log_content)


@app.post("/cv-extraction", response_model=Union[CvParsingResponse, ErrorResponse], tags=['CV Extraction'],
          summary='Extract data from CV')
async def extract_cv(request: Request, cv_model: CvRequestModel):
    response = {}
    try:
        print(cv_model)
        file_list = cv_model.file_list
        algorithm = cv_model.algorithm
        job_description = cv_model.job_description
        parse_cv: list = []
        for file_name in file_list:
            print(file_name)
            file_path = f"documents/cv/{file_name}"
            if check_file_existence(file_path):
                individual_cv_response = getJSON(file_name, job_description, algorithm)
                print(individual_cv_response)
                parse_cv.append(individual_cv_response)
                unlink_file(file_path)
        print(parse_cv)
        response = CvParsingResponse(cv_list=parse_cv)
        return response
    except Exception as e:
        print('internal error', e)
        response = ErrorResponse()
        return response
    finally:
        file_name = f"./logs/cv_extraction_req_res_{get_date('%d-%m-%Y')}.txt"
        log_content = f"{get_date('%d-%m-%Y %H:%I:%S')} | req_url {str(request.url)} | " \
                      f"request data {jsonable_encoder(cv_model)} | response {jsonable_encoder(response)} \n"
        log_write(file_name, log_content)
