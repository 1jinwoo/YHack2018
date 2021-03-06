# libraries import
from keras.models import Sequential
from keras import layers
from sklearn.feature_extraction.text import CountVectorizer

# file import
import data_cleaner as dc
import model_helper as mh

df = dc.clean_item_data(0)
df = dc.cleanup_categoryid(df)[0]

# vectorize training input data
_X_train, _, _X_test, Y_train, _, Y_test = dc.data_split(df, 0.8, 0, 0.2)
vectorizer = CountVectorizer()

# convert pandas dataframes to list of strings
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
dropout_percentage = 0.6
neurons = 100
epoch = 4

print('X train shape: ' + str(X_train.shape[1]))
input_dim = X_train.shape[1] # Number of features
output_dim = df['categoryId'].nunique()
model = Sequential()
model.add(layers.Dense(neurons, input_dim=input_dim, activation='relu'))
model.add(layers.Dropout(dropout_percentage))
model.add(layers.Dense(output_dim, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
history = model.fit(X_train, Y_train,
                    epochs=epoch,
                    verbose=1,
                    validation_data=(X_test, Y_test),
                    batch_size=10)
print(model.summary())

loss, accuracy = model.evaluate(X_train, Y_train, verbose=False)
train_accuracy = round(accuracy, 3)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, Y_test, verbose=False)
test_accuracy = round(accuracy, 3)
print("Testing Accuracy:  {:.4f}".format(accuracy))
mh.plot_history(history, "One Layer Model", train_accuracy, test_accuracy, neurons, dropout_percentage, epoch)
