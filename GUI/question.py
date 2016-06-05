# -*- coding: utf-8 -*-

"""
	Author : Nicolas Gonçalves
	Purpose : Classe des fenêtres de questions
"""


import Tkinter
from Tkinter import *
from tkMessageBox import *
from controle_manuel import *

# classe de la fenêtre d'affichage de la selection du robot qui doit se déplacer à un endroit sélectionné
class Question(Tkinter.Toplevel):
	
	# constructeur de classe
	def __init__(self,fenetre,controller,destination):
		Tkinter.Toplevel.__init__(self,fenetre)
		self.controller = controller    # référence vers le controleur
		self.destination = destination    # coordonnées de l'intersection cible
		
		self.grab_set()
		self.focus_set()
		
		# envoi de la destination cible au robot selectionné au clic sur le bouton correspondant
		def robot(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) == "ready":
					self.controller.aller(id,destination)
				else:
					showinfo('erreur', "Ce robot n'a pas terminé la tâche qui lui a été affectée")
			else:
				showinfo('erreur', "Ce robot n'est pas connecté")
			self.destroy()
			
		
		# création des boutons
		bouton1=Button(self, text="Lancer robot 1", command = lambda : robot(1))
		bouton1.pack(padx=10, pady=10)
		bouton2=Button(self, text="Lancer robot 2", command= lambda : robot(2))
		bouton2.pack(padx=10, pady=10)
		bouton3=Button(self, text="Lancer robot 3", command= lambda : robot(3))
		bouton3.pack(padx=10, pady=10)
		
		

# classe de la fenêtre d'affichage de la selection du robot à lancer/mettre en pause
class Pause(Tkinter.Toplevel):

	# constructeur de classe
	def __init__(self,fenetre,controller):
		Tkinter.Toplevel.__init__(self,fenetre)
		self.fenetre = fenetre
		self.controller = controller    # référence vers le controleur
		
		self.grab_set()
		self.focus_set()
		
		# envoi de l'ordre de lancement au robot sélectionné par clic sur le bouton correspondant
		def lancer_robot(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) == "working":
					showinfo('erreur', "Ce robot est déjà en train de travailler !")
				else:	
					self.controller.lancer_robot(id)
			else :
				showinfo('erreur', "Ce robot n'est pas connecté")
			
		# envoi de l'ordre de mise en pause au robot sélectionné par clic sur le bouton correspondant
		def pause_robot(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) == "pause":
					showinfo('erreur', "Ce robot est déjà en pause ! ")
				else:	
					self.controller.pause(id)
			else :
				showinfo('erreur', "Ce robot n'est pas connecté")
				
		def manuel(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) != "ready":
					showinfo('erreur', "Ce robot ne peut actuellement pas passer en manuel")
				else:	
					controle = ControleManuel(self.fenetre,self.controller,id)
					self.destroy()
			else:
				showinfo('erreur', "Ce robot n'est pas connecté")
		
		# frame 1
		zone1 = Frame(self, borderwidth=2, relief=GROOVE)
		zone1.pack(side=LEFT, padx=30, pady=30)
		
		# frame2
		zone2 = Frame(self, borderwidth=2, relief=GROOVE)
		zone2.pack(side=LEFT, padx=30, pady=30)
		
		# frame3
		zone3 = Frame(self, borderwidth=2, relief=GROOVE)
		zone3.pack(side=RIGHT, padx=30, pady=30)
		
		# frame4
		zone4 = Frame(self, borderwidth=2, relief=GROOVE)
		zone4.pack(side=BOTTOM, padx=30, pady=30)
		
		
		# construction des boutons
		bouton1=Button(zone1, text="Lancer robot 1", command = lambda : lancer_robot(1))
		bouton1.pack(padx=10, pady=10)
		bouton2=Button(zone1, text="Lancer robot 2", command= lambda : lancer_robot(2))
		bouton2.pack(padx=10, pady=10)
		bouton3=Button(zone1, text="Lancer robot 3", command= lambda : lancer_robot(3))
		bouton3.pack(padx=10, pady=10)
		
		bouton4=Button(zone2, text="Pause robot 1", command = lambda : pause_robot(1))
		bouton4.pack(padx=10, pady=10)
		bouton5=Button(zone2, text="Pause robot 2", command= lambda : pause_robot(2))
		bouton5.pack(padx=10, pady=10)
		bouton6=Button(zone2, text="Pause robot 3", command= lambda : pause_robot(3))
		bouton6.pack(padx=10, pady=10)
		
		bouton7=Button(zone4, text="Fermer", command = self.destroy)
		bouton7.pack(padx=10, pady=10)
		
		bouton8=Button(zone3, text="Mode manuel robot 1", command = lambda : manuel(1))
		bouton8.pack(padx=10, pady=10)
		bouton9=Button(zone3, text="Mode manuel robot 2", command= lambda : manuel(2))
		bouton9.pack(padx=10, pady=10)
		bouton10=Button(zone3, text="Mode manuel robot 3", command= lambda : manuel(3))
		bouton10.pack(padx=10, pady=10)