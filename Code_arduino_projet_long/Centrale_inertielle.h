#ifndef Centrale_intertielle_h
#define Centrale_intertielle_h

#include "Arduino.h"
#include <Wire.h>
#include <LSM303.h>

void compass_init();
void calibrage();
float averageHeading();
float relativeHeading(float heading_from, float heading_to);
template <typename T> float heading(LSM303::vector<T> v);

#endif
