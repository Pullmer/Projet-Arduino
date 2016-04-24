#include "Moteurs.h"
#include "Centrale_inertielle.h"

int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};

float consigne = 0;
float erreur_precedente = 0;
float somme_erreur = 0;
float kp = 5.0;
float kd = 0.1;
float ki = 0.01;

ZumoMotors motors;

void pid_boussole()
{
  float erreur = relativeHeading(consigne, averageHeading());
  somme_erreur += erreur;
  float output_pid = kp*erreur + ki*somme_erreur + kd*(erreur - erreur_precedente);
  erreur_precedente = erreur;
  
  if(output_pid < -120) output_pid = -120;
  else if(output_pid > 120) output_pid = 120;
  
  if(vitesse_mot[0] == 0 && vitesse_mot[1] == 0) motors.setSpeeds(-output_pid, output_pid); // robot à l'arrêt
}

void setConsigneBoussole(float c)
{
  consigne = c;
}

void resetPIDBoussole()
{
  somme_erreur = 0;
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
  return "#kp:" + String(kp) + ";" + "#ki:" + String(ki) + ";" + "#kd:" + String(kd) + ";";
}

