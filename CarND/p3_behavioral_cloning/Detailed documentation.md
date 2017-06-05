## Project 3: Behavioral Cloning

setup

```shell
source activate car
pip install python-socketio
pip install eventlet
pip install keras
```

import the pre-recorded data from `data.zip`(330 MB)

```python
import csv 
import cv2
lines =[]
with open("data/driving_log.csv") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader) #['center', 'left', 'right', 'steering', 'throttle', 'brake', 'speed']
    for line in reader:
        lines.append(line)
        
images = []
measurements = []
for line in lines:
    source_path = line[0]  # image by center camera
    filename = source_path.split("/")[-1]
    current_path = "data/IMG/" + filename
    image = cv2.imread(current_path) # shape (160,320,3)
    images.append(image)
    measurement = float(line[3])  # steer
    measurements.append(measurement)
    
import numpy as np
X_train = np.array(images)  #(8036, 160, 320, 3)
y_train = np.array(measurements) #(8036,)
```

Model 1: use **keras and no-hidden layer neural network** for initial training

```python
from keras.models import Sequential
from keras.layers import Flatten, Dense
model = Sequential()
model.add(Flatten(input_shape=(160,320,3)))
model.add(Dense(1))
model.compile(loss="mse", optimizer = "adam")
model.fit(X_train, y_train, validation_split=0.2,shuffle = True, nb_epoch=7)
model.save('model.h5')  # save model to .h5 file, including architechture, weights, loss, optimizer
# model.load_model('model.h5') # reinstantiate model
```

7 epochs takes 1 minute,bring loss to ~2000. open`beta_simulator_mac.app`  and run `python drive.py model.h5`. In autonomous mode, the car fell out of curve in a few seconds!

Model 2: **Normalize the input image by adding lambda layer**, the loss goes down to 2. Then the car can drive more then 10 seconds before stuck on the curb. 

Model 3: try the **LeNet 5-layer** by adding 2 cnn. The cost goes down to 0.01 in 2 epochs. And it can drive more than 1 minutes all the way to the bridge. After bridge, there is a sharp turn where the car fails to steer enough. 

```python
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
model.add(Lambda(lambda x: x/255.0-0.5, input_shape=(160,320,3)))
model.add(Convolution2D(6,(5,5),activation = "relu"))
model.add(MaxPooling2D((2, 2)))
model.add(Convolution2D(6,(5,5),activation = "relu"))
model.add(MaxPooling2D((2, 2)))          
model.add(Dropout(0.5))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(128))
model.add(Dense(84))
model.add(Dense(1))

model.compile(loss="mse", optimizer = "adam")
model.fit(X_train, y_train, validation_split=0.2,shuffle = True, epochs=4)
model.save('model.h5')
```

Model 4: **data augmentation: flipping images**. Previous dataset only teaches the car the steer left, flipping dataset will teach the car to steer right. 

```python
import numpy as np
image_flipped = np.fliplr(image)
measurement_flipped = -measurement
```

Model 5: **data augmentation: using multiple cameras**.

```python
car_images = []
steering_angles = []
for line in lines:
    image_center = cv2.imread("data"+line[0]) #center image 
    image_left = cv2.imread("data"+line[1]) #center image 
	image_right = cv2.imread("data"+line[2]) #center image 
    images.append(image)
    steering_center = float(line[3])  # steer
    correction = 0.2 # this is a parameter to tune
    steering_left = steering_center + correction
    steering_right = steering_center - correction
    car_images.extend(img_center, img_left, img_right)
    steering_angles.extend(steering_center, steering_left, steering_right)
```

Model 6: **cropping images**.

```python
from keras.layers import Cropping2D
model = Sequential()
model.add(Lambda(lambda x: x/255.0-0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25),(0,0)))) # (top,bottom),(left,right)
```

Model 7: **NVIDIA architecture: 5 cnn layer**. the loss is still kept at 0.01 and the car drives all right until it reaches the bridge. 

```python
model.add(Convolution2D(24,(5,5),subsample = (2,2), activation = "relu"))
model.add(Convolution2D(36,(5,5),subsample = (2,2), activation = "relu"))
model.add(Convolution2D(48,(5,5),activation = "relu"))
model.add(Convolution2D(64,(3,3),activation = "relu"))
model.add(Convolution2D(64,(3,3),activation = "relu"))
```

Model 8: **more data collection**. If your training data is all focused on driving in the middle of the road, your model don't know what to do when it gets off to the side of the road. So you will need to create some training data dealing with that situation. So some guidelines for data collection:

- 2 laps of center lane driving
- 1 lap of recovering dring from the sides
- 1 lap focusing on driving smoothingly around the curves.

**plot training loss and validation loss** to see whether there is overfitting.

```python
history = model.fit(...)
print(history_object.history.keys())
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.show()
```

use **generator** to get the burden off the memory. The trick is if your memory is large enough to load the variables, then loading it all at once is actually much faster. 

### learn from peers

[Paul Heraty kick off a hot discussion by sharing his tricks](https://carnd-forums.udacity.com/questions/26214464/behavioral-cloning-cheatsheet#), such as:

1. shrink the images to 4 times smaller
2. udacity simulator is 10 Hz, which means you get 10 images per second.  A 50 Hz simulator will generate much smoother driving angle. And analog joystick also helps.

I wasted some time playing the tedious games for ~ 20 laps and record enough data. No matter how I tune the model, the stupid car could not steer enough in the 1st sharp turn after the bridge. 

As [Carlos Galvez](https://carnd-forums.udacity.com/questions/users?username=carlosgalvezp) pointed out, the No. 0 issue is drive.py sends RGB images to the model; cv2.imread() reads images in BGR format. I tried to dig into drive.py and was freaked out by [`socketio.Server.on()`](https://python-socketio.readthedocs.io/en/latest/#socketio.Server.on) and `PIL.Image.open(BytesIO(base64.b64decode(imgString)))`.  Finally, I just took the coverstion code.

After this color correction, the car can smooth drive through the 3 sharp turns after the bridge and finish the task. No need for data augmentation such as flipping or multiple cameras, recovering drives, or any trick by Paul.

The last two commands to generate a video that records autonomous mode.

```shell
python drive.py model.h5 run1
python video.py run1 
```



## commaai

https://www.youtube.com/watch?v=Hxoke1lDJ9w

George Hotz addressed the following issues:

1. behavior cloning doesn't work because computer don't really understand the rule, such as driving in the center instead of keeping straight. Highway exit, ride in the middle? 
2. reinforcement learning: you don't want the car to explore. 

## 