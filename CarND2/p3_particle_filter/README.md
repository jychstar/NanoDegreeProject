The project material can be found in https://github.com/udacity/CarND-Kidnapped-Vehicle-Project

This project is somewhat harder than I expect. Obviously, there's a gap between the course and the project:

1. course teaches a lot of posterior distribution, motion update, observation update. These has no direct application for the project.
2. particle filter is to generate **100 random points** at an approximate position (e.g. GPS location), and then use **lidar data** to see which point has the best overlap with the **landmarks**. This best point is used to represent the car position.

There are several tricks:

1. initializing the points use `normal_distribution` from algorithm library.
2. resample the points use `discrete_distribution`.
3. when prediction the particle positions, put `default_random_engine gen` before the for loop so the randomness continues.
4. if use for each loop, use `for (Particle &p: particles)` so you can change the original data not just the copied one. 
5. run time complexity of `updateWeights` are 100x8x42. For each observation of each particles, we  first loop through the 42 landmarks to see the best possible landmark for the observation, then calculate the probability. Weight is the continuous multiplication of these probability. 
6. In reality, this algorithm is not efficient. The question is: how many landmarks do you need in each scenario? Of course, this will require high resolution map as accurate as 0.1m. 