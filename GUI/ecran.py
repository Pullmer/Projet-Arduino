# -*- coding: utf-8 -*-

"""
	Author : Nicolas Gonçalves
	Purpose : Fenetre graphique du logiciel
"""


import Tkinter
from Tkinter import *
from tkMessageBox import *
import Queue
from dessin import *
from question import *

# classe contenant les composants de la fenêtre principale
class Ecran():

	# constructeur de classe
	def __init__(self, controller,fenetre,queue):
	
		# action à réaliser quand on appuie sur les flèches clavier (déplacement du curseur)
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
		self.controller = controller    # référence cers le controleur
		self.fenetre = fenetre          # référence vers la fenêtre du programme
		self.queue = queue              # référence vers la file d'attente
		
		# frame 1
		zone1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
		zone1.pack(side=LEFT, padx=30, pady=30)
		
		# frame2
		zone2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
		zone2.pack(side=LEFT, padx=30, pady=30)
		
		
		self.creerMenu(fenetre)   # création de la barre des menus
		self.afficherInformations(zone2)   # création de la zone d'affichage de texte
		self.creerBoutons(zone2)   # création des boutons
		self.dessin = Dessin(zone1,500,500,'yellow')   #création de la zone de dessin du labyrinthe
		self.dessin.focus_set()
		self.dessin.bind("<Key>", clavier)   # on active les évènements clavier
		self.dessin.pack()   # on affiche la zone de dessin
	
	# méthode qui demande le tracé d'une ligne dans la zone de dessin
	def dessinerLigne(self,coord1,coord2):
		self.dessin.creerLigne(coord1,coord2,4)
		
	# méthode de création de la barre de menus et actions associées
	def creerMenu(self,fenetre):
	
		# message à afficher quand on clique sur "A propos"
		def infos():
			showinfo('A propos','cartographie et exploration de labyrinthe\n'+'developpé par :\n'+'BIDOUNG Katia\n'+'GONÇALVES Nicolas\n'+'MAISON Jonas\n'+'THOMAS Cyprien\n')
		
		
		def alert():
			pass
		
		def details_robot(id):
			self.controller.details(id)
			
		# (dés)activation du curseur au clic sur "Curseur"	
		def curseur():
			if(self.dessin.curseurUtilise()):
				self.dessin.effacerCurseur()
			else:
				self.dessin.afficherCurseur()
			
		# demande de lancement du serveur au clic sur "Lancer"
		def lancer():
			showinfo('information','lancement du serveur')
			self.controller.lancerServeur()
			
		# création d'une fenêtre secondaire pour démarrer/mettre en pause un robot au clic sur "Partir/Arreter"
		def go_pause():
			question = Pause(self.fenetre, self.controller)
			
		# action à effectuer au clic sur "Quitter"
		def quitter():
			if self.controller.connexionsEtablies():
				showinfo('erreur', 'Des connexions sont toujours présentes')
			else:
				self.controller.quitter()
				fenetre.destroy()
		
		
		# création des menus déroulants
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
		
	# création de la zone d'affichage de texte
	def afficherInformations(self,frame):
		l = LabelFrame(frame, text="Informations", padx=20, pady=20)
		l.pack(side = TOP,fill="both", expand="yes")
		self.text = "Robot 1:\nPas d'informations\n\nRobot 2:\nPas d'informations\n\nRobot 3:\nPas d'informations\n\n"
		self.label = Label(l, text=self.text)
		self.label.pack()
		
	# création des boutons et des actions associées
	def creerBoutons(self,frame):
			
		# envoi d'une demande de destination au clic sur "Aller à"
		def go():
			if self.dessin.curseurUtilise():
				position = self.dessin.getPositionCurseur()
				question = Question(self.fenetre, self.controller, position)    # fenêtre secondaire permettant de sélectionner le robot
			else:
				showinfo('erreur', 'Le curseur n\'est pas utilisé !')
				
		# on affiche un message contenant les informations de l'intersection pointée par le curseur au clic dur "Voir"
		def voir():
			if self.dessin.curseurUtilise():
				position = self.dessin.getPositionCurseur()
				texte = self.controller.voirInfosIntersection(position)
				showinfo('intersection',texte)
			else:
				showinfo('erreur', 'Le curseur n\'est pas utilisé !')
		
		# création des boutons
		bouton_go=Button(frame, text="Aller à", command=go)
		bouton_go.pack(side=BOTTOM, padx=10, pady=10)
		
		bouton_voir=Button(frame, text="Voir", command=voir)
		bouton_voir.pack(side=BOTTOM, padx=10, pady=10)
		
	
	# méthode de raffraichissment de l'écran (toutes les 50 ms)
	def rafraichirEcran(self):
		# on consulte les éléments de la file d'attente et on effectue les actions d'affichages correspondantes
		while self.queue.qsize():
				try:
					msg = self.queue.get(0)
					# on regarde la modification à faire
					if msg == "chemin":
						id = self.queue.get(0)
						ancienne = self.queue.get(0)
						nouvelle = self.queue.get(0)
						
						X1 = int(0.25*ancienne[0]+250)
						Y1 = int(-0.25*ancienne[1]+250)
						X2 = int(0.25*nouvelle[0]+200)
						Y2 = int(-0.25*nouvelle[1]+500)
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
						tab = self.text.split("\n\n")
						for i in range(1,3):
							if i == id:
								tab[i-1] = "Robot "+str(id)+":\nPas d'informations"
								break
						self.text = tab[0]+"\n\n"+tab[1]+"\n\n"+tab[2]+"\n\n"
						self.label.config(text=self.text)
						showinfo('deconnexion','Le robot ' + str(id) + ' vient de se deconnecter')
						
					if msg == "informations":
						id = self.queue.get(0)
						position = self.queue.get(0)
						batterie = self.queue.get(0)
						tab = self.text.split("\n\n")
						for i in range(1,3):
							if i == id:
								tab[i-1] = "Robot "+str(id)+":\nPosition : "+str(position)+"\nBatterie : "+str(batterie)+"%"
								break
						self.text = tab[0]+"\n\n"+tab[1]+"\n\n"+tab[2]+"\n\n"
						self.label.config(text=self.text)
				except Queue.Empty:
					pass	
					