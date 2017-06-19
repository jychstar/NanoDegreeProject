#include <math.h>
#include <uWS/uWS.h>
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>
#include "Eigen-3.3/Eigen/Core"
#include "Eigen-3.3/Eigen/QR"
#include "MPC.h"
#include "json.hpp"

// for convenience
using json = nlohmann::json;

// For converting back and forth between radians and degrees.
constexpr double pi() { return M_PI; }

double deg2rad(double x) { return x * pi() / 180; }  // 25 degree equals 0.436 radian

double rad2deg(double x) { return x * 180 / pi(); }

// Checks if the SocketIO event has JSON data.
// If there is data the JSON object in string format will be returned,
// else the empty string "" will be returned.
string hasData(string s) {
    auto found_null = s.find("null");
    auto b1 = s.find_first_of("[");
    auto b2 = s.rfind("}]");
    if (found_null != string::npos) {
        return "";
    } else if (b1 != string::npos && b2 != string::npos) {
        return s.substr(b1, b2 - b1 + 2);
    }
    return "";
}

// Evaluate a polynomial.
double polyeval(Eigen::VectorXd coeffs, double x) {
    double result = 0.0;
    for (int i = 0; i < coeffs.size(); i++) {
        result += coeffs[i] * pow(x, i);
    }
    return result;
}

// Fit a polynomial.
// Adapted from
// https://github.com/JuliaMath/Polynomials.jl/blob/master/src/Polynomials.jl#L676-L716
Eigen::VectorXd polyfit(Eigen::VectorXd xvals, Eigen::VectorXd yvals,
                        int order) {
    assert(xvals.size() == yvals.size());
    assert(order >= 1 && order <= xvals.size() - 1);
    Eigen::MatrixXd A(xvals.size(), order + 1);

    for (int i = 0; i < xvals.size(); i++) {
        A(i, 0) = 1.0;
    }

    for (int j = 0; j < xvals.size(); j++) {
        for (int i = 0; i < order; i++) {
            A(j, i + 1) = A(j, i) * xvals(j);
        }
    }

    auto Q = A.householderQr();
    auto result = Q.solve(yvals);
    return result;
}

double getAngle(double x, double y){
    // x close to 0
    if (fabs(x)<1e-5) {
        if (y > 0)
            return 3.1415926/2;
        else
            return -3.1415926/2;
    }
    // y close to 0
    if (fabs(y)<1e-5){
        if (x>=0)
            return 0;
        else
            return 3.1415926;
    }
    double angle = atan(y/x);
    // check quadrant
    if (x<0 && y>0)
        angle += 3.1415926;
    if (x<0 && y<0)
        angle -= 3.1415926;
    return angle;
}

