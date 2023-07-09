import sys
sys.path.append('backend/script')
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from extraction_regex import *

app = FastAPI()

@app.get("/")
def read_root():
    json_data = execute_script('invoices/2.pdf')
    print (json_data)
    return JSONResponse(content=json_data)



