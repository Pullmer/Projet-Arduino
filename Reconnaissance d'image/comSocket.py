#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Librairie pour la communication socket
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
        self.kill_received = False
        self.instanceArduino = None # Instance communication arduino
        self.ip = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("Socket connected to " + host + ":" + str(port))
    
    #----------------------------------------------------------------------
    def setInstanceArduino(self, a):
        """"""
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
            r = self.sock.recv(2048)
            return r
        except:
            print("Erreur lecture socket !")
            self.kill_received = True
            self.instanceArduino.kill_received = True
    
    #----------------------------------------------------------------------
    def Send(self, data):
        """Fonction qui envoie les données vers le pc"""
        try:
            if len(data) > 0 and data is not None:
                self.sock.send(data)
        except:
            print("Erreur transmission socket !")
            self.kill_received = True
            self.instanceArduino.kill_received = True
    
    #----------------------------------------------------------------------
    def processData(self, r):
        """Fonction traitement données venant du pc"""
        if len(r) > 0:
            print("Reception donnees venant du socket : " + str(r))
            
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
        """"""
        self.sock.close()
        print("Socket " + self.ip + ":" + str(self.port) + " closed")
        