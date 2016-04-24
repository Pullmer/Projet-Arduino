#include <Pushbutton.h>
#include <SimpleTimer.h>
#include <ZumoMotors.h>
#include "Centrale_inertielle.h"
#include "Moteurs.h"
#include "Capteurs_ultrasons.h"
#include "Bat_level.h"

String buffer;
SimpleTimer timer_obstacle;
SimpleTimer timer_batterie;
SimpleTimer timer_pid_boussole;
Pushbutton button(ZUMO_BUTTON);

bool enable_timer_obstacle = false;
bool enable_timer_pid_boussole = true;

void setup()
{
  Serial.begin(115200);
  
  timer_obstacle.setInterval(100, alerteObstacle);
  timer_batterie.setInterval(5000, alerteBatterie);
  timer_pid_boussole.setInterval(5, pid_boussole);
  
  refresh_moteurs();
  compass_init();
  //calibrage();
  setConsigneBoussole(averageHeading());
}

void loop()
{
  if(enable_timer_obstacle) timer_obstacle.run();
  timer_batterie.run();
  if(enable_timer_pid_boussole) timer_pid_boussole.run();
  
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on a un caractère de début de trame
    {
      buffer = "";
      buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
      if(buffer == "straight") set_vitesse_mot(MAX_SPEED_LEFT, MAX_SPEED_RIGHT);
      else if(buffer == "back") set_vitesse_mot(-MAX_SPEED_LEFT, -MAX_SPEED_RIGHT);
      else if(buffer == "pause") set_vitesse_mot(0);
      else if(buffer == "ping") Serial.println("#pong;");
      else if(buffer == "consigne") setConsigneBoussole(Serial.readStringUntil(';').toFloat());
      else if(buffer == "calibrage") calibrage();
      else if(buffer == "bat_level") Serial.println("#bat_level:" + String(bat_level()) + ";");
      else if(buffer == "kp") set_kp(Serial.readStringUntil(';').toFloat());
      else if(buffer == "ki") set_ki(Serial.readStringUntil(';').toFloat());
      else if(buffer == "kd") set_kd(Serial.readStringUntil(';').toFloat());
      else if(buffer == "askPIDParameters") Serial.println(getPIDParameters());
    }
    else Serial.read();
  }
}

