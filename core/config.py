from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_VERSION: str = "1.0.0"
    APP_TITLE: str = "Document extraction API collection"
    APP_SUMMARY: str = "Extract content from the PDF and CV"
    DOCS_URL: str = "/api-documentation"
    OPENAPI_URL: str = "/api/openapi.json"
    LOG_ENABLED: bool = True
    STATIC_DIRECTORY: str = "assets"


settings = Settings()
