import sys
sys.path.append('backend/script')
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from extraction_regex import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/items/")
async def get_items(request: Request):
    # Get the query parameters from the request
    params = request.query_params
    
    # Extract specific query parameters
    file_name = params.get("pdfFileName")
    # algo_name = params.get("algo_name")
    json_data = execute_script(file_name)
    # Return the response
    return JSONResponse(content=json_data)
