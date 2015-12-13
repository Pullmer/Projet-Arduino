#include <SimpleTimer.h>
#include <ZumoMotors.h>
//#include <Pushbutton.h>
#include "Centrale_inertielle.h"
#include "Moteurs.h"
#include "Capteurs_ultrasons.h"
#include "Bat_level.h"

//Pushbutton button(ZUMO_BUTTON);
String buffer;
SimpleTimer timer_obstacle;

void setup()
{
  Serial.begin(115200);
  compass_init();
  calibrage();
  timer_obstacle.setInterval(500, alerte);
}

void loop()
{
  timer_obstacle.run();
  
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on chope un caractère de début de trame
    {
      buffer = "";
      buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
      if(buffer == "straight") straight();
      else if(buffer == "stop") brake();
      else if(buffer == "set_angle_boussole") setHeading_boussole(Serial.readStringUntil(';').toFloat());
      else if(buffer == "set_angle_relatif") setHeading_relatif(Serial.readStringUntil(';').toFloat());
      else if(buffer == "get_angle") Serial.println("Angle actuel : " + String(averageHeading()));
      else if(buffer == "back") back();
      else if(buffer == "bat_level") Serial.println("Niveau batterie : " + String(bat_level()));
    }
    else Serial.read();
  }
}

