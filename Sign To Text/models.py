from tensorflow.keras.applications import VGG16
from keras import models
from keras import layers
from keras.layers import Dense,   Flatten , Dropout 
from const import *
from tensorflow.keras.layers import Dense,Dropout,Conv1D,MaxPooling1D,Conv1D,Flatten
from tensorflow.keras.models import Sequential


conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(224, 224, 3))
model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(len(classes), activation='softmax'))


model_conv1d = Sequential()
model_conv1d.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(30,84)))
model_conv1d.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model_conv1d.add(Dropout(0.5))
model_conv1d.add(MaxPooling1D(pool_size=2))
model_conv1d.add(Flatten())
model_conv1d.add(Dense(100, activation='relu'))
model_conv1d.add(Dense(actions.shape[0], activation='softmax'))
model_conv1d.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model_conv1d.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])


model.load_weights('models/vgg16_transfer_learning_ourdata.h5')
model_conv1d.load_weights('models/model_conv1d.h5')