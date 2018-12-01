# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:55:41 2018

@author: Justin Won
"""

# libraries import
from keras.models import Sequential
from keras import layers
from sklearn.feature_extraction.text import CountVectorizer

# file import
import data_cleaner as dc
import model_helper as mh

df = dc.clean_item_data()
df = dc.cleanup_categoryid(df)

# vectorize training input data
_X_train, _, _X_test, Y_train, _, Y_test = dc.data_split(df, 0.8, 0, 0.2)
vectorizer = CountVectorizer()

x_train_list = []
x_test_list = []
for _, row in _X_train.iterrows():
    x_train_list.append(row[0])

for _, row in _X_test.iterrows():
    x_test_list.append(row[0])

vectorizer.fit(x_train_list)
X_train = vectorizer.transform(x_train_list)
X_test = vectorizer.transform(x_test_list)

# Neural Network
print('X train shape: ' + str(X_train.shape[1]))
input_dim = X_train.shape[1] # Number of features
output_dim = df['categoryId'].nunique()
model = Sequential()


# LSTM layer
model.add(layers.LSTM(units=50,
                      activation='tanh',
                      recurrent_activation='hard_sigmoid'))

model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(output_dim, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# print(model.summary())
print('X_train.shape' + str(X_train.shape))
print('Y_train.shape' + str(Y_train.shape))
history = model.fit(X_train, Y_train,
                    epochs=4,
                    verbose=1,
                    validation_data=(X_test, Y_test))

loss, accuracy = model.evaluate(X_train, Y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, Y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))
mh.plot_history(history)