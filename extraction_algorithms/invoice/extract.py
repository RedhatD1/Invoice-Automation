from extraction_algorithms.invoice.helpers import make_json


def get_json(file_name: str):
    try:
        res = make_json.get(file_name)
    except Exception as e:
        res = {}
    return res