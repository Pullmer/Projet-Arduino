#include "Capteurs_ultrasons.h"
#include "Arduino.h"
#include <NewPing.h>

#define TRIGGER_PIN  4  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     5  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 30 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define DISTANCE_STOP 10

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

boolean obstacle()
{
  unsigned long x = sonar.ping_cm();
  return 0 < x && x < DISTANCE_STOP;
}

void alerte()
{
   if(obstacle()) Serial.println("obstacle !");
}

