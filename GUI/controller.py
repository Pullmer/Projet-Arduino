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
			self.serveur = Serveur(self,self.labyrinthe)
			self.ecran = Ecran(self,fenetre,self.queue)
			
			
			self.serveur.start()
			self.periodicCall()
			
	def periodicCall(self):
		self.ecran.rafraichirEcran()
		self.fenetre.after(50,self.periodicCall)

	def dessinerCheminParcouru(self,ancienne_position,nouvelle_position):
		self.queue.put("chemin")
		self.queue.put(ancienne_position)
		self.queue.put(nouvelle_position)