# -*- coding: utf-8 -*-

import Tkinter
from Tkinter import *
from tkMessageBox import *

class Question(Tkinter.Toplevel):
	
	def __init__(self,fenetre,controller,destination):
		Tkinter.Toplevel.__init__(self,fenetre)
		self.controller = controller
		self.destination = destination
		
		self.grab_set()
		self.focus_set()
		
		def robot(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) == "ready":
					self.controller.aller(id,destination)
				else:
					showinfo('erreur', "Ce robot n'a pas terminé la tâche qui lui a été affectée")
			else:
				showinfo('erreur', "Ce robot n'est pas connecté")
			self.destroy()
			
		
		bouton1=Button(self, text="Lancer robot 1", command = lambda : robot(1))
		bouton1.pack(padx=10, pady=10)
		bouton2=Button(self, text="Lancer robot 2", command= lambda : robot(2))
		bouton2.pack(padx=10, pady=10)
		bouton3=Button(self, text="Lancer robot 3", command= lambda : robot(3))
		bouton3.pack(padx=10, pady=10)
		
		
class Pause(Tkinter.Toplevel):
	
	def __init__(self,fenetre,controller):
		Tkinter.Toplevel.__init__(self,fenetre)
		self.controller = controller
		
		self.grab_set()
		self.focus_set()
		
		def lancer_robot(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) == "working":
					showinfo('erreur', "Ce robot est déjà en train de travailler !")
				else:	
					self.controller.lancer_robot(id)
			else :
				showinfo('erreur', "Ce robot n'est pas connecté")
			
		def pause_robot(id):
			if self.controller.isConnected(id):
				if self.controller.getEtatRobot(id) == "pause":
					showinfo('erreur', "Ce robot est déjà en pause ! ")
				else:	
					self.controller.pause(id)
			else :
				showinfo('erreur', "Ce robot n'est pas connecté")
		
		# frame 1
		zone1 = Frame(self, borderwidth=2, relief=GROOVE)
		zone1.pack(side=LEFT, padx=30, pady=30)
		
		# frame2
		zone2 = Frame(self, borderwidth=2, relief=GROOVE)
		zone2.pack(side=RIGHT, padx=30, pady=30)
		
		# frame3
		zone3 = Frame(self, borderwidth=2, relief=GROOVE)
		zone3.pack(side=BOTTOM, padx=30, pady=30)
		
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
		
		bouton7=Button(zone3, text="Fermer", command = self.destroy)
		bouton7.pack(padx=10, pady=10)