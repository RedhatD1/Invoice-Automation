import json
import os
import pandas as pd
# def save_to_excel():
#     data = {'Merchant Name' : m_name
#             }
#     df = pd.DataFrame([data])
#     excel_file = 'excel_file.xlsx'
#     try:
#       existing_data = pd.read_excel(excel_file)
#       combined_data = pd.concat([existing_data, df], ignore_index=True)
#       combined_data.to_excel('/content/drive/MyDrive/CV_extraction_Reddot/mumu/mumu_excel_file.xlsx', index=False)
#       #print("Data appended successfully!")
#     except FileNotFoundError:
#       df.to_excel(excel_file, index=False)
#       #print("New file created with the data.")

folder_path = 'output/'
for filename in os.listdir(folder_path):
        if filename.endswith('.json'): # or filename.endswith('.doc') or filename.endswith('.docx'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path,'r') as f:
              data = json.load(f)
            #print(data['receipts'][0].keys())
            #print('\n')
            items = data['receipts'][0]['items']
            print(f"your purchase at {data['receipts'][0]['merchant_name']} \n")
            if items:
              print("Description   -  Quantity  -  UnitPrice  -  Amount ")
              for item in items:
                print(f"{item['description']} - {item['qty']} - {item['unitPrice']} - {item['amount']}")
            else:
                print(f"No items found")
            print('\n')
            print(f"Subtotal - {data['receipts'][0]['subtotal']}")
            print(f"Tax - {data['receipts'][0]['tax']}")
            print(f"Service Charge - {data['receipts'][0]['service_charge']}")
            print(f"Total - {data['receipts'][0]['total']}")
            print(f"Tip - {data['receipts'][0]['tip']}\n")
            print(f"payment_method - {data['receipts'][0]['payment_method']}")
            print(f"payment_details - {data['receipts'][0]['payment_details']}")
            print(f"Credit Card Info - {data['receipts'][0]['credit_card_type']} - {data['receipts'][0]['credit_card_number']}")
            print("-----------------------------------\n")