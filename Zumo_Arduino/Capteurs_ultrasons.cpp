#include "Capteurs_ultrasons.h"
#include "Moteurs.h"

#define TRIGGER_PIN  4  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     5  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 30 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define DISTANCE_STOP 10 // distance à laquelle on lance une alerte obstacle

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

boolean blocked = false;

boolean obstacle()
{
  unsigned long x = sonar.ping_cm();
  return 0 < x && x < DISTANCE_STOP;
}

void alerte()
{
   if(obstacle() && !blocked) // obstacle détecté
   {
    Serial.println("#obstacledetected;");
    blocked = true;
    set_vitesse_mot(0); // stop moteurs
   }
   else if(!obstacle() && blocked) // il n'y a plus d'obstacle
   {
    run_previous_state_mot();
    blocked = false;
    Serial.println("#obstacleleft;");
   }
}

