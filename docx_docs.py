import os
import docx
import tf_fio
import xgboost as xgb



text_to_replace = 'Noname'

class Docs():
    def __init__(self, filename):
        self.filename = filename
        self.pagelist = []
        self.directory = os.curdir + '/files/'
        self.output_fname = ''
        self.doc = docx.Document(self.directory+self.filename)
        self.model = tf_fio.Predictor()



    def table_process(self):

        print('Обрабатываем таблицы...')
        for p in self.doc.tables:
            for t in p.table.rows:
                for c in t.cells:
                    splits = c.text.split(' ')
                    predict = self.model.bst_predict(splits)
                    for i, p in enumerate(predict):
                        if (p == 1) and (splits[i]!=''):
                            c.text = text_to_replace



    def paragraph_process(self):

        print('Обрабатываем абзацы...')
        for p in self.doc.paragraphs:
            for run in p.runs:
                splits = run.text.split(' ')
                predict = self.model.bst_predict(splits)
                for i, p in enumerate(predict):
                    if (p == 1) and (splits[i]!=''):
                        run.text = text_to_replace



    def recogn_doc(self):
        self.paragraph_process()
        self.table_process()
        self.output_fname = self.directory+self.filename.split('.')[0]+'_out.docx'
        self.doc.save(self.output_fname)
        return self.output_fname




doc = Docs('test.docx')
doc.recogn_doc()
# doc.table_process()