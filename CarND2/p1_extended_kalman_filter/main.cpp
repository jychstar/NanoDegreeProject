#include <uWS/uWS.h>
#include <iostream>
#include "json.hpp"
#include <math.h>
#include "FusionEKF.h"
#include "tools.h"

using namespace std;
using json = nlohmann::json;

// Checks if the SocketIO event has JSON data.
string hasData(string s) {
  if (s.find("null")!= string::npos)
    return "";
  // check JSON object in [] format
  auto b1 = s.find_first_of("[");
  auto b2 = s.find_first_of("]");
  if (b1 != string::npos && b2 != string::npos)
    return s.substr(b1, b2 - b1 + 1);
  return "";
}

int main() {
  uWS::Hub h;
  FusionEKF fusionEKF;
  // used to compute the RMSE later
  Tools tools;
  vector<VectorXd> estimations, ground_truth;

  h.onMessage([&fusionEKF, &tools, &estimations, &ground_truth]
                      (uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length, uWS::OpCode opCode) {
    // "42" at the start of the message means there's a websocket message event.
    // The 4 signifies a websocket message
    // The 2 signifies a websocket event

    if (length && length > 2 && data[0] == '4' && data[1] == '2') {
      string s = hasData(string(data));
      if (s != "") {
        auto j = json::parse(s);
        string event = j[0].get<string>();
        if (event == "telemetry") {
          // j[1] is the data JSON object
          string sensor_measurment = j[1]["sensor_measurement"];

          MeasurementPackage meas_package;
          istringstream iss(sensor_measurment);
    	  long long timestamp;
    	  // reads first element from the current line
    	  string sensor_type;
    	  iss >> sensor_type;

    	  if (sensor_type.compare("L") == 0) { // Laser data
      	  		meas_package.sensor_type_ = MeasurementPackage::LASER;
          		meas_package.raw_measurements_ = VectorXd(2);
          		double px,py;
          		iss >> px;
          		iss >> py;
                iss >> timestamp;
          		meas_package.raw_measurements_ << px, py;
          		meas_package.timestamp_ = timestamp;
          } else if (sensor_type.compare("R") == 0) {  // Radar data
      	  		meas_package.sensor_type_ = MeasurementPackage::RADAR;
          		meas_package.raw_measurements_ = VectorXd(3);
          		double ro, theta, ro_dot;
          		iss >> ro;
          		iss >> theta;
          		iss >> ro_dot;
                iss >> timestamp;
          		meas_package.raw_measurements_ << ro,theta, ro_dot;
          		meas_package.timestamp_ = timestamp;
          }
          // collect ground truth info
          double x_gt, y_gt;
    	  double vx_gt,vy_gt;
    	  iss >> x_gt;
    	  iss >> y_gt;
    	  iss >> vx_gt;
    	  iss >> vy_gt;
    	  VectorXd gt_values(4);
    	  gt_values << x_gt, y_gt,
                      vx_gt, vy_gt;
    	  ground_truth.push_back(gt_values);

          // use Kalman filter to update (x,p) and extract estimation
    	  fusionEKF.ProcessMeasurement(meas_package);
    	  double x = fusionEKF.ekf_.x_(0);
    	  double y = fusionEKF.ekf_.x_(1);
    	  double vx = fusionEKF.ekf_.x_(2);
    	  double vy = fusionEKF.ekf_.x_(3);
          VectorXd estimate(4);
    	  estimate << x, y, vx, vy;
    	  estimations.push_back(estimate);
          // calculate RMSE
    	  VectorXd RMSE = tools.CalculateRMSE(estimations, ground_truth);
          //  cout <<"truth: "<< gt_values.transpose() <<endl;
            cout << RMSE.transpose() <<endl;

          json msgJson;
          msgJson["estimate_x"] = x;
          msgJson["estimate_y"] = y;
          msgJson["rmse_x"] =  RMSE(0);
          msgJson["rmse_y"] =  RMSE(1);
          msgJson["rmse_vx"] = RMSE(2);
          msgJson["rmse_vy"] = RMSE(3);
          string msg = "42[\"estimate_marker\"," + msgJson.dump() + "]";
          ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
	  
        }
      } else {
        string msg = "42[\"manual\",{}]";
        ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
      }
    }

  }); // end h.onMessage

  // We don't use HTTP, this is only required for compilation
  h.onHttpRequest([](uWS::HttpResponse *res, uWS::HttpRequest req, char *data, size_t, size_t) {
    const string s = "<h1>Hello world!</h1>";
    if (req.getUrl().valueLength == 1)
      res->end(s.data(), s.length());
    else
      res->end(nullptr, 0);
  });

  h.onConnection([&h](uWS::WebSocket<uWS::SERVER> ws, uWS::HttpRequest req) {
    cout << "Connected!!!" << endl;
  });

  h.onDisconnection([&h](uWS::WebSocket<uWS::SERVER> ws, int code, char *message, size_t length) {
    ws.close();
    cout << "Disconnected" << endl;
  });

  int port = 4567;
  if (h.listen(port))
    cout << "Listening to port " << port << endl;
  else {
    cerr << "Failed to listen to port" << endl;
    return -1;
  }
  h.run();
} // end main