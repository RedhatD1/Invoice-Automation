from fastapi import APIRouter, Request
from helpers.date_manipulator import get_date
from helpers.log import log_write
from schemas.invoice import InvoiceParsingResponse
from schemas.cv import ErrorResponse
from helpers.pdf_extractor import process_pdf
from helpers.general_helper import unlink_file, check_file_existence
from fastapi.encoders import jsonable_encoder
from typing import Union


router = APIRouter()


@router.get("/invoice-extraction/{file_name}", response_model=Union[InvoiceParsingResponse, ErrorResponse],
            tags=['Invoice Extraction'], summary='Extract data from invoice')
async def extract_invoice(request: Request, file_name: str, algorithm: str = 'regex'):
    response = {}
    try:
        # print('file_name', file_name, 'algorithm', algorithm)
        file_path = f"documents/invoices/{file_name}"
        # print(file_path)
        if check_file_existence(file_path):
            pdf_response = process_pdf(file_name, algorithm)
            # print(pdf_response)
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
        file_name = f"logs/pdf_extraction_req_res_{get_date('%d-%m-%Y')}.txt"
        log_content = f"{get_date('%d-%m-%Y %H:%I:%S')} | req_url {str(request.url)} | " \
                      f"response {jsonable_encoder(response)}\n"
        log_write(file_name, log_content)
