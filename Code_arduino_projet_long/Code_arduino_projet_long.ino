#include <ZumoMotors.h>
#include <Pushbutton.h>
#include <Wire.h>
#include <LSM303.h>

#define DEFAULT_SPEED 400 // Maximum motor speed when going straight; variable speed when turning
#define TURN_BASE_SPEED 300 // Base speed when turning (added to variable speed)

#define CRB_REG_M_2_5GAUSS 0x60 // CRB_REG_M value for magnetometer +/-2.5 gauss full scale
#define CRA_REG_M_220HZ    0x1C // CRA_REG_M value for magnetometer 220 Hz update rate

// Allowed deviation (in degrees) relative to target angle that must be achieved before driving straight
#define DEVIATION_THRESHOLD 2.5

ZumoMotors motors;
Pushbutton button(ZUMO_BUTTON);
LSM303 compass;
String buffer;

void setup()
{
  Serial.begin(115200);
  motors.setSpeeds(0);
  Wire.begin();
  compass.init();
  compass.enableDefault();

  compass.writeReg(LSM303::CRB_REG_M, CRB_REG_M_2_5GAUSS); // +/- 2.5 gauss sensitivity to hopefully avoid overflow problems
  compass.writeReg(LSM303::CRA_REG_M, CRA_REG_M_220HZ);    // 220 Hz compass update rate
  // Set calibrated values to compass.m_max and compass.m_min
  compass.m_max.x = -102;
  compass.m_max.y = 501;
  compass.m_min.x = -307;
  compass.m_min.y = 250;
}

void loop()
{
  if(Serial.available() > 0)
  {
    if(char(Serial.read()) == '#') // si on chope un caractère de début de trame
    {
    buffer = "";
    buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
    if(buffer == "straight") motors.setSpeeds(DEFAULT_SPEED);
    if(buffer == "stop") motors.setSpeeds(0);
    if(buffer == "setAngle") setHeading(Serial.readStringUntil(';').toFloat());
    if(buffer == "getAngle") Serial.println("#" + String(averageHeading()) + ";");
    if(buffer == "back") motors.setSpeeds(-DEFAULT_SPEED);
    }
    else Serial.read();
  }
}

void setHeading(float target_heading)
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

// Converts x and y components of a vector to a heading in degrees.
template <typename T> float heading(LSM303::vector<T> v)
{
  float x_scaled =  2.0*(float)(v.x - compass.m_min.x) / ( compass.m_max.x - compass.m_min.x) - 1.0;
  float y_scaled =  2.0*(float)(v.y - compass.m_min.y) / (compass.m_max.y - compass.m_min.y) - 1.0;

  float angle = atan2(y_scaled, x_scaled)*180 / M_PI;
  if (angle < 0)
    angle += 360;
  return angle;
}

// Yields the angle difference in degrees between two headings
float relativeHeading(float heading_from, float heading_to)
{
  float relative_heading = heading_to - heading_from;

  // constrain to -180 to 180 degree range
  if (relative_heading > 180)
    relative_heading -= 360;
  if (relative_heading < -180)
    relative_heading += 360;

  return relative_heading;
}

// Average 10 vectors to get a better measurement and help smooth out
// the motors' magnetic interference.
float averageHeading()
{
  LSM303::vector<int32_t> avg = {0, 0, 0};

  for(int i = 0; i < 10; i ++)
  {
    compass.readMag();
    avg.x += compass.m.x;
    avg.y += compass.m.y;
  }
  avg.x /= 10.0;
  avg.y /= 10.0;

  // avg is the average measure of the magnetic vector.
  return heading(avg);
}
