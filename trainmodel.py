import numpy as np
from tensorflow import keras

# CONFIGURATION
input_shape = (4)
num_classes = 9
batch_size = 128
epochs = 15

# DATA INPUT
x_train = []
y_train = []
y_indicator_list = [['-1','-1'],['-1','0'],['-1','1'],['0','-1'],['0','0'],['0','1'],['1','-1'],['1','0'],['1','1']]

dataFile = open('tank_data.csv', 'r')
lines = dataFile.readlines()
lines.pop(0)
dataFile.close()

for line in lines:
    linedata = line.split(",")
    line_x_str = linedata[0:4]
    line_x = [int(i) for i in line_x_str]
    line_y_indicator = linedata[8:10]
    line_y = y_indicator_list.index(line_y_indicator)
    x_train.append(line_x)
    y_train.append(line_y)

y_train = keras.utils.to_categorical(y_train, num_classes)

x_train = np.array(x_train)
y_train = np.array(y_train)

# MODEL BUILDING
model = keras.Sequential(
    [
        keras.Input(shape=input_shape),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(num_classes, activation="softmax")
    ]
)
model.summary()


# TRAINING
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

# SAVE
model.save("/Users/cihan/Desktop/AI/example_tank_ai/models/model1")