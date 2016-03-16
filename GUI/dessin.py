import Tkinter
from Tkinter import *

class Dessin(Tkinter.Canvas):

	def __init__(self, fenetre, largeur, hauteur, couleur):
			Tkinter.Canvas.__init__(self,fenetre,width=largeur,height=hauteur,background=couleur)
			self.points = []
			self.couleurs = ['red','blue','green']
			self.taille_points = 8

	def creerLigne(self,coord1,coord2,epaisseur):
		self.create_line(coord1[0], coord1[1], coord2[0], coord2[1],width=epaisseur)
		
	def creerPoint(self):
		couleur = self.couleurs[len(self.points)]
		point = self.create_oval(200-self.taille_points,400-self.taille_points,200+self.taille_points,400+self.taille_points,fill=couleur)
		self.points.append(point)
		
	def deplacerPoint(self,id,coord):
		self.coords(self.points[id],coord[0]-self.taille_points,coord[1]-self.taille_points,coord[0]+self.taille_points,coord[1]+self.taille_points)