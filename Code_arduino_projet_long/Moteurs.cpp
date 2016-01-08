#include "Moteurs.h"

#define MAX_SPEED 400 // Maximum motor speed when going straight; variable speed when turning

double output_pid = 0;
double input_pid = averageHeading();
double consigne_pid = input_pid;

int vitesse_mot[] = {0, 0};
int previous_state_mot[] = {0, 0};

PID PID_mot(&input_pid, &output_pid, &consigne_pid,2,5,1, DIRECT);
ZumoMotors motors;

void init_PID()
{
  PID_mot.SetMode(AUTOMATIC);
  PID_mot.SetOutputLimits(0, 50); // à modif
}

void compute_PID()
{
  input_pid = averageHeading(); // varie de 0° à 360°
  PID_mot.Compute();
  
  previous_state_mot[0] = vitesse_mot[0];
  previous_state_mot[1] = vitesse_mot[1];
  vitesse_mot[0] = vitesse_mot[0] + output_pid; // A MODIF
  vitesse_mot[1] = vitesse_mot[1] - output_pid;
}

void set_vitesse_mot(int leftspeed, int rightspeed)
{
  previous_state_mot[0] = vitesse_mot[0];
  previous_state_mot[1] = vitesse_mot[1];
  vitesse_mot[0] = leftspeed;
  vitesse_mot[1] = rightspeed;
  refresh_moteurs();
}

void set_vitesse_mot(int x)
{
  previous_state_mot[0] = vitesse_mot[0];
  previous_state_mot[1] = vitesse_mot[1];
  vitesse_mot[0] = x;
  vitesse_mot[1] = x;
  refresh_moteurs();
}

void straight()
{
  set_vitesse_mot(MAX_SPEED);
}

void brake()
{
  set_vitesse_mot(0);
}

void back()
{
  set_vitesse_mot(-MAX_SPEED);
}

void refresh_moteurs()
{
  motors.setSpeeds(vitesse_mot[0], vitesse_mot[1]);
}

void run_previous_state_mot()
{
  vitesse_mot[0] = previous_state_mot[0];
  vitesse_mot[1] = previous_state_mot[1];
}

void setHeading_relatif(float target_heading)
{
  setHeading_boussole(averageHeading() + target_heading);
}

void setHeading_boussole(float target_heading)
{
  consigne_pid = target_heading;
}
