# coding: utf-8 

import socket
import threading
from robot import *

# classe qui reçoit et envoie des données aux robots
# nouvelle tache lancée à chaque connexion d'un robot
class ClientThread(threading.Thread):

	def __init__(self, ip, port, clientsocket, labyrinthe,controller):
		threading.Thread.__init__(self)    #on appelle le constructeur de la classe Thread
		self.clientsocket = clientsocket   #socket de communication avec un robot
		self.deconnexion = False
		self.robot = Robot(self,ip, port,labyrinthe,controller)   # on instancie un objet de la classe robot
		
	#code executé par le Thread
	def run(self): 
	
		while True:
			if self.deconnexion:
				self.clientsocket.close()
				break
			try:
				self.recevoir()
			except:
				self.robot.erreur()
	
	# méthode qui s'occupe de la reception des données
	def recevoir(self):
		r = self.clientsocket.recv(2048)
		self.robot.traiter(r)   #on traite la chaine de caractères reçue
		
	
	#méthode qui envoie une chaine de caractère à un robot
	def envoyer(self,ordre):
		self.clientsocket.send(ordre)
	
	def fermer(self):
		self.deconnexion = True
		print("fin connexion")