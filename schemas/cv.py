from pydantic import BaseModel, constr
from typing import Union


class CvRequestModel(BaseModel):
    file_list: list[str]
    job_description: constr(max_length=1000000)


class Candidate(BaseModel):
    name: str = ''
    phone: str = ''
    email: str = ''
    present_address: str = ''
    permanent_address: str = ''


class Education(BaseModel):
    institution: str = ''
    department: str = ''
    cgpa: Union[float, str] = 0.0


class IndividualCvParsingResponse(BaseModel):
    candidate_info: Candidate
    education_info: list[Education]
    experience: Union[float, str] = ""
    score: float = 0.0
    rank: Union[int, str] = "--"


class CvParsingResponse(BaseModel):
    status: bool = True
    cv_list: list[IndividualCvParsingResponse]
    file_name: str = ''


class ErrorResponse(BaseModel):
    status: bool = False
    message: str = 'Something is wrong, Please try again later.'
