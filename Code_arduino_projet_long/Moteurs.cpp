#include "Moteurs.h"

int vitesse_mot[] = {0, 0};
int previous_vitesse_mot[] = {0, 0};

float consigne_angle = 0; // initialisation PID
float erreur = 0;

ZumoMotors motors;

void pid()
{
  erreur = relativeHeading(consigne_angle, averageHeading());
  if(abs(erreur) > 5)
  {
    if((vitesse_mot[0] == 0) && (vitesse_mot[1] == 0))
    {
      if(erreur > 0) motors.setSpeeds(-PID_SPEED, PID_SPEED);
      else motors.setSpeeds(PID_SPEED, -PID_SPEED);
      delay(50);
    }
    else
    {
      if(erreur > 0) motors.setSpeeds(vitesse_mot[0] - 100, vitesse_mot[0]);
      else motors.setSpeeds(vitesse_mot[0], vitesse_mot[0] - 100);
      delay(100);
    }
  }

  refresh_moteurs();
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
