#**Traffic Sign Recognition** 

**Build a Traffic Sign Recognition Project**

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report


###Data Set Summary & Exploration

####1. Provide a basic summary of the data set and identify where in your code the summary was done. 

The code for this step is contained in the 2nd code cell of the IPython notebook.  

I used the pandas library to calculate summary statistics of the traffic
signs data set:

* The size of training set is 34799
* The size of test set is 12630
* The shape of a traffic sign image is (32,32,3)
* The number of unique classes/labels in the data set is 43

####2. Include an exploratory visualization of the dataset 

I have done these things in the code cells of this section:

1. randomly pick an image data and plot it
2. use `seaborn.countplot` to show the frequency for each sign
3. use `collections.Counter` to explictly count the value of each sign
4. build a dictionary to convert sign number to meaningful strings

###Design and Test a Model Architecture

####1. Describe howyou preprocessed the image data. What tecniques were chosen and why did you choose these techniques? 

1. I wrote explicit codes to convert 3-channel color image into 1-channel grey image
2. I normalize the values to [0,1]
3. I check the shape and image after the conversion

####2. Describe how, and identify where in your code, you set up training, validation and testing data. How much data was in each set?

For this preliminary demonstration, I used pre-processed datasets that are already divided into training, validation and testing set. The numbers for each set is 34799,4410,12630, as shown in question 1. 

It will be better if I use cross-validation technique, which fully utilize the known dataset and average out the effect of noise. 


####3. Describewhat your final model architecture looks like. Consider including a diagram and/or table describing the final model.

My final model is very similer to 5-layer LeNet, consisted of the following layers:

|        Layer         |               Description                |
| :------------------: | :--------------------------------------: |
|        Input         |              32x32x1 image               |
| Convolution 5x5+ReLU | 1x1 stride, valid padding, outputs 28x28x6 |
|   Max pooling 2x2    | 2x2 stride,  valid padding, output 14x14x6 |
| Convolution 5x5+ReLU | 1x1 stride, valid padding, outputs 10x10x16 |
|   Max pooling 2x2    | 2x2 stride,  valid padding, output 5x5x16 |
|       flatten        |                output 400                |
| Fully connected+ReLU |                output 120                |
| Fully connected+ReLU |                output 84                 |
|   Fully connected    |                output 43                 |



####4. Describe how you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.

- optimizer: tf.nn.softmax_cross_entropy_with_logits
- batch size: 128
- epochs: 30
- learning rate: 0.001

####5. Describe the approach taken for finding a solution. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

My solution is based on LeNet-5, which is a mature implementation for deep learning.

My final model results were:
* validation set accuracy of 0.932
* test set accuracy of 0.910

If a well known architecture was chosen:
* What architecture was chosen: LeNet-5
* Why did you believe it would be relevant to the traffic sign application: it is proven to be good at digits image recognition.
* How does the final model's accuracy on the training, validation and test set provide evidence that the model is working well?  The accuracy of over 0.9 is achieved in a few minutes with a local cpu. The accuracy can be improved by further fine tune the hyperparameter and faster gpu.


###Test a Model on New Images

####1. Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

I use 9 traffic signs from web. The difficulties come from following:

1. the background is not clean, e.g. road or tree. 
2. the training data set is still small and not complete. e.g., the speed limit of 40 is not even in the training set. 
3. the actual image may not have the sign in the center. 

####2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. Identify where in your code predictions were made. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).

The code for making predictions on my final model is located in the tenth cell of the Ipython notebook.

Here are the results of the prediction:

|                 Image                 |                Prediction                |
| :-----------------------------------: | :--------------------------------------: |
|           children crossing           |           Roundabout mandatory           |
|         Speed limit (60km/h)          |                no passing                |
|                 stop                  |                no passing                |
| Right-of-way at the next intersection |  Right-of-way at the next intersection   |
|               road work               |          Wild animals crossing           |
|         Speed limit (50km/h)          |           Speed limit (30km/h)           |
|               No entry                |                 No entry                 |
|                parking                | Vehicles over 3.5 metric tons prohibited |


The model was able to correctly guess 2 of the 9 traffic signs, which gives an accuracy of 22%. This is much worse than the accuracy on the test of "clean data".

####3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction and identify where in your code softmax probabilities were outputted. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

I don't know why my model shows above 96% confidence of the first prediction for all images. 




