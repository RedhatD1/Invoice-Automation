def log_write(file_name, content) -> None:
    from core.config import settings
    if settings.LOG_ENABLED:
        open_file = open(file_name, "a+")
        open_file.write(content)
        print("file write successfully done")
        open_file.close()
    else:
        print("log writing disabled")


