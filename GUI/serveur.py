# coding: utf-8 

import socket
import threading
from server import *

# classe qui reçoit et envoie des données aux robots
# nouvelle tache lancée à chaque connexion d'un robot
class Serveur(threading.Thread):

	def __init__(self,controller,labyrinthe):
		threading.Thread.__init__(self)   # on appelle le constructeur de la classe Thread
		
		# configuration du socket
		self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.tcpsock.settimeout(1)
		
		self.tcpsock.bind(("",1111))    # on ecoute sur le port 1111
		self.labyrinthe = labyrinthe    # reference vers le labyrinthe
		self.controller = controller    # reference vers le controleur
		self.terminer = False           # booléen indiquant la fin de l'écoute
	
	# code executé par le Thread
	def run(self): 
		while (not self.terminer):
			try:
				self.tcpsock.listen(1)
				(clientsocket, (ip, port)) = self.tcpsock.accept()   # on accepte la connexion d'un robot
				clientsocket.settimeout(0.01)
				semSocket = threading.Semaphore(value=1)    # sémaphore protégeant de l'utilisation simultanée du socket de communication avec le robot
				ordreDirect = OrdreDirect(clientsocket,semSocket)  # s'occupe des ordres qui ne sont pas des réponses
				newthread = ClientThread(ip, port, clientsocket, self.labyrinthe,self.controller,semSocket,ordreDirect)  # création d'un Thread qui s'occupera de la communication avec le robot
				newthread.start()  #on lance le Thread
			except:
				pass
	
	# action à effectuer avant de quitter le logiciel
	def eteindre(self):
		self.tcpsock.close()
		self.terminer = True