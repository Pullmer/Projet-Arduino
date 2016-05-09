import Tkinter
from Tkinter import *

class Dessin(Tkinter.Canvas):

	def __init__(self, fenetre, largeur, hauteur, couleur):
			Tkinter.Canvas.__init__(self,fenetre,width=largeur,height=hauteur,background=couleur)
			self.points = {1:None,2:None,3:None}
			self.couleurs = {1:'red',2:'blue',3:'green'}
			self.taille_points = 8
			self.curseur_utilise = False
			self.position_curseur = (0,0)
	

	def creerLigne(self,coord1,coord2,epaisseur):
		self.create_line(coord1[0], coord1[1], coord2[0], coord2[1],width=epaisseur)
		
	def creerPoint(self,id):
		couleur = self.couleurs.get(id)
		point = self.create_oval(200-self.taille_points,400-self.taille_points,200+self.taille_points,400+self.taille_points,fill=couleur)
		self.points[id] = point
		
	def deplacerPoint(self,id,coord):
		self.coords(self.points[id],coord[0]-self.taille_points,coord[1]-self.taille_points,coord[0]+self.taille_points,coord[1]+self.taille_points)
		
	def effacerPoint(self,id):
		point = self.points.get(id)
		self.delete(point)
		self.points[id] = None
		
	def curseurUtilise(self):
		return self.curseur_utilise
		
	def afficherCurseur(self):
		self.curseur = self.create_oval(200-self.taille_points,400-self.taille_points,200+self.taille_points,400+self.taille_points,fill='black')
		self.curseur_utilise = True
	
	def effacerCurseur(self):
		self.delete(self.curseur)
		self.curseur_utilise = False
		self.position_curseur = (0,0)
	
	def deplacerCurseur(self,position):
		X = int(30*position[0]+200)
		Y = int(-30*position[1]+400)
		coord = (X,Y)
		self.coords(self.curseur,coord[0]-self.taille_points,coord[1]-self.taille_points,coord[0]+self.taille_points,coord[1]+self.taille_points)
		self.position_curseur = position
		
	def getPositionCurseur(self):
		return self.position_curseur