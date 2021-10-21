import io
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import xgboost as xgb
import pickle


max_review_len = 30
max_words = 35


letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя. '
print('TF version {0}'.format(tf.__version__))
print('XGBoost version {0}'.format(xgb.__version__))



def load_tokenizer(filename = 'saved_models/tokenizer.json'):
  with open(filename) as f:
    data = json.load(f)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)
    print('Токенайзер загружен')
    return tokenizer

def load_model():
  model = tf.keras.models.load_model('saved_models/model_fio_classificaion.h5')
  print('Модель xgboost загружена')
  return model


def load_xgb():
  bst = xgb.Booster()  # init model
  filehandler = open('saved_models/xgb.pickle.dat', 'rb')
  bst = pickle.load(filehandler)

  print('Модель классификации загружена')
  return bst


# def string_to_token(list_values):
#   tokenaizer = load_tokenizer()
#   sequences = []
#   for w in list_values:
#     sequences.append(np.array(tokenaizer.texts_to_sequences([w.lower()])[0]))
#
#   return sequences
#
#
# def token_to_tensor(token, max_review_len=40):
#   tensor = pad_sequences(token, maxlen=max_review_len)
#   return tensor
#
#
# def predict(value_string):
#
#   model = load_model()
#   value_string = string_to_token(value_string)
#   value_string = token_to_tensor(value_string)
#   print('Прогнозируем сущности...')
#   fio_class = np.argmax(model.predict(value_string), axis = 1)
#   # print(fio_class)
#   return fio_class


class Predictor():
  def __init__(self):

    self.directory = '/files/'
    self.model = load_model()
    self.xgb   = load_xgb()
    self.tokenizer = load_tokenizer()

  def string_to_token(self, list_values):
    sequences = []
    for w in list_values:
      sequences.append(np.array(self.tokenizer.texts_to_sequences([w.lower()])[0]))

    return sequences

  def token_to_tensor(self, token, max_review_len=max_review_len):
    tensor = pad_sequences(token, maxlen=max_review_len)
    return tensor


  def bst_predict(self, value_string):

    value_string = self.string_to_token(value_string)
    value_string = self.token_to_tensor(value_string)
    print('Прогнозируем сущности...')
    # print(value_string, value_string[:,-3:])

    fio_class = self.xgb.predict(value_string)
    # print(fio_class)
    return fio_class



  def predict(self, value_string):

    value_string = self.string_to_token(value_string)
    value_string = self.token_to_tensor(value_string)
    print('Прогнозируем сущности...')
    # print(value_string, value_string[:,-3:])

    fio_class = np.argmax(self.model.predict(value_string[:,-3:]), axis=1)
    # print(fio_class)
    return fio_class


