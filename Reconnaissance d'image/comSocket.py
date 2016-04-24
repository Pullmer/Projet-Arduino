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
        threading.Thread.__init__(self)
        self.instanceArduino = None
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
        while True:
            r = self.Read()
            self.processData(r)
    
    #----------------------------------------------------------------------
    def Read(self):
        """Fonction qui reçoit les données venant du pc"""
        r = self.sock.recv(2048)
        return r
    
    #----------------------------------------------------------------------
    def Send(self, data):
        """Fonction qui envoie les données vers le pc"""
        self.sock.send(data)
    
    #----------------------------------------------------------------------
    def processData(self, data):
        """Fonction traitement données venant du pc"""
        print("reception donnees venant du socket : " + str(data))
        if self.instanceArduino is not None:
            self.instanceArduino.Send(data)
        
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.sock.close()
        print("Socket " + self.ip + ":" + str(self.port) + " closed")
        