from backend.regex_algorithm import reader

text = reader.read_invoice('../../documents/invoices/17.pdf')
print(text)