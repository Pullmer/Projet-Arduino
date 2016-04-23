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
        self.serialArduino.flushInput() # Vide le port série
        self.checkSerialCom()
        
    #----------------------------------------------------------------------
    def checkSerialCom(self):
        """Teste la communication serial"""
        while("pong" not in self.Read()): # Attente d'une réponse de l'aduino
                self.Send("#ping;")
                print("Ping sent...")
                time.sleep(0.2)
                
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

    #----------------------------------------------------------------------
    def waitMsg(self, timeout=3):
        """Attend qu'un message arrive"""
        debut = time.time()
        while not (self.serialArduino.inWaiting() > 0) and (time.time() - debut) < timeout:
            time.sleep(0.1)
    
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.serialArduino.close()
        print("Serial port closed")