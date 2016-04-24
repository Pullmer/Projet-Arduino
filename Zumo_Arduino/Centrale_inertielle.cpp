#include "Centrale_inertielle.h"
#include "Moteurs.h"

#define CALIBRATION_SAMPLES 100
#define CRB_REG_M_2_5GAUSS 0x60 // CRB_REG_M value for magnetometer +/-2.5 gauss full scale
#define CRA_REG_M_220HZ    0x1C // CRA_REG_M value for magnetometer 220 Hz update rate

LSM303 compass;

void calibrage() // Set calibrated values to compass.m_max and compass.m_min
{
  LSM303::vector<int16_t> running_min = {32767, 32767};
  LSM303::vector<int16_t> running_max = {-32767, -32767};
  
  set_vitesse_mot(400, -400); // on fait tourner le robot sur lui même
  
  for(int i = 0; i < CALIBRATION_SAMPLES; i++)
  {
    compass.read();
    running_min.x = min(running_min.x, compass.m.x);
    running_min.y = min(running_min.y, compass.m.y);
    running_max.x = max(running_max.x, compass.m.x);
    running_max.y = max(running_max.y, compass.m.y);
    delay(50);
  }
  
  set_vitesse_mot(0);
  
  compass.m_max.x = running_max.x;
  compass.m_max.y = running_max.y;
  compass.m_min.x = running_min.x;
  compass.m_min.y = running_min.y;
  
  Serial.println(compass.m_max.x);
  Serial.println(compass.m_max.y);
  Serial.println(compass.m_min.x);
  Serial.println(compass.m_min.y);
}

void compass_init()
{
  Wire.begin();
  compass.init();
  compass.enableDefault();

  compass.writeReg(LSM303::CRB_REG_M, CRB_REG_M_2_5GAUSS); // +/- 2.5 gauss sensitivity to hopefully avoid overflow problems
  compass.writeReg(LSM303::CRA_REG_M, CRA_REG_M_220HZ);    // 220 Hz compass update rate
  
  compass.m_max.x = 225;
  compass.m_max.y = 1305;
  compass.m_min.x = -1848;
  compass.m_min.y = -990;
}

float averageHeading() // Average 10 vectors to get a better measurement and help smooth out the motors' magnetic interference.
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
  
  return heading(avg);
}

float relativeHeading(float heading_from, float heading_to) // Différence entre deux angles
{
  float relative_heading = heading_to - heading_from;
  // constrain to -180 to 180 degree range
  if (relative_heading > 180)
    relative_heading -= 360;
  if (relative_heading < -180)
    relative_heading += 360;

  return relative_heading;
}

template <typename T> float heading(LSM303::vector<T> v) // Converts x and y components of a vector to a heading in degrees.
{
  float x_scaled =  2.0*(float)(v.x - compass.m_min.x) / ( compass.m_max.x - compass.m_min.x) - 1.0;
  float y_scaled =  2.0*(float)(v.y - compass.m_min.y) / (compass.m_max.y - compass.m_min.y) - 1.0;

  float angle = atan2(y_scaled, x_scaled)*180 / M_PI;
  if (angle < 0)
    angle += 360;
  return angle;
}
