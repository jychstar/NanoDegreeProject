walk-through video: https://www.youtube.com/watch?v=bOQuhpz3YfU

There are 3 major difficulties in this projects.

## 1 Understand how to use Ipopt solver to optimize MPC parameters

The MPC quize is great. However, I didn't fully understand it until I do the project. In fact, I wasted several hours in tuning parameters and get wired results.  It turns out that I missed a piece of code that sets the constraints bound, which caused pretty small speed. 

Visualizing the waypoints and prediction are very helpful.

## 2 Data Wrangling, coordinate transform 

The coordiante transform took me a while. Several tricks:

- the server returns waypoints using the map's coordinate system, which is different than the car's coordinate system. Transforming these waypoints will make it easier to both display them and to calculate the CTE and Epsi values for the model predictive controller.
- The `mpc_x` and `mpc_y` variables display a line projection in green. The `next_x` and `next_y` variables display a line projection in yellow. These (x,y) points are displayed in reference to the **vehicle's coordinate system**. The car's heading is always x axis with $\psi=0$. So points (0,0) and (10,0) will draw a straight line right from car's head. 
- For actuators,  steer =0.1 means turn right 0.1 radian, which is in opposite direction with math notation. Positive throttle means forward, the same with convection.
- Note that `ptsy` is up-down direction.

From local point (xl,yl) based on the sight of (x0,y0, theta) to global (xg,yg), the transformation is 
$x_g = x_0 + x_l *cos(\theta) - y_l*sin(\theta)$

$y_g = y_0 + x_l *sin(\theta) + y_l*cos(\theta)$

So the inverse conversion is:

$x_l = (x_g-x_0)*cos(\theta)+(y_g-y_0)*sin(\theta)$

$y_l = -(x_g-x_0)*sin(\theta)+(y_g-y_0)*cos(\theta)$

## 3 Tune MPC hyperparameters

While PID method is basically tuning the 3 parameters, MPC automatically find the optimal parameters using a ipopt solver. However, to apply the solver, we have to correctly implement the cost function, which is actually a combination of 7 cost functions. These values have different orders of magnitude:cross track error:  0.5

- epsi: 0.1
- speed limit: 10
- steer: 0.1
- accelerate: 1
- steer change: 0.01
- accelerate change: 1

 We will have to apply large factor to stand out the small but important errors. 

| cte  | epsi | v-20 | psi   | acc  | d-spi | D-Acc | note           | steps  |
| ---- | ---- | ---- | ----- | ---- | ----- | ----- | -------------- | ------ |
| 1    | 1    | 1    | 1     | 1    | 1     | 1     | zigzag         | 27     |
| 1    | 100  | 1    | 1     | 1    | 1     | 1     | zigzag         |        |
| 100  | 1000 | 1    | 10000 | 50   | 2000  | 10    | zigzag         | 225    |
| 100  | 1000 | 1    | 10000 | 50   | 2000  | 10    | zigzag         | 229    |
| 100  | 1000 | 1    | 10000 | 50   | 4000  | 10    | zigzag         | 233    |
| 100  | 1000 | 1    | 10000 | 50   | 10000 | 10    | zigzag         | 233    |
| 100  | 1000 | 1    | 10000 | 50   | 10000 | 10    | zigzag         | 233    |
| 1000 | 1000 | 1    | 10000 | 50   | 10000 | 10    | zigzag         | 33     |
| 10   | 100  | 1    | 2000  | 5    | 1000  | 1     | inadeque steer | 180    |
| 10   | 1000 | 1    | 2000  | 5    | 2000  | 20    | slow rebound   | 217    |
| 100  | 1000 | 1    | 2000  | 10   | 4000  | 20    | zigzag         | 42     |
| 10   | 2000 | 1    | 1000  | 10   | 1000  | 20    | N=50           | 1 lap  |
| 10   | 2000 | 1    | 500   | 10   | 1000  | 20    | inadeque steer | 234    |
| 10   | 4000 | 1    | 100   | 10   | 2000  | 20    | zigzag         | 262    |
| 20   | 4000 | 1    | 100   | 10   | 4000  | 20    | N=30           | 2 laps |
| 2    | 400  | 1    | 10    | 1    | 400   | 2     |                | 2 laps |
| 3    | 400  | 1    | 10    | 1    | 500   | 2     |                | OK     |
| 3    | 300  | 1    | 5     | 1    | 500   | 2     |                | OK     |
| 3    | 300  | 1    | 5     | 1    | 1000  | 1     |                | Great  |

Notes:

- walk-through video uses (2000, 2000,1,5,5,200,10). Time scope is 0.1s *10 = 1 s
- MPC quiz use dt = 0.05s, N= 25. Time scope is 1.25s
- I tried 0.1s* 50 = 5s. But actually the last 2 seconds have no groundtruth data.
- Mostly I tuned in the time scope 0.1s *30 = 3s and speed = 20 m/s.  The parameter need to be modified if higher speed is used. 

## slack

vivek Yadav suggest a trick to slow down based on the curvature

```c++
double vel;
double V_lw = 45;
double V_up = 125;
double R_up = 60;
double R_dn = 30;
if (R_curve<R_dn)
  vel = V_lw;
else if (R_curve<R_up)
    vel = V_lw+(V_up-V_lw)*(R_curve-R_dn)/(R_up-R_dn);
else
    vel = V_up;
```

