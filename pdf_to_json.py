import json
import os
import requests
url = "http://ocr.asprise.com/api/v1/receipt"
folder_path = 'hoini/'
for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'): # or filename.endswith('.doc') or filename.endswith('.docx'):
            file_path = os.path.join(folder_path, filename)
            res = requests.post(
                url,
                data = {
                    'api_key' : 'TEST',
                    'recognizer' : 'auto',
                    'ref_no' : 'oct_python_123'
                },
                files = {
                    'file' : open(file_path,'rb')
                }
            )
            f_path = 'output/'
            size = len(filename)
            filename=filename[:size - 4]
            print(filename)
            f_path = os.path.join(f_path, filename)
            with open(f_path+".json",'w') as f:
                 json.dump(json.loads(res.text),f)