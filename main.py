# from flask import Flask
import pandas as pd
import pdf2 as pdf
import tf_fio
import os

pdf_name2 = os.curdir + '/files/documents_files_1135_02032020_PR-49_20_Ovchinskii_VA_Gosydarstvennaya_inspekciya_po_kontrolu_za_ispolzovaniem_obektov_nedvijimosti_goroda_Moskvi.pdf'
pdf_name2 = os.curdir + '/files/documents_docs_06102016_64-02-1201_16_Sobyanin_SS_Pechatnikov_LM.pdf'
# app = Flask(__name__)
#

# @app.route('/')

def recogn_pdf(file_name, dpi = 400):
    extractor = pdf.PDFExtractor3(file_name, dpi = dpi)
    extractor.convert_to_jpg()
    df_recogn = extractor.parse_page()
    predict = tf_fio.predict(df_recogn.text)
    df_recogn['flag'] = pd.Series(predict)
    print(df_recogn)

    hide = pdf.Hide_PD(extractor.pagelist)
    hide.fill_image(df_recogn[df_recogn.flag == 2])
    extractor.img2pdf()

    print('Output file {0}'.format(extractor.output_fname))

    return extractor.output_fname

recogn_pdf(pdf_name2)