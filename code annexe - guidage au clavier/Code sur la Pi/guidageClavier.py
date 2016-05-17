#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Cyprien
  Purpose: Partie client (sur Pi) du guidage du robot au clavier
  Created: 13/03/2016
"""

import comSerialArduino
import comSocket

host = 'localhost'
port = '1111'


#----------------------------------------------------------------------
def main():
    """Main function"""
    try:
        sock = comSocket.Com(host, port) # creation du socket de communication avec le PC
        ardu = comSerialArduino.SerialArduino() # creation de la communication serial avec l'arduino
        sock.setInstanceArduino(ardu) #creation des liens entre communication socket et communication serial
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
