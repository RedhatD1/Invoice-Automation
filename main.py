from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from schemas.invoice import WelcomeMessage
from routers import invoice, cv


app = FastAPI(
    title="Document extraction API collection",
    summary="Extract content from the PDF and CV",
    version="1.0.0",
    docs_url="/api-documentation",
    openapi_url="/api/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
static_path = "documents/invoices"
app.mount("/static", StaticFiles(directory=static_path), name="static")


app.include_router(invoice.router)
app.include_router(cv.router)


@app.get("/", response_model=WelcomeMessage, status_code=status.HTTP_200_OK, tags=['Welcome'], summary='Welcome API')
def welcome():
    return {"name": "FastAPI", "version": "0.99.1"}
