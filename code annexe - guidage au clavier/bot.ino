#include <Pushbutton.h>
#include <SimpleTimer.h>
#include <ZumoMotors.h>
#include "Centrale_inertielle.h"
#include "Moteurs.h"
#include "Capteurs_ultrasons.h"
#include "Bat_level.h"

int commande;
int commandeG;
int commandeD;
String buffer;
SimpleTimer timer_obstacle;
SimpleTimer timer_pid;
Pushbutton button(ZUMO_BUTTON);

void setup()
{
	Serial.begin(115200);
}

void loop()
{
	if(Serial.available() > 0)
	{
		if(char(Serial.read()) == '#') // si on a un caractère de début de trame
		{
			buffer = " ";
			buffer = Serial.readStringUntil(';'); // on lit jusqu'au caractère de fin de trame
			if(buffer == "bat_level") Serial.println("Niveau batterie : " + String(bat_level()));
			else if(buffer == "straight") set_vitesse_mot(MAX_SPEED_LEFT, MAX_SPEED_RIGHT);
			else if(buffer == "stop") set_vitesse_mot(0);
			else if(buffer == "back") set_vitesse_mot(-MAX_SPEED_LEFT, -MAX_SPEED_RIGHT);
			else if(buffer == "speed") {
				commande = Serial.readStringUntil(';').toInt();
				set_vitesse_mot((commande/100.0)*MAX_SPEED_LEFT, (commande/100.0)*MAX_SPEED_RIGHT);
			}
			else if(buffer == "speedO") {
				commandeG = Serial.readStringUntil(';').toInt();
				commandeD = Serial.readStringUntil(';').toInt();
				set_vitesse_mot((commandeG/100.0)*MAX_SPEED_LEFT, (commandeD/100.0)*MAX_SPEED_RIGHT);
			}
			

			
		}
		else Serial.read();
	}
	
	delay(50);
	
}

