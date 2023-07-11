def other(file_name):
    temp = "from other algo"
    default_response = {
        "customer_info": {
            "name": temp,
            "phone": temp,
            "email": temp,
            "billing_address": temp,
            "shipping_address": temp
        },
        "item_details": [
            {
                "name": temp,
                "description": temp,
                "quantity": 0,
                "unit_price": 0,
                "amount": "0",
                "currency": "0"
            }
        ],
        "total_amount": "0",
        "note": temp,
        "invoice_info": {
            "date": temp,
            "number": temp
        }
    }

    return default_response