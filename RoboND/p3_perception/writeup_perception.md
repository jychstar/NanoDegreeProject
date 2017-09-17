#Project: Perception Pick & Place
Rubric:https://review.udacity.com/#!/rubrics/1067/view

# Exercise 1, 2 and 3 pipeline implemented
## 1. Complete Exercise 1 steps. Pipeline for filtering and RANSAC plane fitting implemented.

input: `pcl.load_XYZRGB('tabletop.pcd')`

output: `pcl.save(cloud_new,"xx.pcd")`, `pcl_viewer xx.pcd`

Most commonly used filters from the Point Cloud Library:

- VoxelGrid Downsampling Filter
- ExtractIndices Filter
- PassThrough Filter
- RANSAC Plane Fitting: Random Sample Consensus. estimate what pieces of the point cloud set belong to that shape by assuming a particular model, such as a **plane**.The number of iterations is a **trade-off between compuer time vs. model detection accuracy**. 
- Outlier Removal Filter

Basic operations for pcd are implemented in `RANSAC.py`:

## 2. Complete Exercise 2 steps: Pipeline including clustering for segmentation implemented.  

input: camera data from a ROS node by subscribing to a topic called `/sensor_stick/point_cloud`.

output: after point cloud is segmented by Euclidean clustering, publish data back to topics called `/pcl_table` and `/pcl_objects

code is implemented in `segmentation.py`. There are 2 main things:

1. subscriber/publisher to new topic.
2. use Euclidean Clustering to segment individual objects.

##3. Complete Exercise 3 Steps.  Features extracted and SVM trained.  Object recognition implemented.

input: cloud data from ROS

output: clustered cloud with recognized label 

Possible Features for identifying an object:

1. object color and shape
2. detailed color information
3. detailed shape information

### data generation: `capture_feature.py`

1. use spawn_model() and capture_sample() from `sensor_stick/training_helper.py` to generate ROS PointCloud2.
2. ROS PointCloud2 data will be parsed by `pc2.read_points`.use compute_color_histograms() and compute_normal_histograms() from `sensor_stick/features.py` to divide each color channel and each normal direction into 32 bins, so the total features are 192. The exact number of RGB_D points are not important, because histogram measures the distribution of values, or the relative number.
3. concantenate 192 features into one sample. There are 7 classes, each is repeated 5 times, so the total training set is (35,192). 
4. `pickle.dump(labeled_features, open('training_set.sav', 'wb'))`

improve `features.py` :

- in the `for` loop that begins with `for i in range(5):`. Increase this value to increase the number of times you capture features for each object.
- To use HSV, find the line in `capture_features.py` where you're calling `compute_color_histograms()` and change the flag to `using_hsv=True`.
- try different binning schemes.

### machine learning: `train_svm.py` 

- `training_set = pickle.load(open('training_set.sav', 'rb'))`
- preprocess: StandardScaler() for X, LabelEncoder for y, 
- KFold cross validation for score, plot confusion marix
- use whole data to train again and get the final model
- `model = {'classifier': clf, 'classes': encoder.classes_, 'scaler': X_scaler}`
- `pickle.dump to 'model.sav'`
- If you get the 192 features and want to make a prediction, first you need to reformat the data with 3 operations : `X_test = X_scaler.transform(np.array(features).reshape(1,192))`, then you can `clf.predict(X_test)`

### put them all together

```shell
$ cd ~/catkin_ws/src/sensor_stick/scripts/
$ cp template.py object_recognition.py
# finish all TO-DO
$ roslaunch sensor_stick robot_spawn.launch
$ chmod +x object_recognition.py
$ ./object_recognition.py
```

#Pick and Place Setup

##1. For all three tabletop setups (`test*.world`), perform object recognition, then read in respective pick list (`pick_list_*.yaml`). Next construct the messages that would comprise a valid `PickPlace` request output them to `.yaml` format.

Spend some time at the end to discuss your code, what techniques you used, what worked and why, where the implementation might fail and how you might improve it if you were going to pursue this project further.  

`pcl_callback(pcl_msg)` is a collection of previous 3 exercises.

in `pr2_mover(object_list)` function, there are 3 baisic steps:

1. loop through object_list, put relevant information into a dictionary for label-centroid pair.
2. loop through the dropbox parameter obtained from the topic `/dropbox`, build 2 dicitonaries for group-name and group-position pair.
3. loop through the pick_list parameter obtained from the topic `/object_list`, compare with the label dictionary to see whether the object has been found. If it is found, prepare data in message type, send data into `make_yaml_dict` and server.

Remaining issue: 

- for `pick_place_routine` Service, I use `resp = pick_place_routine(test_scene_num, arm_name, object_name, pick_pose, place_pose)`, I got `('Response:',False)`. I don't know what goes wrong.

How to improve:

- generate more model cloud point data to build better classifier
- add collision avoidance

