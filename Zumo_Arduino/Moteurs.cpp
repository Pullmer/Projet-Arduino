#include "Moteurs.h"
#include "Centrale_inertielle.h"

int MAX_SPEED_LEFT = 235;
int MAX_SPEED_RIGHT = 239;

int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};

float consigne = 0;
float erreur_precedente = 0;
float somme_erreur = 0;
float kp = 12.0;
float kd = 0.0;
float ki = 0.0;

ZumoMotors motors;

void pid()
{
  float erreur = relativeHeading(consigne, averageHeading());
  somme_erreur += erreur;
  float output_pid = kp*erreur + ki*somme_erreur + kd*(erreur - erreur_precedente);
  erreur_precedente = erreur;
  
  output_pid = constrain(output_pid, -400, 400);
  
  //if(vitesse_mot[0] == 0 && vitesse_mot[1] == 0) motors.setSpeeds(-output_pid, output_pid); // robot à l'arrêt
}

void resetPID()
{
  somme_erreur = 0;
  erreur_precedente = 0;
}

void set_kp(float k)
{
  kp = k;
}

void set_kd(float k)
{
  kd = k;
}

void set_ki(float k)
{
  ki = k;
}

void set_vitesse_mot(int leftspeed, int rightspeed, bool adjust)
{
  if(adjust)
  {
    leftspeed = constrain(leftspeed, -MAX_SPEED_LEFT, MAX_SPEED_LEFT);
    rightspeed = constrain(rightspeed, -MAX_SPEED_RIGHT, MAX_SPEED_RIGHT);
  }
  
  previous_vitesse_mot[0] = vitesse_mot[0];
  previous_vitesse_mot[1] = vitesse_mot[1];
  vitesse_mot[0] = leftspeed;
  vitesse_mot[1] = rightspeed;
  
  refresh_moteurs();
}

void set_vitesse_mot(int x, bool adjust)
{
  set_vitesse_mot(x, x, adjust);
}

void refresh_moteurs()
{
  motors.setSpeeds(vitesse_mot[0], vitesse_mot[1]);
  //motors.flipLeftMotor(true); // "true" pour le robot rapide uniquement
}

void run_previous_state_mot()
{
  vitesse_mot[0] = previous_vitesse_mot[0];
  vitesse_mot[1] = previous_vitesse_mot[1];
  refresh_moteurs();
}

String getPIDParameters()
{
  return "#kp:" + String(kp) + ";" + "#ki:" + String(ki) + ";" + "#kd:" + String(kd) + ";";
}

void set_maxSpeedLeft(int x)
{
  MAX_SPEED_LEFT = x;
}
void set_maxSpeedRight(int x)
{
  MAX_SPEED_RIGHT = x;
}

int get_maxSpeedLeft()
{
  return MAX_SPEED_LEFT;
}
int get_maxSpeedRight()
{
  return MAX_SPEED_RIGHT;
}

