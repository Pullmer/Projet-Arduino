#include <Wire.h>
#include <LSM303.h>

LSM303 compass;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
}

int min_z=-17;
const int delta_z=12;
int z[delta_z];
int iterator = 0;
int l;

void loop() {
  compass.read();
  
  l = (int)compass.a.x >> 2;

  iterator = l-min_z;

  if ( (iterator >= 0) & ( iterator < delta_z) )
    z[iterator]++;
    
  for (int i=0;i<delta_z;i++)
  {
    Serial.print(" | ");
    Serial.print(z[i]);
  }
  Serial.print(" | ");
  Serial.print(l);
  Serial.println(" |");
  
  delay(100);
}
