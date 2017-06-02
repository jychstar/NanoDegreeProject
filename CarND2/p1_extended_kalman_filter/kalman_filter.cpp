#include "kalman_filter.h"
#include <iostream>
using Eigen::MatrixXd;
using Eigen::VectorXd;

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
    x_ = x_in;
    P_ = P_in;
    F_ = F_in;
    H_ = H_in;
    R_ = R_in;
    Q_ = Q_in;
}

void KalmanFilter::Predict() {
    x_ = F_ * x_;
    MatrixXd Ft = F_.transpose();
    P_ = F_ * P_ * Ft + Q_;
}

void KalmanFilter::Update(const VectorXd &z) {
    VectorXd z_pred = H_ * x_;
    VectorXd y = z - z_pred;
    MatrixXd Ht = H_.transpose();
    MatrixXd S = H_ * P_ * Ht + R_;
    MatrixXd Si = S.inverse();
    MatrixXd PHt = P_ * Ht;
    MatrixXd K = PHt * Si;

    //new estimate
    x_ = x_ + (K * y);
    long x_size = x_.size();
    MatrixXd I = MatrixXd::Identity(x_size, x_size);
    P_ = (I - K * H_) * P_;
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
    VectorXd z_pred(3);
    double px = x_(0),py = x_(1);
    double vx = x_(2),vy = x_(3);
    double r = sqrt( px*px + py*py);
    double rho =  atan(py/px);
    // get rho into the right Quadrant
    if (px<0 && py>0)
        rho += 3.1415926;
    if (px<0 && py<0)
        rho -= 3.1415926;
    // due to noise, rho may be 2*pi away from ground truth.
    if ( rho <-3 &&  z(1)>3 )
        rho += 3.1415926*2;
    if ( rho > 3 &&  z(1)< -3)
        rho -= 3.1415926*2;
    //std::cout <<"to polar: " << z_pred.transpose() <<"\n";
    //std::cout <<"truth polar: " <<  z.transpose() << "\n";}
    z_pred(0) = r;
    z_pred(1) = rho;
    z_pred(2) = (fabs(r) < 0.0001)? (px*vx + py*vy)/0.0001: (px*vx + py*vy)/r;

    VectorXd y = z - z_pred;
    MatrixXd Ht = H_.transpose();
    MatrixXd S = H_ * P_ * Ht + R_;
    MatrixXd Si = S.inverse();
    MatrixXd PHt = P_ * Ht;
    MatrixXd K = PHt * Si;

    //new estimate
    x_ = x_ + (K * y);
    long x_size = x_.size();
    MatrixXd I = MatrixXd::Identity(x_size, x_size);
    P_ = (I - K * H_) * P_;
}
