import io
import json
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, GRU
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.metrics import Recall, Precision
import numpy as np
import pandas as pd


max_review_len = 40
max_words = 34


letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
print(tf.__version__)


def load_tokenizer(filename = 'saved_models/tokenizer.json'):
  with open(filename) as f:
    data = json.load(f)
    tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)
    print('Токенайзер загружен')
    return tokenizer

def load_model():
  model = tf.keras.models.load_model('saved_models/model_fio_classificaion.h5')
  print('Модель классификации загружена')
  return model


def string_to_token(list_values):
  tokenaizer = load_tokenizer()
  sequences = []
  for w in list_values:
    sequences.append(np.array(tokenaizer.texts_to_sequences([w.lower()])[0]))

  return sequences


def token_to_tensor(token, max_review_len=40):
  tensor = pad_sequences(token, maxlen=max_review_len)
  return tensor


# def string_to_token(str):
#   tokenaizer = load_tokenizer()
#   tokenaizer.char_level = True
#   sequence = tokenaizer.texts_to_sequences(str)
#   sequence = [x[0] for x in sequence]
#   return sequence
#
# def token_to_tensor(token, max_review_len = 40):
#   tensor = pad_sequences([token], maxlen=max_review_len)
#   return tensor


def predict(value_string):
  print('Прогнозируем сущности...')
  model = load_model()
  value_string = string_to_token(value_string)
  value_string = token_to_tensor(value_string)
  fio_class = np.argmax(model.predict(value_string), axis = 1)
  print(fio_class)
  return fio_class