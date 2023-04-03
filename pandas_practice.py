import matplotlib.pyplot as plt
import csv
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import keras
import tensorflow as tf
from joblib import dump
df = pd.read_csv('data.csv')
df.head()
class_list = df.iloc[:,-1]
encoder = LabelEncoder()
y= encoder.fit_transform(class_list)
print("y: ", y)
input_parameters = df.iloc[:, 1:27]
print(input_parameters)
scaler = StandardScaler()
X = scaler.fit_transform(np.array(input_parameters,dtype=float))
print("X:", X)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2,random_state=42)
model = tf.keras.models.Sequential([
tf.keras.layers.Dense(512, activation = 'relu', input_shape = (X_train.shape[1],)),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(256, activation = 'relu'),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(128, activation = 'relu'),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(64, activation = 'relu'),
tf.keras.layers.Dropout(0.2),
tf.keras.layers.Dense(42, activation = 'softmax'),
])
print(model.summary())
def trainModel(model,epochs, optimizer):
    batch_size = 128
    model.compile(optimizer = optimizer, loss = 'sparse_categorical_crossentropy', metrics = 'accuracy')
    return model.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = epochs, batch_size = batch_size)
model_history = trainModel(model = model, epochs = 200, optimizer = 'adam')
test_loss, test_acc = model.evaluate(X_val, y_val, batch_size = 128)
print("The test loss is: ", test_loss)
print("The best accuracy is: ", test_acc*100)
dump(model, 'model.joblib')
dump(scaler, 'scaler.joblib')
dump(encoder,'encoder.joblib')