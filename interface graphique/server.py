# coding: utf-8 

import socket
import threading
from robot import *

# classe qui reçit et envoie des données aux robots
# nouvelle tache lancée à chaque connexion d'un robot
class ClientThread(threading.Thread):

	def __init__(self, ip, port, clientsocket, labyrinthe):
		threading.Thread.__init__(self)
		self.clientsocket = clientsocket
		self.robot = Robot(self,ip, port,labyrinthe)
		
	def run(self): 
	
		while True:
			self.recevoir()
	
	def recevoir(self):
		r = self.clientsocket.recv(2048)
		self.robot.traiter(r)
		
	
	def envoyer(self,ordre):
		self.clientsocket.send(ordre)
	