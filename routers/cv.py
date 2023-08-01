from fastapi import APIRouter, Request
from helpers.date_manipulator import get_date
from helpers.log import log_write
from schemas.cv import CvRequestModel, CvParsingResponse, ErrorResponse
from helpers.general_helper import unlink_file, check_file_existence
from fastapi.encoders import jsonable_encoder
from typing import Union
from extraction_algorithms.cv.extract import get_json
from extraction_algorithms.cv.helpers import sort_extracted_cv_list, dump_to_csv

router = APIRouter()


@router.post("/cv-extraction", response_model=Union[CvParsingResponse, ErrorResponse], tags=['CV Extraction'],
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
                individual_cv_response = get_json(file_name, job_description, algorithm)
                print(individual_cv_response)
                parse_cv.append(individual_cv_response)
                unlink_file(file_path)
        # print(parse_cv)
        parse_cv = sort_extracted_cv_list.sort_list(parse_cv)
        response = CvParsingResponse(cv_list=parse_cv)
        print(len(parse_cv))
        if len(parse_cv):
            dump_to_csv.export_csv(parse_cv)
        return response
    except Exception as e:
        print('internal error', e)
        response = ErrorResponse()
        return response
    finally:
        file_name = f"logs/cv_extraction_req_res_{get_date('%d-%m-%Y')}.txt"
        log_content = f"{get_date('%d-%m-%Y %H:%I:%S')} | req_url {str(request.url)} | " \
                      f"request data {jsonable_encoder(cv_model)} | response {jsonable_encoder(response)} \n"
        log_write(file_name, log_content)
