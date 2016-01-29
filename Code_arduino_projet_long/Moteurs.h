#ifndef Moteurs_h
#define Moteurs_h
#include "Arduino.h"
#include "Centrale_inertielle.h"
#include <ZumoMotors.h>

#define MAX_SPEED 400 // Maximum motor speed when going straight; variable speed when turning
#define PID_SPEED 280 // Maximum motor speed when going straight; variable speed when turning

void pid();
void set_vitesse_mot(int leftspeed, int rightspeed);
void set_vitesse_mot(int x);
void refresh_moteurs();
void run_previous_state_mot();
void setHeading_boussole(float target_heading);
void setHeading_relatif(float target_heading);

#endif
