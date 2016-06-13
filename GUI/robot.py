# coding: utf-8

"""
	Author : Nicolas Gonçalves
	Purpose : Classe Robot
"""


class Robot:

	def __init__(self,socket,ip, port,labyrinthe,controller,ordreDirect):
			self.socket = socket   #référence vers le thread de communication
			self.ordreDirect = ordreDirect
			self.ip = ip   #adresse ip du robot
			self.port = port   #port de communication
			self.bat_level = 100   #niveau de batterie
			self.liste_positions = [(0,0)]   #liste des dernières positions connues
			self.position = (0,0)       #position du robot
			self.intersection = ("NON","OUI","NON","NON")   #forme de la dernière intersection parcourue
			self.ancienne_position = (0,0)   #ancienne position du robot
			self.mode = "exploration"
			self.state = "ready"
			self.trajet = []
			self.labyrinthe = labyrinthe     #reference vers le labyrinthe
			self.controller = controller     #reference vers le controleur
			controller.ajouterRobot(self)    #ajout à la liste des robots connus du controleur
			
			
	#traitement de la chaine de caractère reçue
	def traiter(self,recu):
		print(recu)
		l = recu.split("\n")
		
		#action à faire si c'est une demande de direction
		if l[0] == "DIRECTION?" and self.mode == "exploration":
			#on récupère la position
			X = float(l[1].split(" : ")[1])
			Y = float(l[2].split(" : ")[1])
			self.ancienne_position = self.position
			self.position = (X,Y)
			print(self.liste_positions)
			if self.liste_positions == [(0,0)] and self.position == (0,0):
				self.donnerOrdre("#workcompleted;")
				self.controller.fini(self)
				self.state = "ready"
				return
			elif X != (self.liste_positions[-1])[0] or Y != (self.liste_positions[-1])[1]:
				self.liste_positions.append(self.position)
			print(self.position)
			
			#on récupère la forme de l'intersection
			est = (l[3].split(" : ")[1])
			nord = (l[4].split(" : ")[1])
			ouest = (l[5].split(" : ")[1])
			sud = (l[6].split(" : ")[1])
			self.intersection = (est, nord, ouest, sud)
			print(self.intersection)
			
			self.controller.dessinerCheminParcouru(self,self.ancienne_position,self.position)   #on demande de tracer le chemin qui a été parcouru
			#self.labyrinthe.getSemaphore().acquire()
			self.labyrinthe.demandeDirection(self)   #demande de direction au labyrinthe
			#self.labyrinthe.getSemaphore().release()
			
		elif l[0] == "DIRECTION?" and self.mode == "navigation":
			print(self.trajet)
			if len(self.trajet)>1:
				print("test")
				#on récupère la position
				X = float(l[1].split(" : ")[1])
				Y = float(l[2].split(" : ")[1])
				self.ancienne_position = self.position
				self.position = (X,Y)
				
				ancienne = self.labyrinthe.rechercheNoeud(self.ancienne_position)
				depart = self.labyrinthe.rechercheNoeud(self.position)
				arrivee = self.trajet[-1]
				
				if self.labyrinthe.rechercheNoeud(self.position) != self.trajet[0]:
					self.trajet = self.labyrinthe.dijsktra(depart,arrivee)
					direction = self.labyrinthe.calculDirection(ancienne,depart,self.trajet[1])
					del self.trajet[0]
				else :
					direction = self.labyrinthe.calculDirection(ancienne,depart,self.trajet[1])
					del self.trajet[0]
				print(direction)
				self.donnerOrdre(direction)
			else:
				self.donnerOrdre("#workcompleted;")
				self.controller.fini(self)
				self.state = "ready"
			self.controller.dessinerCheminParcouru(self,self.ancienne_position,self.position)   #on demande de tracer le chemin qui a été parcouru
			
		elif l[0] == "CLOSE_CONNEXION":
			self.socket.fermer()
			self.controller.deconnexion(self)
			
		elif l[0] == "Batterie :":
			self.bat_level = (float(l[1])-4.6)/0.8*100
			
			
	#méthode qui demande l'envoi d'un ordre (une réponse) au robot
	def donnerOrdre(self,ordre):
		self.socket.envoyer(ordre)
		
	#méthode qui retourne la position
	def getPosition(self):
		return self.position
	
	#méthode qui retourne l'ancienne position
	def getAnciennePosition(self):
		return self.ancienne_position
		
	#méthode qui retourne l'adresse ip du robot
	def getIP(self):
		return self.ip
		
	#méthode qui retourne le niveau de batterie
	def getBatterie(self):
		return self.bat_level
	
	#méthode qui retourne la forme de l'intersection
	def getIntersection(self):
		return self.intersection
	
	#méthode qui retourne la dernière position connue
	def dernierePositionConnue(self):
		return self.liste_positions[-1]
		
	#méthode qui supprime la dernière position connue
	def supprimerDernierePosition(self):
		del self.liste_positions[-1]
		
	#méthode qui demande l'arret du robot
	def stop(self):
		self.ordreDirect.envoyer("#pause;")
		self.state = "pause"
		
	# on demande le départ du robot
	def go(self):
		self.ordreDirect.envoyer("#face;")
		self.state = "working"
		
	def erreur(self):
		try:
			self.socket.fermer()
		except:
			print("erreur")
		self.controller.deconnexion(self)
		
	# passe le robot en mode navigation vers une destination donnée
	def naviguer(self, destination):
		self.mode = "navigation"
		self.state = "working"
		self.ordreDirect.envoyer("#turnback;")
		depart = self.labyrinthe.rechercheNoeud(self.position)
		arrivee = self.labyrinthe.rechercheNoeud(destination)
		self.trajet = self.labyrinthe.dijsktra(depart, arrivee)
		print(self.trajet)
		if self.position == (0,0) :
			del self.trajet[0]
		
	# retourne l'état du robot
	def getState(self):
		return self.state
		