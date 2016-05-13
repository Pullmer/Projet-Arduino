#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Serveur pour envoyer le flux vidéo de la caméra sur le réseau
  Created: 15/02/2016
"""

import socket

########################################################################
class CameraDebugServer:
    """Classe permettant l'envoi d'un flux vidéo sur le réseau"""

    #----------------------------------------------------------------------
    def __init__(self, port = 8123):
        """Constructor"""
        self.TCP_PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création du socket
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        self.s.listen(True)
        self.conn, self.addr = self.s.accept() # Connexion du client
        print("Socket ouvert")

    #----------------------------------------------------------------------
    def sendData(self, data):
        """Transmission de data sur le réseau"""
        try:
            self.conn.send(str(len(data)).ljust(16))
            self.conn.send(data)
        except:
            print("Interruption du socket, en attente...")
            CameraDebugServer.__init__(self)

    #----------------------------------------------------------------------
    def close(self):
        """Lorsque la classe se ferme on ferme le socket"""
        self.s.close()
        print("Socket closed")
        