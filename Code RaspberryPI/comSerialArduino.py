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
import qrCodeDecoder

########################################################################
class SerialArduino(threading.Thread):
    """Classe qui gère la communication Serial Arduino, hérite de thread"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        threading.Thread.__init__(self) # Initialisation du thread
        self.kill_received = False # Variable destruction du thread
        self.instanceSock = None # Instance communication socket
        self.serialArduino = serial.Serial('/dev/ttyACM0', 115200) # Ouverture port série
        self.serialArduino.flushInput() # Vide le port série
        self.checkSerialCom() # Vérification de la communication
        self.qrReader = qrCodeDecoder.QRDecode()
        print("Connected to arduino")

    #----------------------------------------------------------------------
    def setInstanceSocket(self, s):
        """Lien vers l'instance du socket pour envoyer des données vers le PC"""
        self.instanceSock = s

    #----------------------------------------------------------------------
    def run(self):
        """Boucle thread"""
        while not self.kill_received:
            a = self.Read() # Lecture des données venant de l'Arduino
            if a is not "":
                self.processData(a)

        print("Thread arduino killed !")

    #----------------------------------------------------------------------
    def checkSerialCom(self):
        """Teste la communication serial"""
        while("pong" not in self.Read()): # Attente d'une réponse de l'aduino
            self.Send("#ping;")
            print("Ping sent...")
            time.sleep(0.5)

        print("Received pong !")

    #----------------------------------------------------------------------
    def Send(self, data):
        """Envoie data sur le port série de l'arduino"""
        try:
            if len(data) > 0 and data is not None:
                self.serialArduino.write(data) # Ecriture des données sur le port série
        except:
            print("Erreur transmission serie !") # Fermeture du thread en cas d'erreur
            self.kill_received = True

    #----------------------------------------------------------------------
    def Read(self):
        """Lit données venant de l'arduino"""
        try:
            if(self.serialArduino.inWaiting() > 0):
                time.sleep(0.05) # On attend que les trames arrivent entièrement
                return self.serialArduino.read(self.serialArduino.inWaiting())
            return ""
        except:
            print("Erreur lecture port serie !") # Fermeture du thread en cas d'erreur
            self.kill_received = True

    #----------------------------------------------------------------------
    def processData(self, r):
        """Fonction traitement des données venant de l'arduino"""
        if len(r) > 0:
            print("Reception donnees venant de l'arduino : " + str(r))

            # Les commandes préalablements définies sont traitées ici
            data = r.split('#')
            for i in data:
                if "bat_level" in i:
                    self.instanceSock.Send("Batterie : " + i[i.find(':') + 1:i.find(';')] + "\n")
                elif "lowbat" in i:
                    self.instanceSock.Send("LOW_BAT" + "\n")
                elif "obstacledetected" in i:
                    self.instanceSock.Send("OBSTACLE_DETECTED" + "\n")
                elif "obstacleleft" in i:
                    self.instanceSock.Send("OBSTACLE_LEFT" + "\n")
                elif "pong" in i:
                    self.instanceSock.Send("PONG" + "\n")
                elif "lignedetected" in i:
                    self.instanceSock.Send("LINE_DETECTED" + "\n")
                    time.sleep(1)
                    dataQR = self.qrReader.decodeQRCode() # Lecture du QRCODE codé sous la forme : "X0;Y0;E" ou "X52;Y1;N" par exemple
                    while 'X' not in dataQR and not self.kill_received:
                        print("Erreur lecture QRCode, retry...") # En cas d'échec on ré-essaye en boucle
                        dataQR = self.qrReader.decodeQRCode()
                    coordX = dataQR[dataQR.find('X') + 1:dataQR.find(';')] # Extraction X
                    coordY = dataQR[dataQR.find('Y') + 1:dataQR.find(';', dataQR.find('Y'))] # Extraction Y
                    print("CoordX : {0} et CoordY : {1}".format(coordX, coordY)) # Affichage

                    # Envoi des informations du QRCode à l'ordinateur
                    buffer = "DIRECTION?\n" +  "X : " + coordX + "\n" + "Y : " + coordY + "\n"
                    buffer += "Est : OUI" + "\n" if 'E' in dataQR else "Est : NON" + "\n"
                    buffer += "Nord : OUI" + "\n" if 'N' in dataQR else "Nord : NON" + "\n"
                    buffer += "Ouest : OUI" + "\n" if 'O' in dataQR else "Ouest : NON" + "\n"
                    buffer += "Sud : OUI" + "\n" if 'S' in dataQR else "Sud : NON" + "\n"
                    print(buffer)
                    self.instanceSock.Send(buffer)

    #----------------------------------------------------------------------
    def close(self):
        """Fermeture du port série et qrReader"""
        self.serialArduino.close()
        self.qrReader.close()
        print("Serial port and qrReader closed")
