//#include <Pushbutton.h>
#include <SimpleTimer.h>
#include <ZumoMotors.h>
//#include "Centrale_inertielle.h"
#include "Moteurs.h"
#include "Capteurs_ultrasons.h"
#include "Bat_level.h"

String buffer;
SimpleTimer timer_obstacle;
SimpleTimer timer_batterie;
SimpleTimer timer_pid;
//Pushbutton button(ZUMO_BUTTON);

int commandeD;
int commandeG;


void setup()
{
  Serial.begin(115200);
  refresh_moteurs();
}

void loop()
{
  
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on a un caractère de début de trame
    {
      buffer = " ";
      buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
      if(buffer == "face") set_vitesse_mot(get_maxSpeedLeft(), get_maxSpeedRight(), true);
      else if(buffer == "back") set_vitesse_mot(-get_maxSpeedLeft(), -get_maxSpeedRight(), true);
      else if(buffer == "pause") set_vitesse_mot(0, true);
      else if(buffer == "droite") 1+1;
      else if(buffer == "gauche") 1+1;
      else if(buffer == "turnback") 1+1;
      else if(buffer == "ping") 
	  {
		Serial.println("#pong;");
      }
	  else if (buffer == "speedO")
	  {
		commandeG = Serial.readStringUntil(';').toInt();
		commandeD = Serial.readStringUntil(';').toInt();
		set_vitesse_mot_man(commandeG,commandeD);
	  }
	  else if(buffer == "bat_level") Serial.println("#bat_level:" + String(bat_level()) + ";");
      else if(buffer == "kp") set_kp(Serial.readStringUntil(';').toFloat());
      else if(buffer == "ki") set_ki(Serial.readStringUntil(';').toFloat());
      else if(buffer == "kd") set_kd(Serial.readStringUntil(';').toFloat());
      else if(buffer == "askPIDParameters") Serial.println(getPIDParameters());
      else if(buffer == "setMaxSpeedLeft") set_maxSpeedLeft(Serial.readStringUntil(';').toInt());
      else if(buffer == "setMaxSpeedRight") set_maxSpeedRight(Serial.readStringUntil(';').toInt());
    }
    else Serial.read();
  }
  
  delay(20);
  
}

