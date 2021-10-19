import os
import re
import pandas as pd
import cv2 as cv2
import pytesseract
from pdf2image import convert_from_path


pdf_name2 = os.curdir + '/files/documents_files_1135_02032020_PR-49_20_Ovchinskii_VA_Gosydarstvennaya_inspekciya_po_kontrolu_za_ispolzovaniem_obektov_nedvijimosti_goroda_Moskvi.pdf'


class PDFExtractor3():
    def __init__(self, filename, dpi = 500):
        self.dpi = dpi
        self.filename = filename
        self.frame = pd.DataFrame()
        self.pagelist = []
        self.directory = '/files/'


# конвертирование pdf в jpeg с разбивкой по страницам
    def convert_to_jpg(self):
        print('Конвертируем pdf в jpeg')
        pages = convert_from_path(self.filename, self.dpi)
        for i, page in enumerate(pages):
            fs = os.curdir + self.directory + self.filename.split('.')[0]
            fs = ''.join(fs+'out'+str(i)+'.jpg',)
            page.save(fs, 'JPEG')
            self.pagelist.append(fs)


    def parse_page(self):
        recong = pd.DataFrame()
        print('Распознаем текст на изображениях')

        for i, p in enumerate(self.pagelist):
            im = cv2.imread(p)
            img_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            df_page = pytesseract.image_to_data(img_grey, lang='rus', output_type='data.frame')
            df_page = df_page[df_page['text'].notna()]
            df_page['page_num'] = i
            self.frame = pd.concat([self.frame, df_page])

        self.frame.reset_index(inplace=True)
        self.frame['text'].replace(regex=True, inplace=True, to_replace=r'[^а-яА-Я]', value=r'')
        self.frame.drop((self.frame[self.frame['text'] == ''].index) | (self.frame[self.frame['text'] == ' '].index), inplace=True, axis=0)
        self.frame.reset_index(inplace=True)

        return self.frame



class Hide_PD():
    def __init__(self, filename_list):
        self.filename_list = filename_list

    def open_image(self, filename):
        image = cv2.imread(filename)
        return image

    def fill_rect(self, image, x,y,w,h):
        image[y:y+h,x:x+w,:] = 0

        return image

    def fill_image(self, df):

        for index, filename in enumerate(self.filename_list):
            print('Закрашиваем страницу {0}'.format(index))
            image = self.open_image(filename)
            df_temp = df[['left', 'top', 'width', 'height']][df.page_num == index]
            df_temp.reset_index(inplace=True)
            for n in range(len(df_temp)):
                x = df_temp['left'][n]
                y = df_temp['top'][n]
                w = df_temp['width'][n]
                h = df_temp['height'][n]
                image = self.fill_rect(image, x,y,w,h)
            cv2.imwrite(filename, image)








# ext = PDFExtractor3(pdf_name2)
# ext.convert_to_jpg()
# print(ext.parse_page())


