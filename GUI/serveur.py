# coding: utf-8 

import socket
import threading
from server import *

# classe qui reçit et envoie des données aux robots
# nouvelle tache lancée à chaque connexion d'un robot
class Serveur(threading.Thread):

	def __init__(self,controller,labyrinthe):
		threading.Thread.__init__(self)   #on appelle le constructeur de la classe Thread
		self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.tcpsock.bind(("",1111))    #on ecoute sur le port 1111
		self.labyrinthe = labyrinthe    #reference vers le labyrinthe
		self.controller = controller    #reference vers le controleur
	
	#code executé par le Thread
	def run(self): 
		while True:
			self.tcpsock.listen(10)
			(clientsocket, (ip, port)) = self.tcpsock.accept()   #on accepte la connexion d'un robot
			newthread = ClientThread(ip, port, clientsocket, self.labyrinthe,self.controller)  #création d'un Thread qui s'occupera de la communication avec le robot
			newthread.start()  #on lance le Thread
			
		
	
	