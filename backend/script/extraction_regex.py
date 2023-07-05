from read_pdf import *
import re

def main():
    path = 'invoices/2.pdf'
    invoice = read_pdf(path)
    print(invoice)

if __name__ == "__main__":
    main()