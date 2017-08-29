This writeup is to address each rubric point  to meet specifications of the "search and sample return" project.

https://review.udacity.com/#!/rubrics/916/view

## Notebook Analysis

### 1. Describe how you modified/added functions to add obstacle and rock sample identification.

In the perception step,  color thresholding is used for environment segmentation. The high value pixels ( RGB> 160) are labelled as ground, the low value pixels (RGB<=160) are labelled as obstacle. Due to perspective transform, only certain area has meaningful value. So a mask is used to filter out the undesirable area.

`find_rocks` function set the high value threshold for red and greeen channel (RG>110) and low value threshold for blue channel (B<50). This is because the rock in current setting is usually yellow.

### 2. Describe how you created a world map 

There are several steps:

1. persepctive transform to get a top-down view
2. convert from (y,x) matrix representation to robot-centered (x,y) coordinates
3. use rover's own state (x,y, yaw) and scale to convert image into a focus map
4. overlap the small map to an existing large map,
5. keep updating in each frame

## Autonomous Navigation and Mapping

### 1. fill `perception_step()` and `decision_step()` functions and explain 

perception_step() is to segment image into 3 categories (navigatable land, obstacle, rock) using color channel threshold.

decision_step() is rule-based artificial intelligence. The environment is very simple, so the rover choose an more open area to move and pick sample if it is near.

### 2. run `drive_rover.py` and how you might improve

simulator setting: 

- resolution:  600x800
- graphics quality: fastest
- FPS output: 39


how to improve:

1. when the rock shows up in the image, caluclate the rock's position and move the rover nearby to pick it up.
2. record the rover's inital position, do a path planning to return
3. record explored area so the rover is more efficient to find new rocks.