# -*- coding: utf-8 -*-

import Tkinter
from Tkinter import *
from dessin import *
from tkMessageBox import *

class Ecran(Tkinter.Tk):

	def __init__(self, controller):
		Tkinter.Tk.__init__(self)
		self.controller = controller
		self.controller.ajouterEcran(self)	
		# frame 1
		zone1 = Frame(self, borderwidth=2, relief=GROOVE)
		zone1.pack(side=LEFT, padx=30, pady=30)
		
		# frame2
		zone2 = Frame(self, borderwidth=2, relief=GROOVE)
		zone2.pack(side=LEFT, padx=30, pady=30)
		
		
		self.creerMenu()
		self.afficherInformations(zone2)
		self.creerBoutons(zone2)
		self.dessin = Dessin(zone1,400,400,'yellow')
		self.dessin.pack()
	
	def dessinerLigne(self,coord1,coord2):
		self.dessin.creerLigne(coord1,coord2,4)
		
	def creerMenu(self):
	
		def alert():
			showinfo('essai')
			
		menubar = Menu(self)
		
		menu1 = Menu(menubar, tearoff=0)
		menu1.add_command(label="Commencer", command=alert)
		menu1.add_command(label="Mode", command=alert)
		menu1.add_separator()
		menu1.add_command(label="Quitter", command=self.quit)
		menubar.add_cascade(label="Fichier", menu=menu1)

		menu2 = Menu(menubar, tearoff=0)
		menu2.add_command(label="Robot 1", command=alert)
		menu2.add_command(label="Robot 2", command=alert)
		menu2.add_command(label="Robot 3", command=alert)
		menubar.add_cascade(label="Robot", menu=menu2)

		menu3 = Menu(menubar, tearoff=0)
		menu3.add_command(label="A propos", command=alert)
		menubar.add_cascade(label="Aide", menu=menu3)

		self.config(menu=menubar)
		
	def afficherInformations(self,frame):
		l = LabelFrame(frame, text="Informations", padx=20, pady=20)
		l.pack(side = TOP,fill="both", expand="yes")
		Label(l, text="Robot 1:\nPosition : (X,Y)\nBatterie : 95%\n\nRobot 2:\nPosition : (X,Y)\nBatterie : 95%\n\nRobot 3:\nPosition : (X,Y)\nBatterie : 95%\n\n").pack()
		
	def creerBoutons(self,frame):
	
		def lancer():
			showinfo('information','lancement du serveur')
			self.controller.lancerServeur()
			
		bouton_start=Button(frame, text="Lancer", command=lancer)
		bouton_start.pack(side=BOTTOM, padx=10, pady=10)
		
		bouton_pause=Button(frame, text="Pause", command=self.quit)
		bouton_pause.pack(side=BOTTOM, padx=10, pady=10)
		
	def connexion(self):
		self.event_add('<<connexion>>')
		self.bind('<<connexion>>', evenement)
		
		
	def evenement():
		showinfo('connexion','Un robot vient de se connecter')