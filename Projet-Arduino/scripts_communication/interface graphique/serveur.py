# coding: utf-8 

import socket
import threading
from server import *

# classe qui reçit et envoie des données aux robots
# nouvelle tache lancée à chaque connexion d'un robot
class Serveur(threading.Thread):

	def __init__(self,controller,labyrinthe):
		threading.Thread.__init__(self)
		self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.tcpsock.bind(("",1111))
		self.labyrinthe = labyrinthe
		self.controller = controller
		
	def run(self): 
		while True:
			self.tcpsock.listen(10)
			(clientsocket, (ip, port)) = self.tcpsock.accept()
			self.controller.indiquerConnexion()
			newthread = ClientThread(ip, port, clientsocket, self.labyrinthe)
			newthread.start()
			
		
	
	