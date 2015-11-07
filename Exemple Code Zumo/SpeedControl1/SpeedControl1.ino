#include <Wire.h>
#include <LSM303.h>
#include <Pushbutton.h>
#include <ZumoMotors.h>

#define LED_PIN 13

LSM303 compass;
ZumoMotors motors;
Pushbutton button(ZUMO_BUTTON);

void setup()
{
  Wire.begin();
  compass.init();
  compass.enableDefault();
  pinMode(LED_PIN, OUTPUT);
}

int x;

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
    compass.read();  
    x = (int)compass.a.x/7;
    // Set Motors Speed
    motors.setLeftSpeed(200 + x);
    motors.setRightSpeed(200 + x);
    delay(100);
  }
  delay(10);
  
  // Turn off
  button.waitForButton();
  digitalWrite(LED_PIN, LOW);

}
