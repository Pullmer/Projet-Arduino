# coding: utf-8 

"""
	Author : Nicolas Gonçalves
	Purpose : Main du logiciel
"""

import Tkinter
from Tkinter import *
from controller import *

# chargement d'une fenetre graphique
fenetre = Tk()

#on construit le controleur
controller = Controller(fenetre)

#on affiche la fenetre
fenetre.mainloop()