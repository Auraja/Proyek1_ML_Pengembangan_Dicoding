# -*- coding: utf-8 -*-
"""NLP_Tensorflow_Dicoding_PengembanganML_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BYn9egat5orgkL4a2ItleXbpireGWMNI

NAMA : Derajat Salim Wibowo
NIM  : 2210511077
Asal : UPN Veteran Jakarta - Teknik Informatika
"""

import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout, Conv1D, MaxPooling1D
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

"""dataset :https://www.kaggle.com/datasets/rahulanand0070/youtubevideodataset"""

# Load dataset from Google Drive
df = pd.read_csv('/content/drive/MyDrive/ML/Youtube Video Dataset.csv')

df.head()

df.shape

category = pd.get_dummies(df.Category)
df_baru = pd.concat([df, category], axis=1)
df_baru = df_baru.drop(columns='Category')
df_baru

df = df.drop(['Videourl','Description'], axis=1)
df.head()

print(df.Category.unique())

title = df_baru['Title'].values
label = df_baru[['Food', 'manufacturing', 'History', 'travel blog', 'Science&Technology',
 'Art&Music']].values

title_latih, title_test, label_latih, label_test = train_test_split(title, label, test_size = 0.2 )

tokenizer = Tokenizer(num_words=50000, oov_token='x')
tokenizer.fit_on_texts(title_latih) 
tokenizer.fit_on_texts(title_test)
 
sekuens_latih = tokenizer.texts_to_sequences(title_latih)
sekuens_test = tokenizer.texts_to_sequences(title_test)
 
padded_latih = pad_sequences(sekuens_latih) 
padded_test = pad_sequences(sekuens_test)

model = tf.keras.models.Sequential([
    Embedding(input_dim=50000, output_dim=16),
    Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'),
    MaxPooling1D(pool_size=2),
    LSTM(units=64, return_sequences=True),
    LSTM(units=32),
    Dense(units=128, activation='relu'),
    Dropout(0.3),
    Dense(units=64, activation='relu'),
    Dropout(0.3),
    Dense(units=6, activation='sigmoid')
])

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('val_accuracy') > 0.90):
      print('\nakurasi telah mencapai 90%')
      self.model.stop_training = True

callbacks = myCallback()

num_epochs = 30
history = model.fit(padded_latih, label_latih, epochs=num_epochs, 
                    validation_data=(padded_test, label_test), verbose=2, callbacks=[callbacks])

plt.figure(figsize=(8,5))
plt.plot(history.history['accuracy'], label='train_accuracy')
plt.plot(history.history['val_accuracy'], label='validation_accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.ylim(ymin=0, ymax=1)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='validation_loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.ylim(ymin=0)
plt.show()