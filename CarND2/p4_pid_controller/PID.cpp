#include "PID.h"

//using namespace std;

/*
* TODO: Complete the PID class.
*/

PID::PID() {}

PID::~PID() {}

void PID::Init(double p, double i, double d) {
    Kp = p;
    Ki = i;
    Kd = d;
    p_error = 0;
    d_error = 0;
    i_error = 0;
    total_error = 0;
    count = 0;
}

void PID::UpdateError(double cte) {
    d_error = cte - p_error;
    p_error = cte;
    i_error += cte;
    total_error += cte * cte;
    count ++;
}

double PID::TotalError() {
    return p_error * p_error; // useless
}

