#include "Moteurs.h"

#define LINE_THRESHOLD 800 // 800 normalement
int MAX_SPEED = 125; // 300 pour robots lents, 125 robots rapides
int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};
int erreur_precedente = 0;
float kp = 0.15; // 0.5 robots lents, 0.15 robots rapides
float kd = 0.05; // 0.2 robots lents, 0.05 robots rapides
unsigned int sensors[6];
boolean surLigneHorizontale = false;

ZumoMotors motors;
ZumoReflectanceSensorArray reflectanceSensors;

void pid() // boucle PID
{
  int pos = reflectanceSensors.readLine(sensors);
  //Serial.println(String(sensors[0]) + " ; " + String(sensors[1]) + " ; " + String(sensors[2]) + " ; " + String(sensors[3]) + " ; " +  String(sensors[4])  + " ; " +  String(sensors[5]));
  
  if(isOnHorizontalLine()) // robot sur une ligne horizontale
  {
    if(!surLigneHorizontale)
    {
      setVitesseMot(0);
      Serial.println("#lignedetected;"); // on informe la raspberryPi que le robot est sur un carrefour
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
  m1Speed = constrain(m1Speed, -200, 200); // robot rapide uniquement
  m2Speed = constrain(m2Speed, -200, 200); // robot rapide uniquement
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

void turn(int mode) // fonction pour tourner sur un carrefour
{
  //mode = "0 : droite ; 1 : gauche ; 2 : demi-tour"
  if(mode != 2)
  {
    motors.setSpeeds(MAX_SPEED); // le robot se positionne sur le carrefour
    delay(200);
    motors.setSpeeds(0);
  }
  
  // Rotations
  if(mode == 0) {motors.setSpeeds(150, -150);delay(500);} //400, -400 robots lents, 150, -150 robots rapides
  if(mode == 1) {motors.setSpeeds(-150, 150);delay(500);} //-400, +400 robots lents, -150, 150 robots rapides
  if(mode == 2) {motors.setSpeeds(-150, 150);delay(1000);} //-400, 400 robots lents, -150, 150 robots rapides

  while(abs(reflectanceSensors.readLine(sensors) - 2500) > 300){delay(10);}
  
  setVitesseMot(MAX_SPEED);setVitesseMot(MAX_SPEED);
  delay(150); // on attend que le robot sorte du carrefour
  surLigneHorizontale = false;
}

boolean isOnHorizontalLine() // détection carrefour
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
  motors.flipLeftMotor(true); // "true" pour le robot rapide uniquement
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

void calibrateSensors() // calibrage capteurs IR
{
  delay(500);
  motors.setSpeeds(150, -150); // 400, -400 pour les robots lents, 150, -150 robots rapides
  for(int i = 0; i < 70; i++)
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

