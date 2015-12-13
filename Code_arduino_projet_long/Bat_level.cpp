#include "Bat_level.h"
#include "Arduino.h"

float bat_level()
{
  return (float)analogRead(1)*1.5*5/1023;
}
