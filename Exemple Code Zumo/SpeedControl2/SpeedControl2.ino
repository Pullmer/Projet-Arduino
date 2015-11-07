#include <Wire.h>
#include <libraries/LSM303.h>
#include <libraries/Pushbutton.h>
#include <libraries/ZumoMotors.h>

#define LED_PIN 13

LSM303 compass;
ZumoMotors motors;
Pushbutton button(ZUMO_BUTTON);

void setup()
{  
  Serial.begin(9600);

  Wire.begin();
  compass.init();
  compass.enableDefault();
  pinMode(LED_PIN, OUTPUT);
}

int accel_x = 0;

void loop()
{
  // Wait for a signal
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);

  button.waitForButton();
  // Set LED : ON
  digitalWrite(LED_PIN, HIGH);

  while(!button.isPressed()) { 
    // Read accelerometer values
    // And take the mean
    accel_x = 0;
    for (int i=0;i<16;i++) {
      compass.read();  
      accel_x = accel_x + (int)compass.a.x >> 2;
    }
    accel_x = accel_x/16;
    Serial.println(accel_x);
    /*
    compass.read();  
    accel_x = (int)compass.a.x >> 2;
    Serial.println(accel_x);
    */
    // Set Motors Speed
    motors.setLeftSpeed(210 + accel_x*10);
    motors.setRightSpeed(210 + accel_x*10);
    delay(100);
  }
  delay(10);
  
  // Turn off
  button.waitForButton();
  digitalWrite(LED_PIN, LOW);

}
