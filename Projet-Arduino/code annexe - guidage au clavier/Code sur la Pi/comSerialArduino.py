#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Bibliothèque fonction communication serial avec la carte Arduino
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
        self.kill_received = False # Destruction du thread
        self.instanceSock = None # Instance communication socket
        self.serialArduino = serial.Serial('/dev/ttyACM0', 115200) # Ouverture port série
        self.serialArduino.flushInput() # Vide le port série
        
    #----------------------------------------------------------------------
    def setInstanceSocket(self, s):
        """Lien vers l'instance du socket pour envoyer des données vers le PC"""
        self.instanceSock = s

    #----------------------------------------------------------------------
    def run(self):
        """Boucle thread"""
        if self.checkSerialCom():
            print("Connected to arduino")
        
        while not self.kill_received:
            a = self.Read() # Lecture des données venant de l'Arduino
            if a is not "":
                self.processData(a)

        print("Thread arduino killed !")

    #----------------------------------------------------------------------
    def checkSerialCom(self):
        """Teste la communication serial"""

        pingCounter = 0
        
        while(("pong" not in self.Read()) and (pingCounter<50)): # Attente d'une réponse de l'arduino
            self.Send("#ping;")
            pingCounter=pingCounter+1
            print("Ping sent...")
            time.sleep(0.2)
            
        if (pingCounter>=50):
            print("Ping test failed after 50 retries")
            self.kill_received = True
            if self.instanceSock is not None:
                self.instanceSock.kill_received = True
            return False
        else:
            print("Received pong !")
            return True

    #----------------------------------------------------------------------
    def Send(self, data):
        """Envoie data sur le port série de l'arduino"""

        try:
            if len(data) > 0 and data is not None:
                print("Ecriture des données suivantes sur le port série : "+data)
                self.serialArduino.write(data) # Ecriture des données sur le port série
        except:
            print("Erreur transmission serie !") # Fermeture du thread en cas d'erreur
            self.kill_received = True
            self.instanceSock.kill_received = True

    #----------------------------------------------------------------------
    def Read(self):
        """Lit données venant de l'arduino"""
        try:
            return self.serialArduino.read(self.serialArduino.inWaiting()) if(self.serialArduino.inWaiting() > 0) else ""
        except:
            print("Erreur lecture port serie !") # Fermture du thread en cas d'erreur
            self.kill_received = True
            self.instanceSock.kill_received = True

    #----------------------------------------------------------------------
    def processData(self, r):
        """Fonction traitement des données venant de l'arduino"""
        if len(r) > 0:
            print("Reception donnees venant de l'arduino : " + str(r))

            # Les commandes préalablements définies sont traitées ici
            data = r.split('#')
            for i in data:
                if "bat_level" in i:
                    self.instanceSock.Send("Batterie : " + i[i.find(':') + 1:i.find(';')])
                elif "lowbat" in i:
                    self.instanceSock.Send("LOW_BAT")
                elif "obstacledetected" in i:
                    self.instanceSock.Send("OBSTACLE_DETECTED")
                elif "obstacleleft" in i:
                    self.instanceSock.Send("OBSTACLE_LEFT")
                elif "pong" in i:
                    self.instanceSock.Send("PONG")

    #----------------------------------------------------------------------
    def close(self):
        """Fermeture du port série"""
        self.serialArduino.close()
        print("Serial port closed")
