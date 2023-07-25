invoice_response = {
        "customer_info": {
            "name": "",
            "phone": "",
            "email": "",
            "billing_address": "",
            "shipping_address": ""
        },
        "item_details": [
            {
                "name": "",
                "description": "",
                "quantity": "",
                "unit_price": "",
                "amount": "",
                "discount": "",
                "currency": "BDT"
            }
        ],
        "total_amount": 0.0,
        "note": "",
        "invoice_info": {
            "date": "",
            "number": "",
            "shop_name": ""
        }
    }

individual_cv_response = {
        "candidate_info": {
            "name": "",
            "phone": "",
            "email": "",
            "present_address": "",
            "permanent_address": ""
        },
        "education_info": {
                "institution": "",
                "department": "",
                "cgpa": 0.0
        },
        "experience": 0.0,
        "score": 0.0,
        "rank": "--"
    }
cv_response = {
    "status: bool": True,
    "cv_list": [individual_cv_response],
    "message": "File extraction successfully done."
}

