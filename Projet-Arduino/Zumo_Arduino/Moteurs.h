#ifndef Moteurs_h
#define Moteurs_h
#include "Arduino.h"
#include <ZumoMotors.h>
#include <QTRSensors.h>
#include <ZumoReflectanceSensorArray.h>

void pid();
void setKp(float k);
void setKd(float k);
void turn(int mode);
boolean isOnHorizontalLine();
void setVitesseMot(int leftspeed, int rightspeed);
void setVitesseMot(int x);
void refreshMoteurs();
void runPreviousStateMot();
void initReflectanceSensors();
void calibrateSensors();
void setMaxSpeed(int x);
int getMaxSpeed();

#endif
