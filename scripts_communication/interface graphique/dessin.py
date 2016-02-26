import Tkinter
from Tkinter import *

class Dessin(Tkinter.Canvas):

	def __init__(self, ecran, largeur, hauteur, couleur):
			Tkinter.Canvas.__init__(self,ecran,width=largeur,height=hauteur,background=couleur)
	def creerLigne(self,coord1,coord2,epaisseur):
		ligne1 = self.create_line(coord1[0], coord1[1], coord2[0], coord2[1],width=epaisseur)
		self.update()