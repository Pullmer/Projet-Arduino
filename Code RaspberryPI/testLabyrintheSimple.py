#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test parcours labyrinthe simple
"""

import comSerialArduino
import comSocket
import time

host = '10.0.0.8'
port = 1111

#----------------------------------------------------------------------
def main():
    """Fonction principale"""
    sock = comSocket.Com(host, port) # Instance communication socket
    ardu = comSerialArduino.SerialArduino() # Instance communcation serial

    try:
        sock.setInstanceArduino(ardu)
        ardu.setInstanceSocket(sock)
        sock.start() # Démarrage thread
        ardu.start() # Démarrage thread

        while not sock.kill_received and not ardu.kill_received:
            time.sleep(0.5) # Boucle infinie (les threads de communication Serial et Socket continuent de fonctionner)

    except Exception as e:
        print(str(e)) # Si il y a interruption de la communication on ferme le port série et le socket
        sock.kill_received = True
        ardu.kill_received = True

    finally:
        sock.kill_received = True
        ardu.kill_received = True
        sock.join()
        ardu.join()
        sock.close()
        ardu.close()


if __name__ == '__main__':
    main()
