## Project: Kinematics Pick & Place

---
### Kinematic Analysis
#### 1. Run the forward_kinematics demo and evaluate the kr210.urdf.xacro file to perform kinematic analysis of Kuka KR210 robot and derive its DH parameters.

Ans: The schematics of the 6 joints looks like: 

![](https://d17h27t6h515a5.cloudfront.net/topher/2017/July/5975d719_fk/fk.png)

And the table is 

```python
DH_Table = {alpha0:      0, a0:      0, d1: 0.75, q1: q1,
            alpha1: -pi/2., a1:   0.35, d2:    0, q2: q2-pi/2,
            alpha2:      0, a2:   1.25, d3:    0, q3: q3,
            alpha3: -pi/2., a3: -0.054, d4:  1.5, q4: q4,
            alpha4:  pi/2., a4:      0, d5:    0, q5: q5,
            alpha5: -pi/2., a5:      0, d6:    0, q6: q6,
            alpha6:      0, a6:      0, d7: 0.303, q7: 0}
```

It is obtained by comparing the URDF file parameters and the target position for each joint.

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

The inverse transform from B to  A is:

![](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/594a9d61_inverse-homogeneous-tramsform/inverse-homogeneous-tramsform.png)

### Project Implementation

#### 1. Fill in the `IK_server.py` file with properly commented python code for calculating Inverse Kinematics based on previously performed Kinematic Analysis. Your code must guide the robot to successfully complete 8/10 pick and place cycles. Briefly discuss the code you implemented and your results. 


Honestly, I don't fully understand how the codes work and what cause the problem. It is really difficult to debug the errors for me. 





