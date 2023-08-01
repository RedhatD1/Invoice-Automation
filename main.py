from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from schemas.invoice import WelcomeMessage
from routers import invoice, cv
from core.config import settings


app = FastAPI(
    title=settings.APP_TITLE,
    summary=settings.APP_SUMMARY,
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    openapi_url=settings.OPENAPI_URL
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/assets", StaticFiles(directory=settings.STATIC_DIRECTORY), name="static")


app.include_router(invoice.router)
app.include_router(cv.router)


@app.get("/", response_model=WelcomeMessage, status_code=status.HTTP_200_OK, tags=['Welcome'], summary='Welcome API')
def welcome():
    return {"title": settings.APP_TITLE, "version": settings.APP_VERSION}
