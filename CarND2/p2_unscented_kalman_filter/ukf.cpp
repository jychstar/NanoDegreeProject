#include "ukf.h"
#include "Eigen/Dense"
#include <iostream>

using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::vector;

/**
 * Initializes Unscented Kalman filter
 */
UKF::UKF() {
    is_initialized_ = false;
    time_us_ = 0;
    // if this is false, laser measurements will be ignored (except during init)
    use_laser_ = false;

    // if this is false, radar measurements will be ignored (except during init)
    use_radar_ = false;

    // Process noise standard deviation longitudinal acceleration in m/s^2
    std_a_ = 1;

    // Process noise standard deviation yaw acceleration in rad/s^2
    std_yawdd_ = 3;

    // Laser measurement noise standard deviation position1 in m
    std_laspx_ = 0.15;

    // Laser measurement noise standard deviation position2 in m
    std_laspy_ = 0.15;

    // Radar measurement noise standard deviation radius in m
    std_radr_ = 0.3;

    // Radar measurement noise standard deviation angle in rad
    std_radphi_ = 0.03;

    // Radar measurement noise standard deviation radius change in m/s
    std_radrd_ = 0.3;

    n_x_ = 5;
    n_aug_ = 7;
    x_ = VectorXd(n_x_ );
    P_ = MatrixXd(n_x_ , n_x_ );
    P_.setIdentity();

    Xsig_pred_ = MatrixXd(n_x_, 2 * n_aug_ + 1);
    lambda_ = 3 - n_aug_;
    // initialize weight
    weights_ = VectorXd(2*n_aug_+1);
    double weight_0 = lambda_/(lambda_+n_aug_);
    weights_(0) = weight_0;
    for (int i=1; i<2*n_aug_+1; i++) {  //2n+1 weights
        double weight = 0.5/(n_aug_+lambda_);
        weights_(i) = weight;
    }

}

UKF::~UKF() {}
/**
 * @param {MeasurementPackage} meas_package The latest measurement data of
 * either radar or laser.
 */
void UKF::ProcessMeasurement(MeasurementPackage meas_package) {
    /*****************************************************************************
     *  Initialization
     ****************************************************************************/
    if (!is_initialized_) {
        cout <<"initializing..."<<endl;
        if (meas_package.sensor_type_ == MeasurementPackage::RADAR) {
            double ro    = meas_package.raw_measurements_(0);
            double theta = meas_package.raw_measurements_(1);
            double ro_dot= meas_package.raw_measurements_(2);

            x_ << ro * cos(theta) , ro * sin(theta), ro_dot, 0,0;
        }
        else if (meas_package.sensor_type_ == MeasurementPackage::LASER) {
            double x = meas_package.raw_measurements_(0);
            double y = meas_package.raw_measurements_(1);
            x_ << x, y, 0, 0,0;
        }
        time_us_ = meas_package.timestamp_;
        is_initialized_ = true;
        return;
    }
    double dt = (meas_package.timestamp_ - time_us_) *1e-6;	// converted to seconds
    time_us_ = meas_package.timestamp_;
    if (meas_package.sensor_type_ == MeasurementPackage::RADAR)
        use_radar_ = true;
    if (meas_package.sensor_type_ == MeasurementPackage::LASER)
        use_laser_ = true;

    Prediction(dt);

    if (use_radar_ ){
        UpdateRadar(meas_package); // Radar updates
        use_radar_ = false;
    }
    if (use_laser_ ){
        UpdateLidar(meas_package); // Laser updates
        use_laser_ = false;
    }
    /*
     cout << "delta time = " << dt << endl;
     cout << "x_ = " << ekf_.x_ << endl;
     cout << "P_ = " << ekf_.P_ << endl;
     cout << endl;
     */
}

/**
 * Predicts sigma points, the state, and the state covariance matrix.
 * @param {double} delta_t the change in time (in seconds) between the last
 * measurement and this one.
 */
