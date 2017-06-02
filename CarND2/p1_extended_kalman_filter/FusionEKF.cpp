#include "FusionEKF.h"
#include <iostream>

using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::vector;

FusionEKF::FusionEKF() {
    is_initialized_ = false;
    previous_timestamp_ = 0;

    //measurement covariance matrix
    R_laser_ = MatrixXd(2, 2);
    R_radar_ = MatrixXd(3, 3);
    R_laser_ << 0.0225, 0,
            0, 0.0225;
    R_radar_ << 0.09, 0, 0,
            0, 0.0009, 0,
            0, 0, 0.09;

    //create a 4D state vector, the initial value is unknown
    ekf_.x_ = VectorXd(4);

    //state covariance matrix P
    ekf_.P_ = MatrixXd(4, 4);
    ekf_.P_ << 1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1000, 0,
            0, 0, 0, 1000;

    //measurement matrix
    H_laser_ = MatrixXd(2, 4); // constant
    Hj_      = MatrixXd(3, 4);  // will change with state

    H_laser_ << 1, 0, 0, 0,
            0, 1, 0, 0;

    //the initial transition matrix F_
    ekf_.F_ = MatrixXd(4, 4);
    ekf_.F_ << 1, 0, 1, 0,
            0, 1, 0, 1,
            0, 0, 1, 0,
            0, 0, 0, 1;

    ekf_.Q_ = MatrixXd(4, 4); // process covariance matrix


}

FusionEKF::~FusionEKF() {}

void FusionEKF::ProcessMeasurement(const MeasurementPackage &measurement_pack) {
    /*****************************************************************************
     *  Initialization
     ****************************************************************************/
    if (!is_initialized_) {
        // first measurement
        cout << "Kalman Filter Initialization " << endl;
        if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR) {
            double ro    = measurement_pack.raw_measurements_(0);
            double theta = measurement_pack.raw_measurements_(1);
            ekf_.x_ << ro * cos(theta) , ro * sin(theta), 1, 1;
        }
        else if (measurement_pack.sensor_type_ == MeasurementPackage::LASER) {
            double x = measurement_pack.raw_measurements_(0);
            double y = measurement_pack.raw_measurements_(1);
            ekf_.x_ << x, y, 1, 1;
        }
        previous_timestamp_ = measurement_pack.timestamp_;
        is_initialized_ = true;
        return;
    }

    /*****************************************************************************
     *  Prediction
     ****************************************************************************/

    //compute the time elapsed between the current and previous measurements
    double dt = (measurement_pack.timestamp_ - previous_timestamp_) *1e-6;	// converted to seconds
    previous_timestamp_ = measurement_pack.timestamp_;
    double dt_2 = dt *dt;
    double dt_3 = dt_2 *dt;
    double dt_4 = dt_3 *dt;

    //Modify the F matrix
    ekf_.F_(0, 2) = dt;
    ekf_.F_(1, 3) = dt;

    //set the process covariance matrix Q
    ekf_.Q_ <<  dt_4/4*noise_ax, 0, dt_3/2*noise_ax, 0,
            0, dt_4/4*noise_ay, 0, dt_3/2*noise_ay,
            dt_3/2*noise_ax, 0, dt_2*noise_ax, 0,
            0, dt_3/2*noise_ay, 0, dt_2*noise_ay;

    ekf_.Predict();

    /*****************************************************************************
     *  Update
     ****************************************************************************/

    if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR){
        Hj_  = tools.CalculateJacobian(ekf_.x_);
        ekf_.H_ = Hj_;
        ekf_.R_ = R_radar_;
        ekf_.UpdateEKF(measurement_pack.raw_measurements_);  // Radar updates
    }

    else{
        ekf_.H_ = H_laser_;
        ekf_.R_ = R_laser_;
        ekf_.Update(measurement_pack.raw_measurements_); // Laser updates
    }

/*
    cout << "delta time = " << dt << endl;
    cout << "x_ = " << ekf_.x_ << endl;
    cout << "P_ = " << ekf_.P_.mean() << endl;
    cout << endl;
    */
}
