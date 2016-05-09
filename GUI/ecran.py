# -*- coding: utf-8 -*-

import Tkinter
from Tkinter import *
from tkMessageBox import *
import Queue
from dessin import *
from question import *

class Ecran():

	def __init__(self, controller,fenetre,queue):
	
		def clavier(event):
			touche = event.keysym
			if self.dessin.curseurUtilise():
				position_curseur = self.dessin.getPositionCurseur()
				carrefours_adjacents = self.controller.getAdjacents(position_curseur)
				if touche == "Up":
					for position in carrefours_adjacents:
						dx = position[0]-position_curseur[0]
						dy = position[1]-position_curseur[1]
						if dx == 0 and dy >0.11:
							self.dessin.deplacerCurseur(position)
							break
				elif touche == "Down":
					for position in carrefours_adjacents:
						dx = position[0]-position_curseur[0]
						dy = position[1]-position_curseur[1]
						if dx == 0 and dy <-0.11:
							self.dessin.deplacerCurseur(position)
							break
				elif touche == "Right":
					for position in carrefours_adjacents:
						dx = position[0]-position_curseur[0]
						dy = position[1]-position_curseur[1]
						if dx > 0.11 and dy == 0:
							self.dessin.deplacerCurseur(position)
							break
				elif touche == "Left":
					for position in carrefours_adjacents:
						dx = position[0]-position_curseur[0]
						dy = position[1]-position_curseur[1]
						if dx < -0.11 and dy == 0 and dx!=-0.1:
							self.dessin.deplacerCurseur(position)
							break
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
		self.dessin = Dessin(zone1,400,400,'yellow')
		self.dessin.focus_set()
		self.dessin.bind("<Key>", clavier)
		self.dessin.pack()
	
	def dessinerLigne(self,coord1,coord2):
		self.dessin.creerLigne(coord1,coord2,4)
		
	def creerMenu(self,fenetre):
	
		def infos():
			showinfo('A propos','cartographie et exploration de labyrinthe\n'+'developpé par :\n'+'BIDOUNG Katia\n'+'GONÇALVES Nicolas\n'+'MAISON Jonas\n'+'THOMAS Cyprien\n')
		
		def details_robot(id):
			self.controller.details(id)
			
		def alert():
			self.fenetre.quit()
			
		def curseur():
			if(self.dessin.curseurUtilise()):
				self.dessin.effacerCurseur()
			else:
				self.dessin.afficherCurseur()
			
		def lancer():
			showinfo('information','lancement du serveur')
			self.controller.lancerServeur()
			
		def go_pause():
			question = Pause(self.fenetre, self.controller)
			
		def quitter():
			if self.controller.connexionsEtablies():
				showinfo('erreur', 'Des connexions sont toujours présentes')
			else:
				self.controller.quitter()
				fenetre.destroy()
		
		menubar = Menu(fenetre)
		
		menu1 = Menu(menubar, tearoff=0)
		menu1.add_command(label="Commencer", command=alert)
		menu1.add_command(label="Lancer", command=lancer)
		menu1.add_command(label="Partir/Arreter", command=go_pause)
		menu1.add_command(label="Curseur", command=curseur)
		menu1.add_separator()
		menu1.add_command(label="Quitter", command=quitter)
		menubar.add_cascade(label="Fichier", menu=menu1)

		menu2 = Menu(menubar, tearoff=0)
		menu2.add_command(label="Robot 1", command=lambda : details_robot(1))
		menu2.add_command(label="Robot 2", command=lambda : details_robot(2))
		menu2.add_command(label="Robot 3", command=lambda : details_robot(3))
		menubar.add_cascade(label="Robot", menu=menu2)

		menu3 = Menu(menubar, tearoff=0)
		menu3.add_command(label="A propos", command=infos)
		menubar.add_cascade(label="Aide", menu=menu3)

		fenetre.config(menu=menubar)
		
	def afficherInformations(self,frame):
		l = LabelFrame(frame, text="Informations", padx=20, pady=20)
		l.pack(side = TOP,fill="both", expand="yes")
		Label(l, text="Robot 1:\nPosition : (X,Y)\nBatterie : 95%\n\nRobot 2:\nPosition : (X,Y)\nBatterie : 95%\n\nRobot 3:\nPosition : (X,Y)\nBatterie : 95%\n\n").pack()
		
	def creerBoutons(self,frame):
			
		def pause():
			self.controller.pause()
			
		def go():
			if self.dessin.curseurUtilise():
				position = self.dessin.getPositionCurseur()
				question = Question(self.fenetre, self.controller, position)
			else:
				showinfo('erreur', 'Le curseur n\'est pas utilisé !')
				
		def voir():
			if self.dessin.curseurUtilise():
				position = self.dessin.getPositionCurseur()
				texte = self.controller.voirInfosIntersection(position)
				showinfo('intersection',texte)
			else:
				showinfo('erreur', 'Le curseur n\'est pas utilisé !')
		
		bouton_pause=Button(frame, text="Pause", command=pause)
		bouton_pause.pack(side=BOTTOM, padx=10, pady=10)
		
		bouton_go=Button(frame, text="Aller à", command=go)
		bouton_go.pack(side=BOTTOM, padx=10, pady=10)
		
		bouton_voir=Button(frame, text="Voir", command=voir)
		bouton_voir.pack(side=BOTTOM, padx=10, pady=10)
		
	def rafraichirEcran(self):
		while self.queue.qsize():
				try:
					msg = self.queue.get(0)
					# on regarde la modification à faire
					if msg == "chemin":
						id = self.queue.get(0)
						ancienne = self.queue.get(0)
						nouvelle = self.queue.get(0)
						
						X1 = int(30*ancienne[0]+200)
						Y1 = int(-30*ancienne[1]+400)
						X2 = int(30*nouvelle[0]+200)
						Y2 = int(-30*nouvelle[1]+400)
						self.dessin.creerLigne((X1,Y1),(X2,Y2),4)
						self.dessin.deplacerPoint(id,(X2,Y2))
						
					if msg == "details":
						id = self.queue.get(0)
						if id=="erreur":
							showinfo('exception','Ce robot n\'est pas connecté')
						else:
							ip = self.queue.get(0)
							position = self.queue.get(0)
							batterie = self.queue.get(0)
							text = "Ce robot est en " + str(position) +". Il lui reste "+ str(batterie) +"% de batterie. Son adresse IP est : "+ str(ip)
							showinfo('details du robot '+str(id),text)
							
					if msg == "nouveau robot":
						id = self.queue.get(0)
						self.dessin.creerPoint(id)
						showinfo('connexion','Un robot vient de se connecter')
						
					if msg == "deconnexion":
						id = self.queue.get(0)
						self.dessin.effacerPoint(id)
						showinfo('deconnexion','Le robot ' + str(id) + ' vient de se deconnecter')
				except Queue.Empty:
					pass	
					
