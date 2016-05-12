# -*- coding: utf-8 -*-

from ecran import *
from labyrinthe import *
from serveur import *
import Queue
import time

class Controller:
	
	# constructeur de classe
	def __init__(self,fenetre):
			self.fenetre = fenetre   # référence vers la fenetre d'affichage
			self.queue = Queue.Queue()  # création de la file d'attente des tâches à faire quand on raffraichit l'écran
			self.labyrinthe = Labyrinthe(self)   # création du graphe du labyrinthe
			self.robots = {1:None , 2:None, 3:None}    # dictionnaire des robots (id : robot)
			self.serveur = Serveur(self,self.labyrinthe) # création du serveur d'écoute
			self.ecran = Ecran(self,fenetre,self.queue)   # création de l'objet qui contiendra les éléments contenus dans fenètre
			
			
			self.periodicCall()
			
	# raffraichissement de l'écran
	def periodicCall(self):
		self.ecran.rafraichirEcran()   # on raffraichit l'écran d'affichage
		self.fenetre.after(50,self.periodicCall)   # on le fait toutes les 50 ms

	
	# on souhaite mémoriser le chemin parcouru par un robot, afin de l'afficher
	def dessinerCheminParcouru(self,robot,ancienne_position,nouvelle_position):
		for cle in self.robots.keys():
			if self.robots.get(cle) == robot:
				id = cle
				break
		# on met les infos dans la file d'attente
		self.queue.put("chemin")
		self.queue.put(id)
		self.queue.put(ancienne_position)
		self.queue.put(nouvelle_position)
		
	# on modifie le dictionnaire des robots à chaque connexion d'un nouveau robot
	def ajouterRobot(self,robot):
		id = 0
		for cle in self.robots.keys():
			if self.robots.get(cle) == None:
				id = cle
				self.robots[cle] = robot
				break
		self.queue.put("nouveau robot")
		self.queue.put(id)
		
	# permet de récupérer les infos relatives à un robot afin de les afficher grâce à la file d'attente
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
		
	# on lance le serveur d'écoute des connexions
	def lancerServeur(self):
		self.serveur.start()
		
	# demande l'arret d'un robot d'identifiant donné
	def pause(self,id):
		self.robots.get(id).stop()
		
	# demande le départ d'un robot d'identifiant donné
	def lancer_robot(self,id):
		self.robots.get(id).go()
			
	# retourne les coordonnées des carrefours adjacents à un carrefour de coordonnées données
	def getAdjacents(self,coords):
		return self.labyrinthe.getNoeudsAdjacents(coords)
		
	# prise en compte et notification à l'interface graphique de la déconnexion d'un robot grâce à la file d'attente
	def deconnexion(self, robot):
		id = 0
		for cle in self.robots.keys():
			if self.robots.get(cle) == robot:
				id = cle
				self.robots[cle] = None
				break
		self.queue.put("deconnexion")
		self.queue.put(id)
		
	# on donne un ordre de navigation vers une destination précise à un robot d'identifiant donné
	def aller(self, id, destination):
		print("changement de mode du robot "+ str(id))
		robot = self.robots.get(id)
		robot.naviguer(destination)
		robot.go()
			
	# retourne une description d'un carrefour de coordonnées données
	def voirInfosIntersection(self,position):
		analyse = self.labyrinthe.analyserIntersection(position)
		texte = "L'intersection est à la position :" + str(position) +'\n'
		texte += "Il y a "+str(analyse[0])+" chemin(s).\n"
		texte += "Il y a "+str(analyse[1])+" chemin(s) qui n'ont pas été explorés.\n"
		return texte
		
	# précise si un robot d'identifiant donné est connecté ou non
	def isConnected(self,id):
		if self.robots.get(id) == None:
			return False
		return True
		
	# retourne l'état d'un robot d'identifiant donné (ex : ready,working,pause)
	def getEtatRobot(self,id):
		return self.robots.get(id).getState()
		
	# précise si des robots sont connectés ou non
	def connexionsEtablies(self):
		for cle in self.robots.keys():
			if self.robots.get(cle) != None:
				return True
		return False
		
	# éteint le serveur d'écoute des connexions afin de quitter le logiciel
	def quitter(self):
		self.serveur.eteindre()