#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire communication entre Arduino et PC
  Created: 23/04/2016
"""

import comSocket
import comSerialArduino

host = '10.0.0.5'
port = 1111

#----------------------------------------------------------------------
def main():
    """Main function"""
    sock = comSocket.Com(host, port) # Instance communication socket
    ardu = comSerialArduino.SerialArduino() # Instance communication serial

    try:
        sock.setInstanceArduino(ardu)
        ardu.setInstanceSocket(sock)
        sock.start() # Démarrage thread
        ardu.start() # Démarrage thread

        while not sock.kill_received and not ardu.kill_received:
            pass # Boucle infinie pour tester le fonctionnement des threads...

    except Exception as e:
        print(str(e)) # Si il y a interruption de la communication on ferme le port série et le socket
        sock.kill_received = True
        ardu.kill_received = True

    finally:
        sock.join()
        ardu.join()
        sock.close()
        ardu.close()

if __name__ == '__main__':
    main()
