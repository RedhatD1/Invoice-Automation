import spacy

# Replace 'path_to_saved_model' with the actual path where you saved the model
nlp = spacy.load('ML_Entity_Detection/model')

text_to_analyze = "GEAR BUZZ BD\nShop : 271/A/1 (1st Floor), Motalib Plaza\n8, Poribag, Sonargaon Road, Hatirpool,\nDhaka. Ifitkar Ahmed \n01614 – 351 315\n01852 – 251 215\nINVOICE\nInvoice Number: GB2913\nHouse: 181/b, Jhilpar, Chowdhury Invoice Date: 26-07-2021\nPara Shishu Park, Matir Mosjid,\nOrder Number: 60557\nAbul Hotel\nOrder Date: 26-07-2021\nKhilgaon\nPayment Method: Cash on delivery\nDhaka\n1219\n01521533407\nProduct Quantity Price\nUIISII HM13 In-Ear Dynamic Earphone with Microphone - Blue 1 ৳ 390.00\nSKU: 39448\nWeight: 200g\nUIISII HM13 In-Ear Dynamic Earphone with Microphone - Black 1 ৳ 390.00\nSKU: 39448\nWeight: 200g\nSubtotal ৳ 780.00\nDiscount -৳ 10.00\nShipping ৳ 70.00 via Home\nDelivery\nTotal ৳ 840.00\nThanks for purchasing from us. Post a review of this product in gearbuzzbd.com and earn 50 points.\n*If you face any problem during delivery, call us at 01614 – 351 315.\n*Gear Buzz BD provides 3 days easy replacement policy."

doc = nlp(text_to_analyze)

for ent in doc.ents:
    print(ent.text, ent.label_)
