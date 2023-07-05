import json
import requests

def remove_none_units(dictionary):
    if isinstance(dictionary, list):
        return [remove_none_units(item) for item in dictionary if item]
    elif isinstance(dictionary, dict):
        return {key: remove_none_units(value) for key, value in dictionary.items() if value}
    else:
        return dictionary
    
def main():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMWQ3YWY3NTUtMmE4Yi00YTQ2LWExNDktOGJmYzE4MGI0MjBjIiwidHlwZSI6ImFwaV90b2tlbiJ9.UU4ff7aQlcbURfQL09S1HfUbjnDCSVRQh3zwdqyOmGQ"}

    url="https://api.edenai.run/v2/ocr/receipt_parser"
    data={"providers": "google", 'language':'en'}
    files = {'file': open("invoices/1.pdf",'rb')}

    response = requests.post(url, data=data, files=files, headers=headers)

    result = json.loads(response.text)
    extracted_data = result['google']['extracted_data']
    Cleaned_dict = remove_none_units(extracted_data)
    print(json.dumps(Cleaned_dict, indent=5))


if __name__=="__main__":
    main()