void UKF::Prediction(double delta_t) {
    //cout << "prediciton" <<endl;
    MatrixXd Xsig = MatrixXd(n_x_, 2 * n_x_ + 1);
    MatrixXd A = P_.llt().matrixL();
    Xsig.col(0)  = x_;
    for (int i = 0; i < n_x_; i++){
        Xsig.col(i+1)      = x_ + sqrt(lambda_+n_x_) * A.col(i);
        Xsig.col(i+1+n_x_) = x_ - sqrt(lambda_+n_x_) * A.col(i);
    }
    // augmentation state and covariance
    VectorXd x_aug = VectorXd(n_aug_);
    MatrixXd P_aug = MatrixXd(n_aug_, n_aug_);
    MatrixXd Xsig_aug = MatrixXd(n_aug_, 2 * n_aug_ + 1);
    x_aug.head(5) = x_;
    x_aug(5) = 0;
    x_aug(6) = 0;
    P_aug.fill(0.0);
    P_aug.topLeftCorner(5,5) = P_;
    P_aug(5,5) = std_a_*std_a_;
    P_aug(6,6) = std_yawdd_*std_yawdd_;
    MatrixXd L = P_aug.llt().matrixL();
    Xsig_aug.col(0)  = x_aug;
    double factor = sqrt(lambda_+n_aug_);
    for (int i = 0; i< n_aug_; i++){
        Xsig_aug.col(i+1)= x_aug + factor * L.col(i);
        Xsig_aug.col(i+1+n_aug_) = x_aug - factor * L.col(i);
    }

    // apply time effect for each column
    for (int i = 0; i< 2*n_aug_+1; i++){
        //extract values for better readability
        double p_x = Xsig_aug(0,i);
        double p_y = Xsig_aug(1,i);
        double v = Xsig_aug(2,i);
        double yaw = Xsig_aug(3,i);
        double yawd = Xsig_aug(4,i);
        double nu_a = Xsig_aug(5,i);
        double nu_yawdd = Xsig_aug(6,i);
        double px_p, py_p;  //predicted state positions
        //avoid division by zero
        if (fabs(yawd) > 0.001) {
            px_p = p_x + v/yawd * ( sin (yaw + yawd*delta_t) - sin(yaw));
            py_p = p_y + v/yawd * ( cos(yaw) - cos(yaw+yawd*delta_t) );
        }
        else {
            px_p = p_x + v*delta_t*cos(yaw);
            py_p = p_y + v*delta_t*sin(yaw);
        }
        double v_p = v; // constant velocity magnitude
        double yaw_p = yaw + yawd*delta_t;
        double yawd_p = yawd;  // constant turn rate
        //add noise
        px_p = px_p + 0.5*nu_a*delta_t*delta_t * cos(yaw);
        py_p = py_p + 0.5*nu_a*delta_t*delta_t * sin(yaw);
        v_p = v_p + nu_a*delta_t;
        yaw_p = yaw_p + 0.5*nu_yawdd*delta_t*delta_t;
        yawd_p = yawd_p + nu_yawdd*delta_t;
        //write predicted sigma point into right column
        Xsig_pred_(0,i) = px_p;
        Xsig_pred_(1,i) = py_p;
        Xsig_pred_(2,i) = v_p;
        Xsig_pred_(3,i) = yaw_p;
        Xsig_pred_(4,i) = yawd_p;
    }

    // update state x and covariance P
    //predicted state mean
    x_.fill(0.0);
    for (int i = 0; i < 2 * n_aug_ + 1; i++) {  //iterate over sigma points
        x_ = x_+ weights_(i) * Xsig_pred_.col(i);
    }

    //predicted state covariance matrix
    P_.fill(0.0);
    for (int i = 0; i < 2 * n_aug_ + 1; i++) {  //iterate over sigma points
        // state difference
        VectorXd x_diff = Xsig_pred_.col(i) - x_;
        //angle normalization
        while (x_diff(3)> M_PI)
            x_diff(3)-=2.*M_PI;
        while (x_diff(3)<-M_PI)
            x_diff(3)+=2.*M_PI;
        P_ = P_ + weights_(i) * x_diff * x_diff.transpose();
    }

}

/**
 * Updates the state and the state covariance matrix using a laser measurement.
 * @param {MeasurementPackage} meas_package
 */
