#ifndef KALMAN_FILTER_H_
#define KALMAN_FILTER_H_
#include <Eigen/Dense>
using namespace Eigen;

class KalmanFilter {
public:

  VectorXd x_; // state vector
  MatrixXd P_; // state covariance matrix
  MatrixXd F_; // state transition matrix
  MatrixXd Q_; // process covariance matrix
  MatrixXd H_; // measurement matrix
  MatrixXd R_; // measurement covariance matrix

  KalmanFilter();

  virtual ~KalmanFilter();

  //Init Initializes Kalman filter
  void Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
      MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in);

  void Predict();

  void Update(const VectorXd &z); // standard Kalman Filter

  void UpdateEKF(const VectorXd &z); // Extended Kalman Filter

};

#endif /* KALMAN_FILTER_H_ */
