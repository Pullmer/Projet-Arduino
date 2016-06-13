#include "Bat_level.h"

float bat_level()
{
  return (float)analogRead(1)*1.5*5/1023; // conversion tension batterie
}

void alerteBatterie()
{
  float a = bat_level();
  Serial.println("#bat_level:" + String(a) + ";");
  if(4 < a && a < 4.8)
  {
    Serial.println("#lowbat;");
  }
}

