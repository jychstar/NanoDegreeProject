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