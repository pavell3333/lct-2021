from flask import Flask
import pandas as pd
import pdf2 as pdf
import tf_fio
import os

pdf_name2 = os.curdir + '/files/documents_files_1135_02032020_PR-49_20_Ovchinskii_VA_Gosydarstvennaya_inspekciya_po_kontrolu_za_ispolzovaniem_obektov_nedvijimosti_goroda_Moskvi.pdf'

app = Flask(__name__)

@app.route('/')
# def hello():
#     return 'HELLO'



def recogn_doc():
    extractor = pdf.PDFExtractor3(pdf_name2, dpi = 500)
    extractor.convert_to_jpg()
    df_recogn = extractor.parse_page()
    predict = tf_fio.predict(df_recogn.text)
    df_recogn['flag'] = pd.Series(predict)
    print(df_recogn)

    hide = pdf.Hide_PD(extractor.pagelist)
    hide.fill_image(df_recogn[df_recogn.flag == 2])


    # predict = tf_fio.predict(['правительство'])
    return df_recogn

recogn_doc()