I had stuck in this project for nearly 2 weeks and finally dropout. After I finished self-driving car (1st term), I looked back and have some new ideas. 

The project, Build a Digit Recognition Program, is very similar to [vehicle detection](http://www.yuchao.us/2017/04/self-driving-car-nd-a5-vehicle-detection.html). The basic flows are:

1. build a binary classifier to recognize whether a fixed-size image has a digit or not
2. build a 10-class classifier to recognize the number from 0 to 9
3. Given an image with size larger than the training image, design a sliding window algorithm to slice the image
4. each sliced image is applied the previous trained classifiers
5. combine identified digits and output

To me, the project provides following steps that are somewhat misleading:

- step 1: the project requires learner to use "notMNIST" or "MNIST" dataset to train model and generate data by concantenating character images.
- step 2: the project requires the learner to use "**SVHN**" (street view house number) dataset to train the model. 
- step 3: test the model on newly captured image 
- step 4: use the provided **bounding boxes to train a localizer**.

Because our targeted image is more similar to SVHN, we need to focus on SVHN dataset. 

The dataset of SVHN comes in 2 formats. 

Format 1 is very raw data, .mat file is in `h5py` format which stores the metadata, We need to crop the png image and resize it to 28\*28.

Format 2 is much more handy. The image is already processed into arrays and stored in .mat file.

Details are shown in "SVHN, data preprocessing.ipynd"

## How to implement region proposal?

I haven't got time to solve it.  Hints:

https://discussions.udacity.com/t/tips-for-svhn-project-with-bounding-boxes/219969

https://leonardoaraujosantos.gitbooks.io/artificial-inteligence/content/object_localization_and_detection.html

