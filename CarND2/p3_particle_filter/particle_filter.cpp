/*
 * particle_filter.cpp
 *
 *  Created on: Dec 12, 2016
 *      Author: Tiffany Huang
 */

#include <random>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <math.h> 
#include <iostream>
#include <sstream>
#include <string>
#include <iterator>
#include "map.h"
#include "particle_filter.h"
using namespace std;

void ParticleFilter::init(double x, double y, double theta, double std[]) {
	// TODO: Set the number of particles. Initialize all particles to first position (based on estimates of 
	//   x, y, theta and their uncertainties from GPS) and all weights to 1. 
	// Add random Gaussian noise to each particle.
	num_particles = 100;
	is_initialized = true;
	default_random_engine gen;
	normal_distribution<double> dist_x(x, std[0]);
	normal_distribution<double> dist_y(y, std[1]);
	normal_distribution<double> dist_psi(theta, std[2]);
	for (int i=0; i < num_particles; i++){
		Particle p;
		p.id = i;
		p.x = dist_x(gen);
		p.y = dist_y(gen);
		p.theta = dist_psi(gen);
		p.weight = 0;  // should not be 1
		particles.push_back(p);
		weights.push_back(1);  // for resample
	}
	cout <<"initialized:"
         <<x<<","
         <<y<<","
         <<theta<<endl;
}

void ParticleFilter::prediction(double delta_t, double std_pos[], double velocity, double yaw_rate) {
	// TODO: Add measurements to each particle and add random Gaussian noise.
	// NOTE: When adding noise you may find std::normal_distribution and std::default_random_engine useful.
	//  http://en.cppreference.com/w/cpp/numeric/random/normal_distribution
	//  http://www.cplusplus.com/reference/random/default_random_engine/
    double x, y, theta;
    //cout << "delta_t:"<<delta_t<<"veloctiy:"<<velocity <<",yaw_rate:" <<yaw_rate<<endl ;
    //yaw_rate = yaw_rate/180.0 * M_PI;
    default_random_engine gen;
	for (Particle &p: particles){
		if (fabs(yaw_rate) > 0.001) {
            //cout << "px:" <<p.x <<",py:" <<p.y <<endl;
            x = p.x + velocity/yaw_rate * ( sin(p.theta + yaw_rate * delta_t) - sin(p.theta));
			y = p.y + velocity/yaw_rate * ( cos(p.theta) - cos(p.theta + yaw_rate * delta_t));
            //cout << "x:" <<x <<",y:" <<y <<endl;
		}
		else {
			x = p.x + velocity * delta_t * cos(p.theta);
			y = p.y + velocity * delta_t * sin(p.theta);
		}
		theta = p.theta + yaw_rate * delta_t;
        //while (theta> 2*M_PI) theta -= 2*M_PI;
        //while (theta< -2*M_PI) theta += 2*M_PI;
		normal_distribution<double> dist_x(x, std_pos[0]);  //0.03
		normal_distribution<double> dist_y(y, std_pos[1]);  //0.03
		normal_distribution<double> dist_psi(theta, std_pos[2]); //0.01
		p.x = dist_x(gen);
		p.y = dist_y(gen);
		p.theta = dist_psi(gen);
	}
}

void ParticleFilter::dataAssociation(std::vector<LandmarkObs> predicted, std::vector<LandmarkObs>& observations) {
	// TODO: Find the predicted measurement that is closest to each observed measurement and assign the 
	//   observed measurement to this particular landmark.
	// NOTE: this method will NOT be called by the grading code. But you will probably find it useful to 
	//   implement this method and use it as a helper during the updateWeights phase.

}

