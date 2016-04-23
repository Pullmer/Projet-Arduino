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
class ComSocket(threading.Thread):
    """Classe qui gère la com socket, hérite de thread"""

    #----------------------------------------------------------------------
    def __init__(self, host, port):
        """Constructor"""
        threading.Thread.__init__(self)
        self.ip = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("Socket connected to " + host + ":" + str(port))
        
    #----------------------------------------------------------------------
    def run(self):
        """Code exécuté par le thread"""
        while True:
            self.recevoir()
    
    #----------------------------------------------------------------------
    def recevoir(self):
        """Fonction qui reçoit les données"""
        r = self.sock.recv(2048)
        # traiter les données ici
        
    #----------------------------------------------------------------------
    def envoyer(self, data):
        """Fonction qui envoie les données"""
        self.sock.send(data)
        
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.sock.close()
        print("Socket " + self.ip + ":" + str(self.port) + " closed")
        