#include "Moteurs.h"

#define LINE_THRESHOLD 800
int MAX_SPEED = 300;
int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};
int erreur_precedente = 0;
float kp = 0.5;
float kd = 0.2;
unsigned int sensors[6];
boolean surLigneHorizontale = false;

ZumoMotors motors;
ZumoReflectanceSensorArray reflectanceSensors;

void pid()
{
  int pos = reflectanceSensors.readLine(sensors);
  
  if(isOnHorizontalLine()) // robot sur une ligne horizontale
  {
    if(!surLigneHorizontale)
    {
      setVitesseMot(0);
      Serial.println("#lignedetected;");
    }
    surLigneHorizontale = true;
  }
  else
  {
    surLigneHorizontale = false;
  }
  
  int erreur = pos - 2500;
  int output_pid = kp*(float)erreur + kd*(float)(erreur - erreur_precedente);
  erreur_precedente = erreur;
  
  int m1Speed = vitesse_mot[0] + output_pid;
  int m2Speed = vitesse_mot[1] - output_pid;
  if(!(abs(erreur) < 200 && vitesse_mot[0] == 0 && vitesse_mot[1] == 0)) motors.setSpeeds(m1Speed, m2Speed);
}

void setKp(float k)
{
  kp = k;
}

void setKd(float k)
{
  kd = k;
}

void turn(int mode)
{
  //mode = "0 : droite ; 1 : gauche ; 2 : demi-tour"
  if(mode != 2)
  {
    motors.setSpeeds(MAX_SPEED);
    delay(300);
    motors.setSpeeds(0);
  }

  if(mode == 0) {motors.setSpeeds(400, -400);delay(500);}
  if(mode == 1) {motors.setSpeeds(-400, 400);delay(500);}
  if(mode == 2) {motors.setSpeeds(-400, 400);delay(1000);}

  while(abs(reflectanceSensors.readLine(sensors) - 2500) > 300){delay(10);}
  
  setVitesseMot(MAX_SPEED);setVitesseMot(MAX_SPEED);
  surLigneHorizontale = false;
}

boolean isOnHorizontalLine()
{
  return sensors[0] > LINE_THRESHOLD && sensors[1] > LINE_THRESHOLD && sensors[2] > LINE_THRESHOLD && sensors[3] > LINE_THRESHOLD && sensors[4] > LINE_THRESHOLD && sensors[5] > LINE_THRESHOLD;
}

void setVitesseMot(int leftspeed, int rightspeed)
{  
  previous_vitesse_mot[0] = vitesse_mot[0];
  previous_vitesse_mot[1] = vitesse_mot[1];
  vitesse_mot[0] = leftspeed;
  vitesse_mot[1] = rightspeed;
  
  refreshMoteurs();
}

void setVitesseMot(int x)
{
  setVitesseMot(x, x);
}

void refreshMoteurs()
{
  motors.setSpeeds(vitesse_mot[0], vitesse_mot[1]);
  //motors.flipLeftMotor(true); // "true" pour le robot rapide uniquement
}

void runPreviousStateMot()
{
  vitesse_mot[0] = previous_vitesse_mot[0];
  vitesse_mot[1] = previous_vitesse_mot[1];
  refreshMoteurs();
}

void initReflectanceSensors()
{
  reflectanceSensors.init();
}

void calibrateSensors()
{
  delay(500);
  motors.setSpeeds(400, -400);
  for(int i = 0; i < 50; i++)
  {
    reflectanceSensors.calibrate();
    delay(20);
  }
  motors.setSpeeds(0);
}

void setMaxSpeed(int x)
{
  MAX_SPEED = x;
}

int getMaxSpeed()
{
  return MAX_SPEED;
}

