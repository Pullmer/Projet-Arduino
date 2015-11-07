#include <Wire.h>
#include <LSM303.h>
#include <Pushbutton.h>
#include <ZumoMotors.h>


#define LED_PIN 13

Pushbutton button(ZUMO_BUTTON);
ZumoMotors motors;

LSM303 compass;
LSM303::vector running_min = { 2047,  2047,  2047}, 
               running_max = {-2048, -2048, -2048};

void setup() {
  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
  pinMode(LED_PIN, OUTPUT);
  
//M min X: -838 Y: -703 Z: -4096 M max X: -123 Y: 205 Z: -2048
  
  /*
  compass.m_min.x = -838; 
  compass.m_min.y = -703; 
  compass.m_min.z = -4096;
  compass.m_max.x = -123; 
  compass.m_max.y = +205; 
  compass.m_max.z = -2048;
  */
  compass.m_min.x = running_min.x; 
  compass.m_min.y = running_min.y; 
  compass.m_min.z = running_min.z;
  compass.m_max.x = running_max.x; 
  compass.m_max.y = running_max.y; 
  compass.m_max.z = running_max.z;
  
}
double time;

void loop() {  

  button.waitForButton();
    Serial.print("To calibrate : Press the button for more than 3 seconds ");

  while(!button.isPressed());
  delay(10);
  while( button.isPressed()) {
    time++;
  }
  // In seconds
  time = time/45000;
  Serial.println(time);
  //time =  1;
  if (time > 3) {
    
    Serial.print(" Carefully, move your device in every direction ");
 
    while(!button.isPressed()) {
      compass.read();
      running_min.x = min(running_min.x, compass.m.x);
      running_min.y = min(running_min.y, compass.m.y);
      running_min.z = min(running_min.z, compass.m.z);
  
      running_max.x = max(running_max.x, compass.m.x);
      running_max.y = max(running_max.y, compass.m.y);
      running_max.z = max(running_max.z, compass.m.z);
      
      Serial.print("M min ");
      Serial.print("X: ");
      Serial.print((int)running_min.x);
      Serial.print(" Y: ");
      Serial.print((int)running_min.y);
      Serial.print(" Z: ");
      Serial.print((int)running_min.z);
  
      Serial.print(" M max ");  
      Serial.print("X: ");
      Serial.print((int)running_max.x);
      Serial.print(" Y: ");
      Serial.print((int)running_max.y);
      Serial.print(" Z: ");
      Serial.println((int)running_max.z);
      
      //delay(100);
    }
  
    Serial.println("Using registered values ");
    setup();
  }
  //time = 6;
  if (time > 5) {
    int heading;
    // Gradually aproximate to the north
     while(true) {
       compass.read();             
       heading = compass.heading((LSM303::vector){1,0,0});
       if(button.isPressed()) {
         while(heading > 3) {
           if (heading > 180)
             motors.setSpeeds(+200,-200);
           else
             motors.setSpeeds(-200,+200);
           compass.read();
           heading = compass.heading((LSM303::vector){1,0,0});
         }
         motors.setSpeeds(0,0);
         delay(100);
       }
     }
  }
  delay(10);
  while(button.isPressed());

  while(!button.isPressed()) {
    compass.read();
    int heading = compass.heading((LSM303::vector){1,0,0});
    Serial.println(heading);
    delay(100);
  }
}



