[TOC]

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position

[Rubric](https://review.udacity.com/#!/rubrics/571/view) 

# 1 Camera Calibration

## 1.1 Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is in section 1.2 of the IPython notebook.

The key is get objpoints-imgpoints pairs. The object points is the ground truth. For chessboard, these ordered 3D points can be easily created by 

```python
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8, 0:6].T.reshape(-1,2) 
```

The chessboard points are assumed to be fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  What pair with `objpoints` is  `imgpoints` , which are corners found by `cv2.findChessboardCorners(gray, (nx, ny))`.

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![](output_images/undistort.png)

We can see the distorted area happens around the edge, sometims it is so subtle that human eye may not notice it. 

## 1.2 perspective transform 

Perspective transform deals with the problem of **depth perception**. This is much important than distortion because the object farther away is less likely to be distorted.  For a good perspective transform, we need to **physically mark** 4 points in the lanelines that form a rectangle/parallelogram and how they appear in the camera image. 

Due to lack of experimental data, I tried my imagenation several times. It works but I not completely satisfied. I asked in the slack and no one answered. I asked my mentor Martijin. He seemed not understand my question and only gave me a link of his blog.

Luckily, the writeup template gives the  following source and destination points:

|  Source   | Destination |
| :-------: | :---------: |
| 585, 460  |   320, 0    |
| 203, 720  |  320, 720   |
| 1127, 720 |  960, 720   |
| 695, 460  |   960, 0    |

And it works pretty well:

![](output_images/perspective.png)

# 2 Pipeline (single images)

## 2.1 Provide an example of a distortion-corrected image.
To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![](output_images/undistort2.png)
## 2.2 thresholded binary image and perspective transform

As show in section 2 of my notebook, I have tried different gradients and channel:

1. sobelx gray
2. sobel magnitude
3. sobel angle
4. s-channel
5. soble l-channel
6. r-channel

It turns out the red-channel is good enough to do the job. Here's an example of my output for this step.  

![](output_images/r_binary.png)

## 2.3 Describe how you identified lane-line pixels and fit their positions with a polynomial?

Code implementaton in the section 3 of my notebook.

First, run a histogram to estimate the lane line position as the starting points.

![](output_images/histogram.png)

Then I used several windows to collect points on the lanelines. 

![](output_images/window_search.png)

With these points, I am able to fit parabolic curves and use the fitting coefficients as the starting points to more precisely search in the all subsequent images.

![](output_images/oriented_search.png)

## 2.4 Describe how you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

For the real-world curvature, the first thing is to make a connections between the pixel value and the physcial size. The use the rescaled pixels and equation to recalculate the fitting coefficient.

The off-center value is calcuated the difference of:

1. the car position is in the middle of the camera image
2. the lane center is in the middle of two lane lines

Then use `cv2.putText()` to write these information on image.

![](output_images/curvature.png)

## 2.5 Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

The code snippet is alread provided by the project instruction. The key thing is use   Minv to warp image back to the original perspecive. Here is an example of my result on a test image:

![](output_images/draw_lane.png)

## Pipeline (video)

Condense all the above code snippet together into a function called `pipeline`, then use the following code to produce a video:

```python
from moviepy.editor import VideoFileClip
output = 'project_output.mp4'
challenge_clip = VideoFileClip('project_video.mp4').fl_image(pipeline)
%time challenge_clip.write_videofile(output, audio=False)
```

Here's a [link to my video result on Youtube](https://youtu.be/xZK199K9jwk)

---

## Discussion

### Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I have played a trick in processing the image: put a mask area to fill out the undesirable background: sky, tress, other cars, etc. 

I know my model is not robust enough because I only use red-channel, which is somewhat sensitive to lightness.  To imporve the robustness, I will combine with other channels like s-channel and sobelx. And other paraterms such as margin, mask size may be also tuned. 

Actually, the most difficut thing is find the intial lane line centers, which may require a lot of manual exploration.

