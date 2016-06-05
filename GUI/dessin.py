# -*- coding: utf-8 -*-

"""
	Author : Nicolas Gonçalves
	Purpose : Zone de dessin du labyrinthe
"""


import Tkinter
from Tkinter import *

class Dessin(Tkinter.Canvas):

	# constructeur de classe
	def __init__(self, fenetre, largeur, hauteur, couleur):
			Tkinter.Canvas.__init__(self,fenetre,width=largeur,height=hauteur,background=couleur)
			self.points = {1:None,2:None,3:None}    # dictionnaire des points graphiques représentant les robots (id : point)
			self.couleurs = {1:'red',2:'blue',3:'green'}   # dictionnaire de couleur des points (id : couleur)
			self.taille_points = 8    # taille des points
			self.curseur_utilise = False    # booléen d'utilisation du curseur
			self.position_curseur = (0,0)    # coordonnées du curseur (position réelle)
	

	# création d'une ligne
	def creerLigne(self,coord1,coord2,epaisseur):
		self.create_line(coord1[0], coord1[1], coord2[0], coord2[1],width=epaisseur)
		
	# création d'un point d'identifiant donné
	def creerPoint(self,id):
		couleur = self.couleurs.get(id)
		point = self.create_oval(200-self.taille_points,400-self.taille_points,200+self.taille_points,400+self.taille_points,fill=couleur)
		self.points[id] = point
		
	# déplacement d'un point
	def deplacerPoint(self,id,coord):
		self.coords(self.points[id],coord[0]-self.taille_points,coord[1]-self.taille_points,coord[0]+self.taille_points,coord[1]+self.taille_points)
		
	# effacement d'un point
	def effacerPoint(self,id):
		point = self.points.get(id)
		self.delete(point)
		self.points[id] = None
		
	# retourne si le curseur est utilisé ou non
	def curseurUtilise(self):
		return self.curseur_utilise
		
	# affichage du curseur à sa création
	def afficherCurseur(self):
		self.curseur = self.create_oval(200-self.taille_points,400-self.taille_points,200+self.taille_points,400+self.taille_points,fill='black')
		self.curseur_utilise = True
	
	# effacement du curseur
	def effacerCurseur(self):
		self.delete(self.curseur)
		self.curseur_utilise = False
		self.position_curseur = (0,0)
	
	# déplacement du curseur
	def deplacerCurseur(self,position):
		X = int(30*position[0]+200)
		Y = int(-30*position[1]+400)
		coord = (X,Y)
		self.coords(self.curseur,coord[0]-self.taille_points,coord[1]-self.taille_points,coord[0]+self.taille_points,coord[1]+self.taille_points)
		self.position_curseur = position
		
	# retourne les coordonnées du curseur
	def getPositionCurseur(self):
		return self.position_curseur