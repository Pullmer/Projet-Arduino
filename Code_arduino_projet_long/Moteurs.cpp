#include "Moteurs.h"

int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};

float consigne_angle = 0; // initialisation PID
float erreur = 0;
float erreur_precedente = 0;
float somme_erreur = 0;
float kp = 0;
float kd = 0;
float ki = 0;
float output_pid = 0;

ZumoMotors motors;

void pid()
{  
  if(abs(relativeHeading(consigne_angle, averageHeading())) > 5)
  {
    erreur = relativeHeading(consigne_angle, averageHeading()); // compris entre -180 et 180
    somme_erreur += erreur;
    /*if(somme_erreur > borne_max) somme_erreur = borne_max;
    else if(somme_erreur < borne_min) somme_erreur = borne_min;*/
    erreur_precedente = erreur;
    
    output_pid = kp*erreur + ki*somme_erreur + kd*(erreur - erreur_precedente);
    if(output_pid < -370) output_pid = -370;
    else if(output_pid > 370) output_pid = 370;
    
    set_vitesse_mot(-output_pid, output_pid);
  }
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
  if(rightspeed > 400) rightspeed = 400;
  if(leftspeed > 400) leftspeed = 400;
  if(rightspeed < -400) rightspeed = -400;
  if(leftspeed < -400) leftspeed = -400;
  
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
  motors.flipLeftMotor(false); // "true" pour le robot rapide uniquement
  motors.setSpeeds(vitesse_mot[0], vitesse_mot[1]);
}

void run_previous_state_mot()
{
  vitesse_mot[0] = previous_vitesse_mot[0];
  vitesse_mot[1] = previous_vitesse_mot[1];
  refresh_moteurs();
}

void setHeading_relatif(float target_heading)
{
  setHeading_boussole(averageHeading() + target_heading);
}

void setHeading_boussole(float target_heading)
{
  consigne_angle = target_heading;
}
