#ifndef Moteurs_h
#define Moteurs_h
#include "Arduino.h"
#include "Centrale_inertielle.h"
#include <PID_v1.h>
#include <ZumoMotors.h>

void init_PID();
void run_PID(boolean x);
void vitesse_mot(int leftspeed, int rightspeed);
void vitesse_mot(int speed);
void straight();
void brake();
void back();
void setHeading_boussole(float target_heading);
void setHeading_relatif(float target_heading);

#endif