void UKF::UpdateLidar(MeasurementPackage meas_package) {
    VectorXd z = meas_package.raw_measurements_; // incoming lidar measurement
    MatrixXd H_ = MatrixXd(2, 5); // constant
    H_ << 1, 0, 0, 0, 0,
          0, 1, 0, 0, 0;
    MatrixXd R_ = MatrixXd(2, 2);
    R_ << std_laspx_*std_laspx_, 0,
                0, std_laspy_*std_laspy_;
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

/**
 * Updates the state and the state covariance matrix using a radar measurement.
 * @param {MeasurementPackage} meas_package
 */
void UKF::UpdateRadar(MeasurementPackage meas_package) {
    // get covariance matrix S
    int n_z = 3;
    MatrixXd Zsig = MatrixXd(n_z, 2 * n_aug_ + 1);
    for (int i = 0; i < 2 * n_aug_ + 1; i++) {  //2n+1 simga points
        // extract values for better readibility
        double p_x = Xsig_pred_(0,i);
        double p_y = Xsig_pred_(1,i);
        double v  = Xsig_pred_(2,i);
        double yaw = Xsig_pred_(3,i);
        double v1 = cos(yaw)*v;
        double v2 = sin(yaw)*v;
        // measurement model
        Zsig(0,i) = sqrt(p_x*p_x + p_y*p_y);   //r
        Zsig(1,i) = atan2(p_y,p_x);   //phi
        Zsig(2,i) = (p_x*v1 + p_y*v2 ) / sqrt(p_x*p_x + p_y*p_y);   //r_dot
    }
    //mean predicted measurement
    VectorXd z_pred = VectorXd(n_z);
    z_pred.fill(0.0);
    for (int i=0; i < 2*n_aug_+1; i++) {
        z_pred = z_pred + weights_(i) * Zsig.col(i);
    }
    //measurement covariance matrix S
    MatrixXd S = MatrixXd(n_z,n_z);
    S.fill(0.0);
    for (int i = 0; i < 2 * n_aug_ + 1; i++) {  //2n+1 simga points
        //residual
        VectorXd z_diff = Zsig.col(i) - z_pred;
        //angle normalization
        while (z_diff(1)> M_PI) z_diff(1)-=2.*M_PI;
        while (z_diff(1)<-M_PI) z_diff(1)+=2.*M_PI;
        S = S + weights_(i) * z_diff * z_diff.transpose();
    }
    //add measurement noise covariance matrix
    MatrixXd R = MatrixXd(n_z,n_z);
    R <<    std_radr_ * std_radr_, 0, 0,
            0, std_radphi_*std_radphi_, 0,
            0, 0,std_radrd_*std_radrd_;
    S = S + R;

    // incoming radar measurement
    VectorXd z = meas_package.raw_measurements_;

    //create matrix for cross correlation Tc
    MatrixXd Tc = MatrixXd(n_x_, n_z);
    Tc.fill(0.0);
    for (int i = 0; i < 2 * n_aug_ + 1; i++) {  //2n+1 simga points
        //residual
        VectorXd z_diff = Zsig.col(i) - z_pred;
        //angle normalization
        while (z_diff(1)> M_PI) z_diff(1)-=2.*M_PI;
        while (z_diff(1)<-M_PI) z_diff(1)+=2.*M_PI;
        // state difference
        VectorXd x_diff = Xsig_pred_.col(i) - x_;
        //angle normalization
        while (x_diff(3)> M_PI) x_diff(3)-=2.*M_PI;
        while (x_diff(3)<-M_PI) x_diff(3)+=2.*M_PI;
        Tc = Tc + weights_(i) * x_diff * z_diff.transpose();
    }
    //Kalman gain K;
    MatrixXd K = Tc * S.inverse();
    //residual
    VectorXd z_diff = z - z_pred;

    //angle normalization
    while (z_diff(1)> M_PI) z_diff(1)-=2.*M_PI;
    while (z_diff(1)<-M_PI) z_diff(1)+=2.*M_PI;
    //update state mean and covariance matrix
    x_ = x_ + K * z_diff;
    P_ = P_ - K*S*K.transpose();
}
