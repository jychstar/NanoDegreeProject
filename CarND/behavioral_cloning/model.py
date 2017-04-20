import csv
import cv2
import numpy as np
import matplotlib.image as mpimg
# get metadata  of the images
lines =[]
with open("data/driving_log.csv") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader) #['center', 'left', 'right', 'steering', 'throttle', 'brake', 'speed']
    for line in reader:
        lines.append(line)
# read images into numpy arrays and correct color format
images = []
measurements = []
for line in lines:
    source_path = line[0]
    filename = source_path.split("/")[-1]
    current_path = "data/IMG/" + filename
    rgb = mpimg. imread(current_path)
    #imgBGR = cv2.imread(current_path) # shape (160,320,3)
    #imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)
    images.append(rgb)
    measurement = float(line[3])  # steer
    measurements.append(measurement)
    #images.append(np.fliplr(imgRGB)) # flip images
    #measurements.append(-measurement)
# format data into numpy array and delete old variables
X_train = np.array(images)  #(8036, 160, 320, 3)
y_train = np.array(measurements) #(8036,)
del images, measurements  # save memory

# store variables to local and check the memory burden,
#  8036*160*320*3/1e9=1.23 G
import pickle
with open('data.pickle','wb') as f:
    pickle.dump((X_train,y_train), f, pickle.HIGHEST_PROTOCOL)
# recover variables
with open('data.pickle', 'rb') as f:
    metadata = pickle.load(f)

# use keras to implement NVIDIA architecture,  5 CNN layers, dropout and 4 dense layer
from keras.models import Sequential
from keras.layers import Cropping2D, Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D as Conv2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
model.add(Lambda(lambda x: x/255.0-0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((50,20),(0,0)))) # (top,bottom),(left,right)
model.add(Conv2D(24,(5,5),strides = (2,2), activation = "relu"))
model.add(Conv2D(36,(5,5),strides = (2,2), activation = "relu"))
model.add(Conv2D(48,(5,5),activation = "relu"))
model.add(Conv2D(64,(3,3),activation = "relu"))
model.add(Conv2D(64,(3,3),activation = "relu"))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))
model.compile(loss="mse", optimizer = "adam")
model.fit(X_train, y_train, validation_split=0.2,shuffle = True, epochs=5)
model.save('model.h5')  # save model to .h5 file, including architechture, weights, loss, optimizer
