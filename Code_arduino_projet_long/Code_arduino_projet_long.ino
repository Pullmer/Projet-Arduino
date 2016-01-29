#include <Pushbutton.h>
#include <SimpleTimer.h>
#include <ZumoMotors.h>
#include "Centrale_inertielle.h"
#include "Moteurs.h"
#include "Capteurs_ultrasons.h"
#include "Bat_level.h"

String buffer;
SimpleTimer timer_obstacle;
SimpleTimer timer_pid;
Pushbutton button(ZUMO_BUTTON);

void setup()
{
  Serial.begin(115200);
  compass_init();
  delay(1500);
  timer_obstacle.setInterval(200, alerte);
  timer_pid.setInterval(50, pid);
  setHeading_boussole(averageHeading());
}

void loop()
{
  //timer_obstacle.run();
  timer_pid.run();
  
  if(button.isPressed()) calibrage();
  
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on a un caractère de début de trame
    {
      buffer = " ";
      buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
      if(buffer == "straight") set_vitesse_mot(MAX_SPEED);
      else if(buffer == "back") set_vitesse_mot(-MAX_SPEED);
      else if(buffer == "stop") set_vitesse_mot(0);
      else if(buffer == "set_angle_boussole") setHeading_boussole(Serial.readStringUntil(';').toFloat());
      else if(buffer == "set_angle_relatif") setHeading_relatif(Serial.readStringUntil(';').toFloat());
      else if(buffer == "get_angle") Serial.println("Angle actuel : " + String(averageHeading()));
      else if(buffer == "bat_level") Serial.println("Niveau batterie : " + String(bat_level()));
      else if(buffer == "calibrage") calibrage();
    }
    else Serial.read();
  }
}

