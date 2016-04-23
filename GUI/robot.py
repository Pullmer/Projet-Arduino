# coding: utf-8

class Robot:

	def __init__(self,socket,ip, port,labyrinthe,controller):
			self.socket = socket   #référence vers le thread de communication
			self.ip = ip   #adresse ip du robot
			self.port = port   #port de communication
			self.bat_level = 100   #niveau de batterie
			self.liste_positions = [(0,0)]   #liste des dernières positions connues
			self.position = (0,0)       #position du robot
			self.intersection = ("NON","OUI","NON")   #forme de la dernière intersection parcourue
			self.ancienne_position = (0,0)   #ancienne position du robot
			self.labyrinthe = labyrinthe     #reference vers le labyrinthe
			self.controller = controller     #reference vers le controleur
			controller.ajouterRobot(self)    #ajout à la liste des robots connus du controleur
			
			
	#traitement de la chaine de caractère reçue
	def traiter(self,recu):
		l = recu.split("\n")
		
		#action à faire si c'est une demande de direction
		if l[0] == "DIRECTION?":
			#on récupère la position
			X = float(l[1].split(" : ")[1])
			Y = float(l[2].split(" : ")[1])
			self.ancienne_position = self.position
			self.position = (X,Y)
			
			if X != (self.liste_positions[-1])[0] or Y != (self.liste_positions[-1])[1]:
				self.liste_positions.append(self.position)
			print(self.position)
			
			#on récupère la forme de l'intersection
			droite = (l[3].split(" : ")[1])
			face = (l[4].split(" : ")[1])
			gauche = (l[5].split(" : ")[1])
			self.intersection = (droite, face, gauche)
			print(self.intersection)
			
			#on récupère le niveau de batterie
			self.bat_level = float(l[6].split(" : ")[1])
			print(self.bat_level)
			
			self.controller.dessinerCheminParcouru(self,self.ancienne_position,self.position)   #on demande de tracer le chemin qui a été parcouru
			self.labyrinthe.demandeDirection(self)   #demande de direction au labyrinthe
			
	#méthode qui demande l'envoi d'un ordre au robot
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
		self.liste_positions.remove(self.liste_positions[-1])
		
	#méthode qui demande l'arret du robot
	def stop(self):
		self.donnerOrdre("stop")