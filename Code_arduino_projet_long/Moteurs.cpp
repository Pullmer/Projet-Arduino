#include "Moteurs.h"

#define DEVIATION_THRESHOLD 2
#define DEFAULT_SPEED 400 // Maximum motor speed when going straight; variable speed when turning
#define TURN_BASE_SPEED 300 // Base speed when turning (added to variable speed)

double output_pid = 0;
double input_pid = averageHeading();
double consigne_pid = input_pid;

PID PID_mot(&input_pid, &output_pid, &consigne_pid,2,5,1, DIRECT);
ZumoMotors motors;

void init_PID()
{
  PID_mot.SetMode(AUTOMATIC);
  PID_mot.SetOutputLimits(200, 400);
}

void run_PID(boolean x)
{
  input_pid = averageHeading();
  
  if(x)
  {
    PID_mot.Compute();
    vitesse_mot(output_pid, -output_pid);
  }
}

void vitesse_mot(int leftspeed, int rightspeed)
  {motors.setSpeeds(leftspeed, rightspeed);}

void vitesse_mot(int x)
  {motors.setSpeeds(x);}

void straight()
  {motors.setSpeeds(DEFAULT_SPEED);}

void brake()
  {motors.setSpeeds(0);}

void back()
  {motors.setSpeeds(-DEFAULT_SPEED);}

void setHeading_relatif(float target_heading)
  {setHeading_boussole(averageHeading() + target_heading);}

void setHeading_boussole(float target_heading)
{
  consigne_pid = target_heading;
  /*unsigned long chrono = millis();
  
  if(target_heading <= 360.0 && target_heading >= 0)
  {
    for(int i = 0 ; i < 3 ; i++)
    {
      motors.setSpeeds(0);
      delay(1000);
      float relative_heading = relativeHeading(target_heading, averageHeading());
    
      while(abs(relative_heading) > DEVIATION_THRESHOLD && (millis() - chrono) < 5000)
      {
        if(relative_heading > 0)
          motors.setSpeeds(-TURN_BASE_SPEED, TURN_BASE_SPEED);
        else
          motors.setSpeeds(TURN_BASE_SPEED, -TURN_BASE_SPEED);
            
        relative_heading = relativeHeading(target_heading, averageHeading());
      }
    }
  }
  motors.setSpeeds(0);*/
}
