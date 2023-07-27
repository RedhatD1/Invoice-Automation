from pydantic import BaseModel, constr


class CvRequestModel(BaseModel):
    file_list: list[str]
    algorithm: str
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
    cgpa: float | str = 0.0


class IndividualCvParsingResponse(BaseModel):
    candidate_info: Candidate
    education_info: list[Education]
    experience: float | str = ""
    score: float = 0.0
    rank: int | str = "--"


class CvParsingResponse(BaseModel):
    status: bool = True
    cv_list: list[IndividualCvParsingResponse]


class ErrorResponse(BaseModel):
    status: bool = False
    message: str = 'Something is wrong, Please try again later.'
