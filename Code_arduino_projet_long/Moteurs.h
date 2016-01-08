#ifndef Moteurs_h
#define Moteurs_h
#include "Arduino.h"
#include "Centrale_inertielle.h"
#include <PID_v1.h>
#include <ZumoMotors.h>

void init_PID();
void compute_PID();
void set_vitesse_mot(int leftspeed, int rightspeed);
void set_vitesse_mot(int x);
void straight();
void brake();
void back();
void refresh_moteurs();
void run_previous_state_mot();
void setHeading_boussole(float target_heading);
void setHeading_relatif(float target_heading);

#endif
