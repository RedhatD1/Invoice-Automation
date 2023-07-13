from backend.regex_algorithm import reader

text = reader.read_invoice('../../invoices/15.pdf')
print(text)