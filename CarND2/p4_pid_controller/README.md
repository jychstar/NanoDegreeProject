PID stands for proportional, integral, derivative. It is actually a combination of 3 feedback mechanisms. Each is at different time scale: immediate, one interval, accumulative. 

In Sebatian's course, a coded twiddle method was used to find the best parameters. However, similar codes can't be readily applied to the simulator due to the IO barrier. Instead, I manually tune the parameter. Here are my steps:

1. only use  the P parameter to get a rough number about the possible scale. In the course, PID parameter is [2.35,0, 1.893], which is not readily applicable due to different vehicle setting.
2. tune P and D simultaneously. The reason is that **a sharp steer will need a large roll back to avoid overshoot**.
3. After finding a good relationship of (P,D) pair, scale them up to see how large can they go without losing balance. 
4. Add a small I parameter to calibrate the system bias.

The manual tuning process is recorded in this table. Several local minimums have been highlighted.

| p        | i         | d       | step | error     | i-error |
| -------- | --------- | ------- | ---- | --------- | ------- |
| 0.1      | 0         | 0.03    | 1000 | 937       |         |
| 0.1      | 0         | 0.05    | 1000 | 777       |         |
| 0.1      | 0         | 0.1     | 1000 | 532       |         |
| **0.05** | 0         | **0.1** | 1780 | 5806      |         |
| 0.07     | 0         | 0.1     | 1000 | 1191      |         |
| 0.06     | 0         | 0.1     | 1000 | 1486      |         |
| 0.05     | 0         | 0.05    | 1780 | 6242      |         |
| 0.05     | 0         | 0.2     | 1860 | 6054      |         |
| 0.1      |           | 0.4     | 1760 | 5083      |         |
| 0.075    |           | 0.3     | 1440 | 4326      |         |
| **0.1**  |           | **0.6** | 3715 | 3729      |         |
| 0.15     |           | 1       | 3750 | 1721      |         |
| 0.2      |           | 1.5     | 3650 | 930       |         |
| **0.4**  |           | **3**   | 3860 | 640       |         |
| 0.8      |           | 6       | 3860 | 800       |         |
| 0.6      |           | 4.5     | 3860 | 3665      |         |
| 0.4      | 0.01      | 3       | 1700 | 657       |         |
| 0.4      |           | 4       | 4250 | 519       |         |
| 0.4      |           | 5       | 4250 | 524       | 663     |
| **0.4**  | **0.001** | **4**   | 4250 | **468.8** | 95      |
| 0.4      | 0.002     | 4       | 4240 | 483       | 47      |
| 0.5      | 0.001     | 5       | 4630 | 593       | 97      |
|          |           |         |      |           |         |

So my final parameter is PID = [**0.4,0.001,4**], which is good for throttle = 0.3.  I expect the PID parameter should be scale up if a larger throttle is used (means higher speed).