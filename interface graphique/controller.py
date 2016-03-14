from ecran import *
from serveur import *

class Controller:
	def __init__(self,labyrinthe):
			self.labyrinthe = labyrinthe
			self.serveur = Serveur(self,labyrinthe)
			
	def lancerServeur(self):
		self.serveur.start()
		
	def indiquerConnexion(self):
		self.ecran.connexion()
		
	def ajouterEcran(self,ecran):
		self.ecran = ecran