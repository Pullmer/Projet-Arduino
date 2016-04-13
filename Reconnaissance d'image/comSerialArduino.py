#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Bibliothèque fonction communication serial
  Created: 13/03/2016
"""

import serial
import time

########################################################################
class SerialArduino:
    """Classe qui gère la com Serial Arduino"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.serialArduino = serial.Serial('/dev/ttyACM0', 115200) # Ouverture port série
        time.sleep(1)
        self.serialArduino.flushInput() # Vide le port série
        self.checkSerialCom()
        
    #----------------------------------------------------------------------
    def checkSerialCom(self):
        """Teste la communication serial"""
        while("pong" not in self.Read()): # Attente d'une réponse de l'aduino
                self.Send("#ping;")
                print("Ping sent...")
                time.sleep(0.5)
                
        print("Received pong")
        
    #----------------------------------------------------------------------
    def Send(self, data):
        """Envoie data sur le port série de l'arduino"""
        try:
            self.serialArduino.write(data)        
        except:
            print("Problème port série !")
    
    #----------------------------------------------------------------------
    def Read(self):
        """Lit données venant de l'arduino"""
        return self.serialArduino.read(self.serialArduino.inWaiting()) if(self.serialArduino.inWaiting() > 0) else ""
