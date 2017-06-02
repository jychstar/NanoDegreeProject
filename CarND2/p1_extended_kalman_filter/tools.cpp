#include <iostream>
#include "tools.h"

using Eigen::VectorXd;
using Eigen::MatrixXd;
using std::vector;

Tools::Tools() {}

Tools::~Tools() {}

VectorXd Tools::CalculateRMSE(const vector<VectorXd> &estimations,
                              const vector<VectorXd> &ground_truth) {
    VectorXd rmse = VectorXd::Zero(4); //initialize
    if(estimations.size() != ground_truth.size()
       || estimations.size() == 0){
        cout << "Invalid data" << endl;
        return rmse;
    }
    //accumulate squared residuals
    VectorXd residual(4);
    for(unsigned int i=0; i < estimations.size(); ++i){
        residual = estimations[i] - ground_truth[i];
        residual = residual.array()*residual.array();
        rmse += residual;
    }
    rmse = rmse/estimations.size(); //mean
    rmse = rmse.array().sqrt();  // square root
    return rmse;
}

MatrixXd Tools::CalculateJacobian(const VectorXd& x_state) {
    MatrixXd Hj(3,4); // set size
    double px = x_state(0), py = x_state(1);
    double vx = x_state(2), vy = x_state(3);
    double c1 = px*px+py*py;
    double c2 = sqrt(c1);
    double c3 = (c1*c2);
    //check division by zero
    if(fabs(c1) < 0.0001){ // c-styple abs only for int
        cout << "Error - Division by Zero" << endl;
        return Hj;
    }
    //compute the Jacobian matrix
    Hj << (px/c2), (py/c2), 0, 0,
            -(py/c1), (px/c1), 0, 0,
            py*(vx*py - vy*px)/c3, px*(px*vy - py*vx)/c3, px/c2, py/c2;
    return Hj;
}
