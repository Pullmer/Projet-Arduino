#include "Moteurs.h"
#include "Arduino.h"

#define DEVIATION_THRESHOLD 2
#define DEFAULT_SPEED 400 // Maximum motor speed when going straight; variable speed when turning
#define TURN_BASE_SPEED 300 // Base speed when turning (added to variable speed)

ZumoMotors motors;

void vitesse_mot(int leftspeed, int rightspeed)
{
  motors.setSpeeds(leftspeed, rightspeed);
}

void vitesse_mot(int x)
{
  motors.setSpeeds(x);
}

void straight()
{
  motors.setSpeeds(DEFAULT_SPEED);
}

void brake()
{
  motors.setSpeeds(0);
}

void back()
{
  motors.setSpeeds(-DEFAULT_SPEED);
}

void setHeading_relatif(float target_heading)
{
  
}

void setHeading_boussole(float target_heading)
{
  unsigned long chrono = millis();
  
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
  motors.setSpeeds(0);
}
