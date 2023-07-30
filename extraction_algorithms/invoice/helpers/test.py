from extraction_algorithms.invoice.helpers import reader

text = reader.read_invoice('../../documents/invoices/17.pdf')
print(text)