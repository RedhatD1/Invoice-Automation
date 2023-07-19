from pydantic import BaseModel


class Customer(BaseModel):
    name: str = ''
    phone: str = ''
    email: str = ''
    billing_address: str = ''
    shipping_address: str = ''


class Invoice(BaseModel):
    number: str
    date: str = ''


class ItemDetail(BaseModel):
    name: str = ''
    unit_price: str = ''
    quantity: str = ''
    discount: str = ''
    amount: str = ''
    currency: str = 'Taka'


class InvoiceExtractionFormat(BaseModel):
    customer_info: Customer
    invoice_info: Invoice
    item_details: list[ItemDetail] = []
    total_amount: str = 0.0
    note: str = ''


class WelcomeMessage(BaseModel):
    name: str
    tagline: str = ''
    version: str
