#ifndef FusionEKF_H_
#define FusionEKF_H_

#include "measurement_package.h"
#include <Eigen/Dense>
#include <vector>
#include <string>
#include <fstream>
#include "kalman_filter.h"
#include "tools.h"

class FusionEKF {
public:

  FusionEKF();
  virtual ~FusionEKF();
  void ProcessMeasurement(const MeasurementPackage &measurement_pack);
  KalmanFilter ekf_;

private:
  bool is_initialized_; // check whether it is first measurement
  long long previous_timestamp_;
  Tools tools;  // tool object used to compute Jacobian and RMSE
  Eigen::MatrixXd R_laser_;
  Eigen::MatrixXd R_radar_;
  Eigen::MatrixXd H_laser_;
  Eigen::MatrixXd Hj_;

    //set the acceleration noise components
  float noise_ax = 5;
  float noise_ay = 5;
};

#endif /* FusionEKF_H_ */
