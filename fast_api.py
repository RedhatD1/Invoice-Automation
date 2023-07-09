import sys
sys.path.append('backend/script')
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from extraction_regex import *

app = FastAPI()

@app.get("/items/")
async def get_items(request: Request):
    # Get the query parameters from the request
    params = request.query_params
    
    # Extract specific query parameters
    file_name = params.get("pdf_file_name")
    json_data = execute_script(file_name)
    
    # Return the response
    return JSONResponse(content=json_data)