void ParticleFilter::updateWeights(double sensor_range, double std_landmark[], 
		std::vector<LandmarkObs> observations, Map map_landmarks) {
	// TODO: Update the weights of each particle using a mult-variate Gaussian distribution. You can read
	//   more about this distribution here: https://en.wikipedia.org/wiki/Multivariate_normal_distribution
	// NOTE: The observations are given in the VEHICLE'S coordinate system. Your particles are located
	//   according to the MAP'S coordinate system. You will need to transform between the two systems.
	//   Keep in mind that this transformation requires both rotation AND translation (but no scaling).
	//   The following is a good resource for the theory:
	//   https://www.willamette.edu/~gorr/classes/GeneralGraphics/Transforms/transforms2d.htm
	//   and the following is a good resource for the actual equation to implement (look at equation 
	//   3.33
	//   http://planning.cs.uiuc.edu/node99.html
    cout<<"updating weights ..."<<endl;
	vector<Map::single_landmark_s> landmarks = map_landmarks.landmark_list;
    weights.clear();
	for (Particle &p: particles){
        //cout<<"particles:" <<endl;
        p.associations.clear();
        p.sense_x.clear();
        p.sense_y.clear();
		double prob = 1.0;
		double distance, multiplier;
		for (const LandmarkObs &obs: observations){
            //cout<<"observations:"<<endl;
			double x = p.x + obs.x * cos(p.theta) - obs.y * sin(p.theta); // particle in map's coordinate
			double y = p.y + obs.x * sin(p.theta) + obs.y * cos(p.theta);
			double closest_dis = sensor_range;

			Map::single_landmark_s closest_landmark;
			for (Map::single_landmark_s landmark: landmarks){ // loop through landmark
				distance = dist(x, y, landmark.x_f,landmark.y_f);
				if (distance < closest_dis){
					closest_dis = distance;
					closest_landmark = landmark;
				}
			} // for loop landmark to find closest landmark
            if (closest_dis < sensor_range) { // make sure there is a landmark in range
                multiplier = 1 / (2 * M_PI * std_landmark[0] * std_landmark[1])
                             * exp(-(pow(x - closest_landmark.x_f, 2) / 2 / pow(std_landmark[0], 2)))
                             * exp(-(pow(y - closest_landmark.y_f, 2) / 2 / pow(std_landmark[1], 2)));
                prob *= multiplier;
                p.sense_x.push_back(x);
                p.sense_y.push_back(y);
                p.associations.push_back(closest_landmark.id_i);
            }
		} // end observation
        if (p.associations.size()==0)
            prob = 0;
        p.weight = prob;
        weights.push_back(prob);
		//p = SetAssociations(p,associations,sense_x,sense_y); // clear old value and fill in new value
	} // end particle
	cout <<endl;
}

void ParticleFilter::resample() {
	// TODO: Resample particles with replacement with probability proportional to their weight. 
	// NOTE: You may find std::discrete_distribution helpful here.
	//   http://en.cppreference.com/w/cpp/numeric/random/discrete_distribution
	default_random_engine gen;
	discrete_distribution<int> distribution(weights.begin(), weights.end());
	vector<Particle> resample_p;
	for (int i = 0; i < num_particles; i++)
		resample_p.push_back(particles[distribution(gen)]);
	particles = resample_p;
}

Particle ParticleFilter::SetAssociations(Particle particle, std::vector<int> associations, std::vector<double> sense_x, std::vector<double> sense_y)
{
	//particle: the particle to assign each listed association, and association's (x,y) world coordinates mapping to
	// associations: The landmark id that goes along with each listed association
	// sense_x: the associations x mapping already converted to world coordinates
	// sense_y: the associations y mapping already converted to world coordinates

	//Clear the previous associations
	particle.associations.clear();
	particle.sense_x.clear();
	particle.sense_y.clear();

	particle.associations= associations;
 	particle.sense_x = sense_x;
 	particle.sense_y = sense_y;

 	return particle;
}

string ParticleFilter::getAssociations(Particle best)
{
	vector<int> v = best.associations;
	stringstream ss;
    copy( v.begin(), v.end(), ostream_iterator<int>(ss, " "));
    string s = ss.str();
    s = s.substr(0, s.length()-1);  // get rid of the trailing space
    return s;
}
string ParticleFilter::getSenseX(Particle best)
{
	vector<double> v = best.sense_x;
	stringstream ss;
    copy( v.begin(), v.end(), ostream_iterator<float>(ss, " "));
    string s = ss.str();
    s = s.substr(0, s.length()-1);  // get rid of the trailing space
    return s;
}
string ParticleFilter::getSenseY(Particle best)
{
	vector<double> v = best.sense_y;
	stringstream ss;
    copy( v.begin(), v.end(), ostream_iterator<float>(ss, " "));
    string s = ss.str();
    s = s.substr(0, s.length()-1);  // get rid of the trailing space
    return s;
}
