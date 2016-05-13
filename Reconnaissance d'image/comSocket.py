#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Librairie pour la communication socket sur la RaspberryPi
  Created: 23/04/2016
"""

import socket
import threading

########################################################################
class Com(threading.Thread):
    """Classe qui gère la communication socket, hérite de thread"""

    #----------------------------------------------------------------------
    def __init__(self, host, port):
        """Constructor"""
        threading.Thread.__init__(self) # Initialisation du thread
        self.kill_received = False # Destruction du thread
        self.instanceArduino = None # Instance communication arduino
        self.ip = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Définition du socket
        self.sock.connect((host, port)) # Connexion au socket
        print("Socket connected to " + host + ":" + str(port))
    
    #----------------------------------------------------------------------
    def setInstanceArduino(self, a):
        """Permet l'envoi des messages à l'Arduino via le port série"""
        self.instanceArduino = a
        
    #----------------------------------------------------------------------
    def run(self):
        """Code exécuté par le thread"""
        while not self.kill_received:
            r = self.Read()
            if r is not None:
                self.processData(r)
                
        print("Thread socket killed !")
    
    #----------------------------------------------------------------------
    def Read(self):
        """Fonction qui reçoit les données venant du pc"""
        try:
            r = self.sock.recv(2048) # Attente réception données venant du socket
            return r
        except:
            print("Erreur lecture socket !") # Problème de liaison, fermeture du socket
            self.kill_received = True
            self.instanceArduino.kill_received = True
    
    #----------------------------------------------------------------------
    def Send(self, data):
        """Fonction qui envoie les données vers le pc"""
        try:
            if len(data) > 0 and data is not None:
                self.sock.send(data) # Envoi des données
        except:
            print("Erreur transmission socket !")
            self.kill_received = True
            self.instanceArduino.kill_received = True
    
    #----------------------------------------------------------------------
    def processData(self, r):
        """Fonction traitement données venant du pc via le socket"""
        if len(r) > 0:
            print("Reception donnees venant du socket : " + str(r))
            
			# Les commandes préalablements définies sont traitées ici
            data = r.split('#')
            for i in data:
                if "bat_level" in i:
                    self.instanceArduino.Send("#bat_level;")
                elif "pause" in i:
                    self.instanceArduino.Send("#pause;")
                elif "ping" in i:
                    self.instanceArduino.Send("#ping;")
                elif "droite" in i:
                    self.instanceArduino.Send("#droite;")
                elif "gauche" in i:
                    self.instanceArduino.Send("#gauche;")
                elif "face" in i:
                    self.instanceArduino.Send("#face;")
                elif "demi" in i:
                    self.instanceArduino.Send("#turnback;")
                elif "workcompleted" in i:
                    self.instanceArduino.Send("#finish;")
        
    #----------------------------------------------------------------------
    def close(self):
        """Fermeture du socket"""
        self.sock.close()
        print("Socket " + self.ip + ":" + str(self.port) + " closed")
        