#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire communication socket (client)
  Created: 23/04/2016
"""

import comSocket
import comSerialArduino

host = '10.0.0.5'
port = 1111

#----------------------------------------------------------------------
def main():
    """Main function"""
    
    try:
        sock = comSocket.Com(host, port) # Instance communication socket
        ardu = comSerialArduino.SerialArduino() # Instance communcation serial
        sock.setInstanceArduino(ardu)
        ardu.setInstanceSocket(sock)
        sock.start() # Démarrage thread
        ardu.start() # Démarrage thread

        while True:
            pass # Boucle infinie pour tester le fonctionnement des threads...
            
    except Exception as e:
        print(str(e))
        
    finally:
        sock.join()
        ardu.join()
        sock.close()
        ardu.close()

if __name__ == '__main__':
    main()
