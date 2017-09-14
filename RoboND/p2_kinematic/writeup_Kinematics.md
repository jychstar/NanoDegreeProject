## Project: Kinematics Pick & Place

---
[first review](https://review.udacity.com/#!/reviews/731583)

### Kinematic Analysis

#### 1. Run the forward_kinematics demo and evaluate the kr210.urdf.xacro file to perform kinematic analysis of Kuka KR210 robot and derive its DH parameters.

Ans: The schematics of the 6 joints looks like: 

![](https://d17h27t6h515a5.cloudfront.net/topher/2017/July/5975d719_fk/fk.png)

And the table is 

| Links | alpha(i-1) | a(i-1) | d(i-1) | theta(i)   |
| ----- | ---------- | ------ | ------ | ---------- |
| 0->1  | 0          | 0      | 0.75   | qi         |
| 1->2  | - pi/2     | 0.35   | 0      | -pi/2 + q2 |
| 2->3  | 0          | 1.25   | 0      | q3         |
| 3->4  | - pi/2     | -0.054 | 1.5    | q4         |
| 4->5  | pi/2       | 0      | 0      | q5         |
| 5->6  | -pi/2      | 0      | 0      | q6         |
| 6->EE | 0          | 0      | 0.303  | 0          |

kr210.urdf.xacro file shows the relative position between current joint and its parent joint. The choice of x-y-z axis for each frame follows the rules of minimizing the number of non-zero parameters. 

For example, the d value of joint 1 can be chosen to be 0.33 or other arbitrary number. But it is better to choose x1 axis to be intersected with next joint, which can reduce the number of non-zero parameters. As a result, D is chosen to be 0.75 for joint 1. 

#### 2. Using the DH parameter table you derived earlier, create individual transformation matrices about each joint. In addition, also generate a generalized homogeneous transform between base_link and gripper_link using only end-effector(gripper) pose.

Ans: Individual tranformation matrices for each joint using forward kinematics:

```python
def TF_Matrix(alpha,a,d,q):
    TF = Matrix([[cos(q), -sin(q), 0, a],
        [sin(q)*cos(alpha),cos(q)*cos(alpha),-sin(alpha),-sin(alpha)*d], 
        [sin(q)*sin(alpha),cos(q)*sin(alpha), cos(alpha), cos(alpha)*d],
                 [0, 0, 0,1]                  ])
    return TF
# create individual transformation matrices
T0_1 = TF_Matrix(alpha0, a0,d1,q1).subs(DH_Table)
T1_2 = TF_Matrix(alpha1, a1,d2,q2).subs(DH_Table)
T2_3 = TF_Matrix(alpha2, a2,d3,q3).subs(DH_Table)
T3_4 = TF_Matrix(alpha3, a3,d4,q4).subs(DH_Table)
T4_5 = TF_Matrix(alpha4, a4,d5,q5).subs(DH_Table)
T5_6 = TF_Matrix(alpha5, a5,d6,q6).subs(DH_Table)
T6_EE = TF_Matrix(alpha6,a6,d7,q7).subs(DH_Table)
```

An homogenous transform between based link and end-effector:

![](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/593c3bde_image2/image2.png)

#### 3. Decouple Inverse Kinematics problem into Inverse Position Kinematics and inverse Orientation Kinematics; doing so derive the equations to calculate all individual joint angles.

The designof spherical wrist **kinematically decouples the position and orientation** of the end effector. So the problem is divided into 2  basic steps.

1st, get the wrist center position in the base frame. The confusing thing here is that  $^6r_{EE/WC}$ is in the frame 6.  We intentional manipulate the frame EE so these two align (same orientation) and $^6r_{EE/WC}$ simply becomes (0, 0, -d).

$^0r_{EE/0} =[^0_6R,^0r_{WC/0}]\times[^6r_{EE/WC},1]^T=^0_6R\times ^6r_{EE/WC}+^0r_{WC/0} $

$\rightarrow ^0r_{WC/0} =^0r_{EE/0}-^0_6R\times ^6r_{EE/WC}=(px,py,pz)-d(r13,r23, r33) $

$^0r_{EE/0}$ is the position of end effector and $^0_6R$ can be directly calculated from the orientation of the end effector, i.e. euler angle (roll, pitch,yaw).

2nd,  calculate the angles of first 3 joints by the Wrist Center using cosine laws

<img src="https://d17h27t6h515a5.cloudfront.net/topher/2017/August/598dce04_l21-l-inverse-kinematics-new-design-fixed/l21-l-inverse-kinematics-new-design-fixed.png" alt="Smiley face" width="600">

With these 3 angles, calculate the $^0_3R$, then get $^3_6R$, the remaining angles can be calculated by the matrix element.

```python
R3_6 = R0_3.inv("LU") * ROT_EE
theta4 = atan2(R3_6[2,2], -R3_6[0,2])
theta5 = atan2(sqrt(R3_6[0,2]*R3_6[0,2] + 										R3_6[2,2]*R3_6[2,2]),R3_6[1,2])
theta6 = atan2(-R3_6[1,1],R3_6[1,0])
```

# 

### Project Implementation

#### 1. Fill in the `IK_server.py` file with properly commented python code for calculating Inverse Kinematics based on previously performed Kinematic Analysis. Your code must guide the robot to successfully complete 8/10 pick and place cycles. Briefly discuss the code you implemented and your results. 

logical flow in the code block:

1. A service "calculate_ik" is send to `handle_calculate_IK` function to process the request.
2. Within the function, create symbols and DH parameter dictionary for KR 210, define Transfomration matrix and call it for each joint, calculate the rotation maxtrix using position and orientation of the end effector.
3. For each poses of the end effector, calculate the wrist center and 6 angles using inverse kinematics, append them in to joint_trajectory_list. 

The code does work. But it runs very slow (I assign 6 G memory to VM on my Macbook pro 2012). The end-effctor seems to reach the object but not always grasp it firmly. The robot arm move to the trash can as the trajectory shows. 



