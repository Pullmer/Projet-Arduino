#ifndef Moteurs_h
#define Moteurs_h
#include "Arduino.h"
#include <ZumoMotors.h>

#define MAX_SPEED_LEFT 100
#define MAX_SPEED_RIGHT 100

void pid();
void set_kp(float k);
void set_kd(float k);
void set_ki(float k);
void set_vitesse_mot(int leftspeed, int rightspeed);
void set_vitesse_mot(int x);
void refresh_moteurs();
void run_previous_state_mot();
void refreshAngularError(float e);

#endif
