from ecran import *
from labyrinthe import *
from serveur import *
import Queue
import time

class Controller:
	def __init__(self,fenetre):
			self.fenetre = fenetre
			self.queue = Queue.Queue()
			self.labyrinthe = Labyrinthe(self)
			self.robots = []
			self.serveur = Serveur(self,self.labyrinthe)
			self.ecran = Ecran(self,fenetre,self.queue)
			
			
			self.periodicCall()
			
	def periodicCall(self):
		self.ecran.rafraichirEcran()
		self.fenetre.after(50,self.periodicCall)

	def dessinerCheminParcouru(self,robot,ancienne_position,nouvelle_position):
		id = 0
		while self.robots[id] != robot:
			id = id+1
		self.queue.put("chemin")
		self.queue.put(id)
		self.queue.put(ancienne_position)
		self.queue.put(nouvelle_position)
		
	def ajouterRobot(self,robot):
		self.robots.append(robot)
		self.queue.put("nouveau robot")
		
	def details(self,id):
		try:
			robot = self.robots[id-1]
			ip = robot.getIP()
			position = robot.getPosition()
			batterie = robot.getBatterie()
			self.queue.put("details")
			self.queue.put(id)
			self.queue.put(ip)
			self.queue.put(position)
			self.queue.put(batterie)
		except IndexError:
			self.queue.put("details")
			self.queue.put("erreur")
		
	def lancerServeur(self):
		self.serveur.start()
		
	def pause(self):
		for robot in self.robots:
			robot.stop()