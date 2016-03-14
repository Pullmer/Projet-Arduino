# coding: utf-8 

import serial
import time
import socket

TCP_PORT = 1111
BUFFER_SIZE = 1024

m1=0
m2=0

#initialisation de la communication série
ser = serial.Serial('/dev/ttyACM0',115200)

#initialisation de la communication wifi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("",TCP_PORT))



print("Recherche d'une connexion...")

sock.listen(10)

(clientsocket, (ip, port)) = sock.accept()

print("Connecte a "+str(ip)+" sur le port "+str(port)+ "!")



while True:
	
	#attente d'une commande de l'ordinateur

	print("Listening...")

	data = clientsocket.recv(BUFFER_SIZE)

	print('Message recu : '+ data )

        if data=='':
                continue

	
	#traitement de la commande

        for word in data.split(':'):

                print("Mot envoye a arduino :"+word)

                ser.write(word)
                
        time.sleep(0.05)
	

