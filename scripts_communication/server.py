# coding: utf-8 

import socket
import threading

class ClientThread(threading.Thread):

	def __init__(self, ip, port, clientsocket, labyrinthe):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		self.labyrinthe = labyrinthe
		self.bat_level = 100
		
	def run(self): 
	
		while True:
			self.recevoir()
			self.donnerOrdre("straight")
	
	def recevoir(self):
		r = self.clientsocket.recv(2048)
		print(r)
		self.traiter(r)
		
	
	def donnerOrdre(self,ordre):
		self.clientsocket.send(ordre)
		resultat = self.clientsocket.recv(2048)
		print(resultat)
		
		
	def traiter(self,recu):
		l = recu.split("\n")
		if l[0] == "DIRECTION?":
			X = float(l[1].split(" : ")[1])
			Y = float(l[2].split(" : ")[1])
			coord = (X,Y)
			print(coord)
			self.bat_level = float(l[6].split(" : ")[1])
			print(self.bat_level)
			self.labyrinthe.add_node(coord,0)
			print(self.labyrinthe.getNodes())