int main() {
    uWS::Hub h;

    // MPC is initialized here!
    MPC mpc;

    h.onMessage([&mpc](uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length,
                       uWS::OpCode opCode) {
        // "42" at the start of the message means there's a websocket message event.
        // The 4 signifies a websocket message
        // The 2 signifies a websocket event
        string sdata = string(data).substr(0, length);
        //cout << sdata << endl;
        if (sdata.size() > 2 && sdata[0] == '4' && sdata[1] == '2') {
            string s = hasData(sdata);
            if (s != "") {
                auto j = json::parse(s);
                string event = j[0].get<string>();
                if (event == "telemetry") {
                    // j[1] is the data JSON object
                    vector<double> ptsx = j[1]["ptsx"];
                    vector<double> ptsy = j[1]["ptsy"];
                    double px = j[1]["x"];
                    double py = j[1]["y"];
                    double psi = j[1]["psi"];
                    double v = j[1]["speed"];
                    // convert speed from mph to m/s.
                    v = v * 0.44704;
                    // convert from map perspective to car perspective
                    size_t num = ptsx.size();
                    Eigen::VectorXd carx(num), cary(num);
                    for (size_t i = 0; i < num; i++) {
                        carx[i] =  (ptsx[i] - px) * cos(psi) + (ptsy[i] - py) * sin(psi) ;
                        cary[i] = -(ptsx[i] - px) * sin(psi) + (ptsy[i] - py) * cos(psi) ;
                    }
                    //cout << carx.transpose() <<endl;
                    //cout << cary.transpose() <<endl;
                    // convert from map angle to car angle
                    double carpsi = 0;

                    auto coeffs = polyfit(carx, cary, 3);  // fit to the 3 order
                    //auto coeffs = polyfit(carx, cary, 1);  // fit to the 3 order

                    double x0 = 0, y0 = 0;
                    double slope = coeffs[1] + coeffs[2] * x0 * 2 +  coeffs[3] * x0 * x0 * 3;
                    //double slope = coeffs[1];
                    double psides0 = atan(slope);
                    cout << " ***** reference angle: " << psides0 << endl;

                    double cte = polyeval(coeffs, x0) - y0;
                    double epsi = (carpsi - psides0);
                    cout << "cte:" << cte <<endl;
                    cout << "epsi:" <<epsi <<endl;
                    cout <<"speed:" << v <<endl;

                    Eigen::VectorXd state(6);
                    state << x0, y0, 0, v, cte, epsi;
                    cout<< "-----------  using mpc solver: " << mpc.count <<endl;
                    vector<double> vars = mpc.Solve(state, coeffs);

                    double steer_value =  -vars[6];
                    double throttle_value = vars[7];

                    cout <<"steer:" << steer_value <<endl;
                    cout <<"throttle:" << throttle_value <<endl;

                    json msgJson;
                    // NOTE: Remember to divide by deg2rad(25) before you send the steering value back.
                    // Otherwise the values will be in between [-deg2rad(25), deg2rad(25] instead of [-1, 1].
                    msgJson["steering_angle"] = steer_value;// m/s to mph /deg2rad(25);
                    msgJson["throttle"] = throttle_value;

                    //Display the MPC predicted trajectory
                    vector<double> mpc_x_vals ;
                    vector<double> mpc_y_vals ;
                    //mpc_x_vals.push_back(vars[0]);
                    //mpc_y_vals.push_back(vars[1]);
                    mpc_x_vals = mpc.x_vals;
                    mpc_y_vals = mpc.y_vals;

                    //.. add (x,y) points to list here, points are in reference to the vehicle's coordinate system
                    // the points in the simulator are connected by a Green line

                    msgJson["mpc_x"] = mpc_x_vals;
                    msgJson["mpc_y"] = mpc_y_vals;

                    //Display the waypoints/reference line
                    vector<double> next_x_vals;
                    vector<double> next_y_vals;
                    for (size_t i = 0; i < num; i++){
                        next_x_vals.push_back(carx[i]);
                        next_y_vals.push_back(cary[i]);
                    }

                    //.. add (x,y) points to list here, points are in reference to the vehicle's coordinate system
                    // the points in the simulator are connected by a Yellow line

                    msgJson["next_x"] = next_x_vals;
                    msgJson["next_y"] = next_y_vals;


                    auto msg = "42[\"steer\"," + msgJson.dump() + "]";
                    //std::cout << msg << std::endl;
                    // Latency
                    // The purpose is to mimic real driving conditions where
                    // the car does actuate the commands instantly.
                    //
                    // Feel free to play around with this value but should be to drive
                    // around the track with 100ms latency.
                    //
                    // NOTE: REMEMBER TO SET THIS TO 100 MILLISECONDS BEFORE
                    // SUBMITTING.
                    this_thread::sleep_for(chrono::milliseconds(100));
                    ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
                }
            } else {
                // Manual driving
                std::string msg = "42[\"manual\",{}]";
                ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
            }
        }
    });

    // We don't need this since we're not using HTTP but if it's removed the
    // program
    // doesn't compile :-(
    h.onHttpRequest([](uWS::HttpResponse *res, uWS::HttpRequest req, char *data,
                       size_t, size_t) {
        const std::string s = "<h1>Hello world!</h1>";
        if (req.getUrl().valueLength == 1) {
            res->end(s.data(), s.length());
        } else {
            // i guess this should be done more gracefully?
            res->end(nullptr, 0);
        }
    });

    h.onConnection([&h](uWS::WebSocket<uWS::SERVER> ws, uWS::HttpRequest req) {
        std::cout << "Connected!!!" << std::endl;
    });

    h.onDisconnection([&h](uWS::WebSocket<uWS::SERVER> ws, int code,
                           char *message, size_t length) {
        ws.close();
        std::cout << "Disconnected" << std::endl;
    });

    int port = 4567;
    if (h.listen(port)) {
        std::cout << "Listening to port " << port << std::endl;
    } else {
        std::cerr << "Failed to listen to port" << std::endl;
        return -1;
    }
    h.run();
}
