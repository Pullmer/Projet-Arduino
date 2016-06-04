#include <SimpleTimer.h>
#include <Pushbutton.h>
#include "Bat_level.h"
#include "Capteurs_ultrasons.h"
//#include "Centrale_inertielle.h"
#include "Moteurs.h"

String buffer;
SimpleTimer timer_obstacle;
SimpleTimer timer_batterie;
Pushbutton button(ZUMO_BUTTON);

void setup()
{
  Serial.begin(115200);
  
  timer_obstacle.setInterval(200, alerteObstacle);
  timer_batterie.setInterval(5000, alerteBatterie);
  
  refreshMoteurs();
  initReflectanceSensors();
  Serial.println("Attente bouton pour calibration");
  button.waitForButton();
  calibrateSensors();
}

void loop()
{
  timer_obstacle.run();
  timer_batterie.run();
  pid();
  
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on a un caractère de début de trame
    {
      buffer = "";
      buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
      if(buffer == "face" || buffer == "straight") setVitesseMot(getMaxSpeed(), getMaxSpeed());
      else if(buffer == "back") setVitesseMot(-getMaxSpeed(), -getMaxSpeed());
      else if(buffer == "pause" || buffer == "stop" || buffer == "workcompleted") setVitesseMot(0);
      else if(buffer == "droite") turn(0);
      else if(buffer == "gauche") turn(1);
      else if(buffer == "turnback") turn(2);
      else if(buffer == "ping") Serial.println("#pong;");
      else if(buffer == "bat_level") Serial.println("#bat_level:" + String(bat_level()) + ";");
      else if(buffer == "kp") setKp(Serial.readStringUntil(';').toFloat());
      else if(buffer == "kd") setKd(Serial.readStringUntil(';').toFloat());
      else if(buffer == "setMaxSpeed") setMaxSpeed(Serial.readStringUntil(';').toInt());
      else if(buffer == "calibrage") calibrateSensors();
    }
    else Serial.read();
  }
}

