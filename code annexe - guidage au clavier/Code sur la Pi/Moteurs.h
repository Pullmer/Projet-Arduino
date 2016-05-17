#ifndef Moteurs_h
#define Moteurs_h
#include "Arduino.h"
#include <ZumoMotors.h>

void pid();
void resetPID();
void set_kp(float k);
void set_kd(float k);
void set_ki(float k);
void set_vitesse_mot(int leftspeed, int rightspeed, bool adjust);
void set_vitesse_mot(int x, bool adjust);
void set_vitesse_mot_man(int leftspeed, int rightspeed);
void refresh_moteurs();
void run_previous_state_mot();
String getPIDParameters();
void set_maxSpeedLeft(int x);
void set_maxSpeedRight(int x);
int get_maxSpeedLeft();
int get_maxSpeedRight();

#endif
