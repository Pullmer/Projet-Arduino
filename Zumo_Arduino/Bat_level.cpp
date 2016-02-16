#include "Bat_level.h"

float bat_level()
{
  return (float)analogRead(1)*1.5*5/1023; // conversion tension batterie
}
