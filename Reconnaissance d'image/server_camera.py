#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Serveur pour envoyer le flux vidéo sur le réseau
  Created: 15/02/2016
"""

import socket

########################################################################
class CameraDebugServer:
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, port = 8123):
        """Constructor"""
        self.TCP_IP = ''
        self.TCP_PORT = port
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(True)
        self.conn, self.addr = self.s.accept()
        print("socket ouvert")

    #----------------------------------------------------------------------
    def sendData(self, image):
        """Transmission du flux vidéo sur le réseau"""
        self.conn.send(str(len(image)).ljust(16))
        self.conn.send(image)        

    #----------------------------------------------------------------------
    def __del__(self):
        """Lorsque la classe se ferme on close le socket"""
        print("socket closed")
        self.s.close()



