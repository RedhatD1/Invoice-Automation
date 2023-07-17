from backend.regex_algorithm import reader

text = reader.read_invoice('../../invoices/17.pdf')
print(text)