from pydantic import BaseModel
from typing import Union


class Customer(BaseModel):
    name: str = ''
    phone: str = ''
    email: str = ''
    billing_address: str = ''
    shipping_address: str = ''


class Invoice(BaseModel):
    number: str = ''
    date: str = ''
    shop_name: str = ''


class ItemDetail(BaseModel):
    name: str = ''
    unit_price: Union[float, str] = ''
    quantity: Union[int, str] = ''
    discount: Union[float, str] = ''
    amount: Union[float, str] = ''
    currency: str = 'Taka'


class IndividualPdfParsingResponse(BaseModel):
    customer_info: Customer
    invoice_info: Invoice
    item_details: list[ItemDetail] = []
    total_amount: Union[float, str] = 0.0
    note: str = ''


class InvoiceParsingResponse(BaseModel):
    status: bool = True
    extract_data: IndividualPdfParsingResponse


class WelcomeMessage(BaseModel):
    title: str
    tagline: str = ''
    version: str
