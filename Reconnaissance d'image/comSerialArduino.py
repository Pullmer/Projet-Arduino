#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Bibliothèque fonction communication serial
  Created: 13/03/2016
"""

import serial
import time
import threading

########################################################################
class SerialArduino(threading.Thread):
    """Classe qui gère la com Serial Arduino, hérite de thread"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        threading.Thread.__init__(self) # Initialisation du thread
        self.instanceSock = None # Instance communication socket
        self.serialArduino = serial.Serial('/dev/ttyACM0', 115200) # Ouverture port série
        self.serialArduino.flushInput() # Vide le port série
        self.checkSerialCom() # Vérification de la communication
        print("Connected to arduino")
    
    #----------------------------------------------------------------------
    def setInstanceSocket(self, s):
        """Lien vers l'instance du socket"""
        self.instanceSock = s
    
    #----------------------------------------------------------------------
    def run(self):
        """Boucle thread"""
        while True:
            a = self.Read()
            if a != "":
                self.processData(a)
        
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
        if data:
            try:
                self.serialArduino.write(data)
            except:
                print("Problème port série !")
    
    #----------------------------------------------------------------------
    def Read(self):
        """Lit données venant de l'arduino"""
        return self.serialArduino.read(self.serialArduino.inWaiting()) if(self.serialArduino.inWaiting() > 0) else ""

    #----------------------------------------------------------------------
    def processData(self, data):
        """Fonction traitement des données venant de l'arduino"""
        print("reception donnees arduino : " + str(data))
        if self.instanceSock is not None:
            self.instanceSock.Send(data)
        
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.serialArduino.close()
        print("Serial port closed")
        