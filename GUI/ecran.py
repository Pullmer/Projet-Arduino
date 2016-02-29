# -*- coding: utf-8 -*-

import Tkinter
from Tkinter import *
from tkMessageBox import *

class Ecran():

	def __init__(self, controller,fenetre,queue):
		self.controller = controller
		self.fenetre = fenetre
		self.queue = queue
		
		# frame 1
		zone1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
		zone1.pack(side=LEFT, padx=30, pady=30)
		
		# frame2
		zone2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
		zone2.pack(side=LEFT, padx=30, pady=30)
		
		
		self.creerMenu(fenetre)
		self.afficherInformations(zone2)
		self.creerBoutons(zone2)
		self.dessin = Canvas(zone1,width=400,height=400,background='yellow')
		self.dessin.pack()
	
	def dessinerLigne(self,coord1,coord2):
		self.dessin.creerLigne(coord1,coord2,4)
		
	def creerMenu(self,fenetre):
	
		def alert():
			showinfo('essai')
			
		menubar = Menu(fenetre)
		
		menu1 = Menu(menubar, tearoff=0)
		menu1.add_command(label="Commencer", command=alert)
		menu1.add_command(label="Mode", command=alert)
		menu1.add_separator()
		menu1.add_command(label="Quitter", command=fenetre.quit)
		menubar.add_cascade(label="Fichier", menu=menu1)

		menu2 = Menu(menubar, tearoff=0)
		menu2.add_command(label="Robot 1", command=alert)
		menu2.add_command(label="Robot 2", command=alert)
		menu2.add_command(label="Robot 3", command=alert)
		menubar.add_cascade(label="Robot", menu=menu2)

		menu3 = Menu(menubar, tearoff=0)
		menu3.add_command(label="A propos", command=alert)
		menubar.add_cascade(label="Aide", menu=menu3)

		fenetre.config(menu=menubar)
		
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
		
		bouton_pause=Button(frame, text="Pause", command=self.fenetre.quit)
		bouton_pause.pack(side=BOTTOM, padx=10, pady=10)
	def rafraichirEcran(self):
		while self.queue.qsize():
				try:
					msg = self.queue.get(0)
					# on regarde la modification à faire
					if msg == "chemin":
						ancienne = self.queue.get(0)
						nouvelle = self.queue.get(0)
						
						X1 = int(30*ancienne[0]+200)
						Y1 = int(-30*ancienne[1]+400)
						X2 = int(30*nouvelle[0]+200)
						Y2 = int(-30*nouvelle[1]+400)
						self.dessin.create_line(X1, Y1, X2, Y2,width=4)
						
				except Queue.Empty:
					pass	