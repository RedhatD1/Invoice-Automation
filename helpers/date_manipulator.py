import datetime


def get_date(date_format: str) -> str:
    date_obj = datetime.datetime.now()
    return date_obj.strftime(date_format)
