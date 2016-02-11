# coding: utf-8

class Robot:

	def __init__(self,socket,ip, port,labyrinthe):
			self.socket = socket
			self.ip = ip
			self.port = port
			self.bat_level = 100
			self.position = (0,0)
			self.intersection = ("NON","OUI","NON")
			self.ancienne_position = (0,0)
			self.labyrinthe = labyrinthe
			
			
	#traitement de la chaine de caractère reçue
	def traiter(self,recu):
		l = recu.split("\n")
		
		#action à faire si c'est une demande de direction
		if l[0] == "DIRECTION?":
			X = float(l[1].split(" : ")[1])
			Y = float(l[2].split(" : ")[1])
			self.ancienne_position = self.position
			self.position = (X,Y)
			print(self.position)
			droite = (l[3].split(" : ")[1])
			face = (l[4].split(" : ")[1])
			gauche = (l[5].split(" : ")[1])
			self.intersection = (droite, face, gauche)
			print(self.intersection)
			self.bat_level = float(l[6].split(" : ")[1])
			print(self.bat_level)
			self.labyrinthe.demandeDirection(self)   #demande de direction au labyrinthe
			
	def donnerOrdre(self,ordre):
		self.socket.envoyer(ordre)
		
	def getPosition(self):
		return self.position
	
	def getAnciennePosition(self):
		return self.ancienne_position
		
	def getIP(self):
		return self.ip
		
	def getBatterie(self):
		return self.bat_level
		
	def getIntersection(self):
		return self.intersection