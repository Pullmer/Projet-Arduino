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
  //compass_init();
  delay(1000);
  //calibrage();
  
  //timer_obstacle.setInterval(200, alerte);
  //timer_pid.setInterval(5, pid);
}

void loop()
{
  float e = 0;
  //timer_obstacle.run();
  //timer_pid.run();
  
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on a un caractère de début de trame
    {
      buffer = "";
      buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
      if(buffer == "straight") set_vitesse_mot(MAX_SPEED_LEFT, MAX_SPEED_RIGHT);
      else if(buffer == "back") set_vitesse_mot(-MAX_SPEED_LEFT, MAX_SPEED_RIGHT);
      else if(buffer == "stop") set_vitesse_mot(0);
      else if(buffer == "ping") Serial.println("pong");
      else if(buffer == "deviation")
      {
        e = Serial.readStringUntil(';').toFloat();
        Serial.println(e);
      }
      else if(buffer == "bat_level") Serial.println("Niveau batterie : " + String(bat_level()));
      else if(buffer == "kp") set_kp(Serial.readStringUntil(';').toFloat());
      else if(buffer == "ki") set_ki(Serial.readStringUntil(';').toFloat());
      else if(buffer == "kd") set_kd(Serial.readStringUntil(';').toFloat());
    }
    else Serial.read();
  }
}

