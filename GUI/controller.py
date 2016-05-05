# -*- coding: utf-8 -*-

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
			self.robots = {1:None , 2:None, 3:None}
			self.serveur = Serveur(self,self.labyrinthe)
			self.ecran = Ecran(self,fenetre,self.queue)
			
			
			self.periodicCall()
			
	def periodicCall(self):
		self.ecran.rafraichirEcran()
		self.fenetre.after(50,self.periodicCall)

	def dessinerCheminParcouru(self,robot,ancienne_position,nouvelle_position):
		for cle in self.robots.keys():
			if self.robots.get(cle) == robot:
				id = cle
				break
		self.queue.put("chemin")
		self.queue.put(id)
		self.queue.put(ancienne_position)
		self.queue.put(nouvelle_position)
		
	def ajouterRobot(self,robot):
		id = 0
		for cle in self.robots.keys():
			if self.robots.get(cle) == None:
				id = cle
				self.robots[cle] = robot
				break
		self.queue.put("nouveau robot")
		self.queue.put(id)
		
	def details(self,id):
		robot = self.robots.get(id)
		if robot != None:
			ip = robot.getIP()
			position = robot.getPosition()
			batterie = robot.getBatterie()
			self.queue.put("details")
			self.queue.put(id)
			self.queue.put(ip)
			self.queue.put(position)
			self.queue.put(batterie)
		else:
			self.queue.put("details")
			self.queue.put("erreur")
		
	def lancerServeur(self):
		self.serveur.start()
		
	def pause(self,id):
		self.robots.get(id).stop()
		
	def lancer_robot(self,id):
		self.robots.get(id).go()
			
	def getAdjacents(self,coords):
		return self.labyrinthe.getNoeudsAdjacents(coords)
		
	def deconnexion(self, robot):
		id = 0
		for cle in self.robots.keys():
			if self.robots.get(cle) == robot:
				id = cle
				self.robots[cle] = None
				break
		self.queue.put("deconnexion")
		self.queue.put(id)
		
	def changer_mode(self, id):
		print("changement de mode du robot "+ str(id))
		robot = self.robots.get(id)
		robot.setMode("navigation")
		robot.go()
			
	def voirInfosIntersection(self,position):
		analyse = self.labyrinthe.analyserIntersection(position)
		texte = "L'intersection est à la position :" + str(position) +'\n'
		texte += "Il y a "+str(analyse[0])+" chemin(s).\n"
		texte += "Il y a "+str(analyse[1])+" chemin(s) qui n'ont pas été explorés.\n"
		return texte
		
	def isConnected(self,id):
		if self.robots.get(id) == None:
			return False
		return True
		
	def getEtatRobot(self,id):
		return self.robots.get(id).getState()
		
	def connexionsEtablies(self):
		for cle in self.robots.keys():
			if self.robots.get(cle) != None:
				return True
		return False
		
	def quitter(self):
		self.serveur.eteindre()