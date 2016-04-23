#include "Moteurs.h"

int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};

float erreur = 0;
float erreur_precedente = 0;
float somme_erreur = 0;
float kp = 0.0;
float kd = 0.0;
float ki = 0.0;
float output_pid = 0;

ZumoMotors motors;

void pid(float e)
{
  erreur = e;
  somme_erreur += erreur;
  output_pid = kp*erreur + ki*somme_erreur + kd*(erreur - erreur_precedente);
  erreur_precedente = erreur;
  
  if(output_pid < -80) output_pid = -80;
  else if(output_pid > 80) output_pid = 80;
  
  if(vitesse_mot[0] == 0 && vitesse_mot[1] == 0) motors.setSpeeds(output_pid, -output_pid); // robot à l'arrêt
}

void set_kp(float k)
{
  kp = k;
}

void set_ki(float k)
{
  ki = k;
}

void set_kd(float k)
{
  kd = k;
}

void set_vitesse_mot(int leftspeed, int rightspeed)
{
  if(rightspeed > 120) rightspeed = 120;
  if(leftspeed > 120) leftspeed = 120;
  if(rightspeed < -120) rightspeed = -120;
  if(leftspeed < -120) leftspeed = -120;
  
  previous_vitesse_mot[0] = vitesse_mot[0];
  previous_vitesse_mot[1] = vitesse_mot[1];
  vitesse_mot[0] = leftspeed;
  vitesse_mot[1] = rightspeed;
  
  refresh_moteurs();
}

void set_vitesse_mot(int x)
{
  set_vitesse_mot(x, x);
}

void refresh_moteurs()
{
  motors.setSpeeds(vitesse_mot[0], vitesse_mot[1]);
  motors.flipLeftMotor(true); // "true" pour le robot rapide uniquement
}

void run_previous_state_mot()
{
  vitesse_mot[0] = previous_vitesse_mot[0];
  vitesse_mot[1] = previous_vitesse_mot[1];
  refresh_moteurs();
}

String getPIDParameters()
{
  return "kp : " + String(kp) + "; " + "ki : " + String(ki) + "; " + "kd : " + String(kd) + ";";
}

