# -*- coding: utf-8 -*-

"""
	Author : Nicolas Gonçalves
	Purpose : Fenêtre de commande manuelle des robots
"""


import Tkinter
from Tkinter import *

# classe de la fenêtre d'affichage de la selection du robot qui doit se déplacer à un endroit sélectionné
class ControleManuel(Tkinter.Toplevel):
	
	# constructeur de classe
	def __init__(self,fenetre,controller,id):
		Tkinter.Toplevel.__init__(self,fenetre)
		self.controller = controller    # référence vers le controleur
		self.id = id
		self.commande = (0,0)
		self.spamG = False
		self.spamD = False
		
		
		#########################################################

		#########################################################
		#fonctions executées lors d'un evenement clavier


		def onKeyPress(event):

			if (event.keysym=='e') and (not spamG):
				self.spamG = True
				self.commande[0]=100
				self.controller.envoiCommande(self.commande,id)
			elif (event.keysym=='d') and (not spamG):
				self.spamG = True
				self.commande[0]=-100
				self.controller.envoiCommande(self.commande,id)
			elif (event.keysym=='o') and (not spamD):
				self.spamD = True
				self.commande[1]=100
				self.controller.envoiCommande(self.commande,id)
			elif (event.keysym=='l') and (not spamD):
				self.spamD = True
				self.commande[1]=-100
				self.controller.envoiCommande(self.commande,id)
			


		def onKeyRelease(event):

			if (event.keysym=='e'):
				self.commande[0]=0
				self.spamG = False
			elif (event.keysym=='d'):
				self.commande[0]=0
				self.spamG = False
			elif (event.keysym=='o'):
				self.commande[1]=0
				self.spamD = False
			elif (event.keysym=='l'):
				self.commande[1]=0
				self.spamD = False

			self.controller.envoiCommande(self.commande,id)


		#########################################################

		#########################################################
		#envoie commande avancer
		def goUp(event):

			self.commande[0]=100
			self.commande[1]=100
			self.controller.envoiCommande(self.commande,id)
			
		#########################################################

		#########################################################
		#envoie commande reculer
		def goDown(event):

			self.commande[0]=-100
			self.commande[1]=-100
			self.controller.envoiCommande(self.commande,id)
			
		#########################################################

		#########################################################
		#envoie commande tourner à gauche
		def goLeft(event):

			self.commande[0]=-60
			self.commande[1]=+60
			self.controller.envoiCommande(self.commande,id)
			
		#########################################################

		#########################################################
		#envoie commande tourner à droite
		def goRight(event):

			self.commande[0]=60
			self.commande[1]=-60
			self.controller.envoiCommande(self.commande,id)
			
		#########################################################


		#########################################################
		#envoi d'une commande nulle
		def pasGo(event):

			self.commande[0]=0
			self.commande[1]=0
			self.controller.envoiCommande(self.commande,id)
			
		#########################################################

		#########################################################
		#envoie la demande de niveau batterie
		def askBat():

			comm="#bat_level;"
			self.controller.envoiDirect(comm,id)
			
		#########################################################

		#########################################################
		#prend une photo (pas encore implémenté sur la Pi
		def askForPic():

			comm="#picture;"
			self.controller.envoiDirect(comm,id)
			
		#########################################################

		#########################################################
		#envoie la commande de coupure de connexion à la Pi et quitte tk
		def quitter():

			comm="#quit;"
			self.controller.envoiDirect(comm,id)
			self.destroy()
			
		#########################################################

		#creation de la fenetre et element graphiques
		self.geometry('800x400')

		self.resizable(0,0)

		Canvas(self, width=480, height=380, bg='grey').pack(side=LEFT, padx=5, pady=5)

		LabelFrameControles = LabelFrame(self, borderwidth=2,text="Controles", relief=GROOVE, height=370, width=280)
		LabelFrameControles.pack(side=LEFT, padx=5, pady=5)
		LabelFrameControles.pack_propagate(0) #Empèche le frame de changer sa taille 

		LabelFrameDirections = LabelFrame(LabelFrameControles, borderwidth=2, text="Directions", relief=GROOVE, height=120, width=160)
		LabelFrameDirections.pack(side=TOP)
		LabelFrameDirections.pack_propagate(0)

		ButtonUp=Button(LabelFrameDirections,text="Avancer")
		ButtonUp.pack(side=TOP)
		ButtonDown=Button(LabelFrameDirections,text="Reculer")
		ButtonDown.pack(side=BOTTOM)
		ButtonLeft=Button(LabelFrameDirections,text="Gauche")
		ButtonLeft.pack(side=LEFT)
		ButtonRight=Button(LabelFrameDirections,text="Droite")
		ButtonRight.pack(side=RIGHT)

		ButtonPic=Button(LabelFrameControles,text="Take Picture",command=askForPic)
		ButtonPic.pack(side=TOP,pady=5)

		LabelBatterie=Label(LabelFrameControles,text="Niveau Batterie : ----")
		LabelBatterie.pack(side=TOP,pady=5)

		ButtonBatterie=Button(LabelFrameControles,text="Lire niveau batterie", command=askBat)
		ButtonBatterie.pack(side=TOP,pady=5)

		ButtonQuit=Button(LabelFrameControles,text="Quitter", command=quitter)
		ButtonQuit.pack(side=TOP,pady=5)


		#creation des liens entre evenement clavier et fonctions à executer
		self.bind('<KeyPress>', onKeyPress)
		self.bind('<KeyRelease>', onKeyRelease)

		ButtonUp.bind('<ButtonPress-1>',goUp)
		ButtonUp.bind('<ButtonRelease-1>',pasGo)
		ButtonDown.bind('<ButtonPress-1>',goDown)
		ButtonDown.bind('<ButtonRelease-1>',pasGo)
		ButtonLeft.bind('<ButtonPress-1>',goLeft)
		ButtonLeft.bind('<ButtonRelease-1>',pasGo)
		ButtonRight.bind('<ButtonPress-1>',goRight)
		ButtonRight.bind('<ButtonRelease-1>',pasGo)

		

				
				
