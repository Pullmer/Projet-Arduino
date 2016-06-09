# coding: utf-8

"""
	Author : Nicolas Gonçalves
	Purpose : Classe Labyrinthe
"""


import networkx as nx
from robot import *
import threading

class Labyrinthe:

	def __init__(self,controller):
		self.controller = controller   #référence vers le controller
		self.labyrinthe = nx.Graph()   #graphe de représentation du labyrinthe
		self.semaphore = threading.Semaphore(value=1)
		self.labyrinthe.add_node(0, coords = (0,0))   #ajout du point de départ du labyrinthe
		self.labyrinthe.add_node(1, coords = (0,0.1))
		self.prochain = 2             #identifiant du prochain noeud à construire
		self.ajouterChemin(0,1,0)
		
	#retourne la liste des noeuds du labyrinthe
	def getNodes(self):
		return self.labyrinthe.nodes()
		
	#calcul de distance entre deux points
	def calculDistance(self, coord1, coord2):
		return ((coord2[0]-coord1[0])*(coord2[0]-coord1[0]) + (coord2[1]-coord1[1])*(coord2[1]-coord1[1]))
		
	#ajout d'un chemin dans le graphe
	def ajouterChemin(self, depart, arrivee, longueur):
		self.labyrinthe.add_edge(depart,arrivee, weight = longueur)
		
	#ajout d'un noeud dans un graphe
	def ajouterNoeud(self, coordonees):
		nombre_noeuds = self.labyrinthe.number_of_nodes()
		self.labyrinthe.add_node(self.prochain, coords = coordonnees)
		self.prochain += 1
		
	#executé quand un robot demande sa direction
	def demandeDirection(self, robot):
		#on récupère l'ancienne et la nouvelle position du robot
		coord1 = robot.getAnciennePosition()
		coord2 = robot.getPosition()
		#on récupère les noeuds correspondants aux coordonnées récupérées
		nouvelle_position = self.rechercheNoeud(coord2)
		ancienne_position = self.rechercheNoeud(coord1)
		
		#si le carrefour est inconnu
		if nouvelle_position == -1:
			#on recherche le noeud à modifier parmi les ajacents à l'ancienne position
			adjacents = self.labyrinthe.neighbors(ancienne_position)
			Dx = coord2[0]-coord1[0]
			Dy = coord2[1]-coord1[1]
			for noeud in adjacents:
				position_noeud = self.labyrinthe.node[noeud]['coords']
				dx = position_noeud[0]-coord1[0]
				dy = position_noeud[1]-coord1[1]
				if (Dx==0 and dx==0 and Dy*dy>0) or (Dy==0 and dy==0 and Dx*dx>0):
					nouvelle_position = noeud
			
			self.labyrinthe.node[nouvelle_position]['coords'] = coord2   #on modifie les coordonnées du noeud
			distance_parcourue = self.calculDistance(coord1,coord2)
			self.labyrinthe.edge[ancienne_position][nouvelle_position]['weight'] = distance_parcourue    #mise à jour distance du chemin parcouru
			print("modification noeud ",nouvelle_position," en :",coord2)
			intersection = robot.getIntersection()   #on récupère la forme de l'intersection découverte
			self.construireIntersection(intersection, coord1, coord2,nouvelle_position)   #on demande la construction de cette intersection dans le graphe
			
		#si le chemin parcouru est inconnu, mais pas le carrefour
		elif self.estConnu(ancienne_position, nouvelle_position) == False:		
			distance_parcourue = self.calculDistance(coord1,coord2)
			self.labyrinthe.edge[ancienne_position][nouvelle_position]['weight'] = distance_parcourue   #mise à jour distance du chemin parcouru
			
			#on supprime les noeuds intermédiaires mais en fait inutiles construits précédemment
			adjacents = self.labyrinthe.neighbors(ancienne_position)
			Dx = coord2[0]-coord1[0]
			Dy = coord2[1]-coord1[1]
			for noeud in adjacents:
				position_noeud = self.labyrinthe.node[noeud]['coords']
				dx = position_noeud[0]-coord1[0]
				dy = position_noeud[1]-coord1[1]
				if (Dx==0 and dx==0 and Dy*dy>0) or (Dy==0 and dy==0 and Dx*dx>0):
					if noeud != nouvelle_position:
						self.labyrinthe.remove_node(noeud)
						print("suppression noeud",noeud)		
			adjacents = self.labyrinthe.neighbors(nouvelle_position)
			Dx = coord2[0]-coord1[0]
			Dy = coord2[1]-coord1[1]
			for noeud in adjacents:
				position_noeud = self.labyrinthe.node[noeud]['coords']
				dx = position_noeud[0]-coord2[0]
				dy = position_noeud[1]-coord2[1]
				if (Dx==0 and dx==0 and Dy*dy<0) or (Dy==0 and dy==0 and Dx*dx<0):
					if noeud != ancienne_position:	
						self.labyrinthe.remove_node(noeud)
						print("suppression noeud",noeud)
		
		#si chemin déjà parcouru par un autre robot
		else:
			print("chemin deja parcouru")
		
		direction = self.nouvelleDirection(robot,ancienne_position, nouvelle_position)   #on demande la direction à suivre
		print(self.getNodes())
		print(self.labyrinthe.edges())
		print(direction)
		robot.donnerOrdre(direction)    #on demande l'envoi de l'ordre de direction
		
	#fonction qui retourne l'identifiant d'un noeud de coordonnées spécifiées
	def rechercheNoeud(self, coordonnees):
		noeuds = self.labyrinthe.nodes()
		for n in noeuds:
			if self.labyrinthe.node[n]['coords'] == coordonnees:
				return n
		return -1
	
	#fonction qui répond si un chemin a été exploré ou non : retourne un booléen
	def estConnu(self, noeud_depart, noeud_arrivee):
		try:
			if self.labyrinthe[noeud_depart][noeud_arrivee]['weight'] == 0:
				return False
			return True
		except KeyError:
			self.labyrinthe.add_edge(noeud_depart,noeud_arrivee,weight=0)
			return False
	
	#construit les nouveaux chemins autour du nouveau carrefour découvert
	def construireIntersection(self, intersection, coord1, coord2, nouvelle_position):
		est = (intersection[0].split(";")[0])
		nord = (intersection[1].split(";")[0])
		ouest = (intersection[2].split(";")[0])
		sud = (intersection[3].split(";")[0])
		deplacementX = coord2[0] - coord1[0]
		deplacementY = coord2[1] - coord1[1]
		if est == "OUI":
			if not (deplacementX < 0 and deplacementY == 0):
				coord = (coord2[0]+0.1,coord2[1])   #coordonnée provisoire du carrefour est
				nouveau_noeud = self.prochain
				self.labyrinthe.add_node(nouveau_noeud, coords = coord)             #noeud est
				self.prochain += 1
				print("creation noeud ",nouveau_noeud," en :",coord)
				self.ajouterChemin(nouvelle_position,nouveau_noeud,0)				#création du chemin entre les deux noeuds
		if ouest == "OUI":
			if not (deplacementX > 0 and deplacementY == 0):
				coord = (coord2[0]-0.1,coord2[1])     #coordonnée provisoire du carrefour ouest
				nouveau_noeud = self.prochain
				self.labyrinthe.add_node(nouveau_noeud, coords = coord)              #noeud ouest
				self.prochain += 1
				print("creation noeud ",nouveau_noeud," en :",coord)
				self.ajouterChemin(nouvelle_position,nouveau_noeud,0)                 #création du chemin entre les deux noeuds
		if nord == "OUI":
			if not (deplacementX == 0 and deplacementY < 0):
				coord = (coord2[0],coord2[1]+0.1)      #coordonnée provisoire du carrefour nord
				nouveau_noeud = self.prochain
				self.labyrinthe.add_node(nouveau_noeud, coords = coord)               #noeud nord
				self.prochain += 1
				print("creation noeud ",nouveau_noeud," en :",coord)
				self.ajouterChemin(nouvelle_position,nouveau_noeud,0)                 #création du chemin entre les deux noeuds
		if sud == "OUI":
			if not (deplacementX == 0 and deplacementY > 0):
				coord = (coord2[0],coord2[1]-0.1)      #coordonnée provisoire du carrefour sud
				nouveau_noeud = self.prochain
				self.labyrinthe.add_node(nouveau_noeud, coords = coord)               #noeud sud
				self.prochain += 1
				print("creation noeud ",nouveau_noeud," en :",coord)
				self.ajouterChemin(nouvelle_position,nouveau_noeud,0)                 #création du chemin entre les deux noeuds
				
	def nouvelleDirection(self,robot,ancienne_position,nouvelle_position):
		coord1 = self.labyrinthe.node[ancienne_position]['coords']
		coord2 = self.labyrinthe.node[nouvelle_position]['coords']
		Dx = coord2[0]-coord1[0]
		Dy = coord2[1]-coord1[1]
		adjacents = self.labyrinthe.neighbors(nouvelle_position)
		objectif = -1
		i =0
		#on cherche un chemin non exploré
		while i < len(adjacents) and objectif == -1:
			if self.labyrinthe.edge[nouvelle_position][adjacents[i]]['weight'] == 0:
				objectif = adjacents[i]
				position_objectif = self.labyrinthe.node[objectif]['coords']
			i=i+1
		
		# si pas de possibilité, on revient au carrefour précédent
		if objectif ==-1:
			robot.supprimerDernierePosition()
			position_objectif = robot.dernierePositionConnue()
		
		# on retourne l'ordre de direction correpondant au noeud à aller découvrir
		dx = position_objectif[0]-coord2[0]
		dy = position_objectif[1]-coord2[1]
		if Dx==0 and dx==0:
			if Dy*dy>0:
				return "#face;"
			else:
				return "#turnback;"
		if Dy==0 and dy==0:
			if Dx*dx>0:
				return "#face;"
			else:
				return "#turnback;"
		if Dx==0:
			if Dy*dx>0:
				return "#droite;"
			else:
				return "#gauche;"
		if Dy==0:
			if Dx*dy>0:
				return "#gauche;"
			else:
				return "#droite;"
	
	# méthode qui renvoie la liste des noeuds pour relier de manière optimale deux points du labyrinthe
	def dijsktra(self, depart, arrivee):
		nx.dijkstra_path(self.labyrinthe, depart, arrivee)   #algorithme de Dijkstra
		
	# méthode qui retourne une liste de coordonnées des carrefours ajacents à un de coordonnées spécifiées
	def getNoeudsAdjacents(self,coords):
		noeud = self.rechercheNoeud(coords)
		liste = []
		if noeud != -1:
			adjacents = self.labyrinthe.neighbors(noeud)
			for i in adjacents:
				liste.append(self.labyrinthe.node[i]['coords'])
		return liste
		
	# retourne le nombre de chemins d'une intersection, et le nombre de chemins non explorés
	def analyserIntersection(self,coords):
		carrefour = self.rechercheNoeud(coords)
		liste = []
		non_explore = 0
		if carrefour != -1:
			adjacents = self.labyrinthe.neighbors(carrefour)
			for noeud in adjacents:
				if self.labyrinthe[carrefour][noeud] == 0:
					non_explore = non_explore + 1
		taille = len(adjacents)
		return (taille,non_explore)
		
	# retourne la direction (gauche,droite,etc...) à suivre à partir de l'ancienne, de l'actuelle et de la future intersection explorée par le robot
	def calculDirection(self, ancienne, depart, arrivee):
		coord1 = self.labyrinthe.node[ancienne]['coords']
		coord2 = self.labyrinthe.node[depart]['coords']
		coord3 = self.labyrinthe.node[arrivee]['coords']
		
		Dx = coord2[0]-coord1[0]
		Dy = coord2[1]-coord1[1]
		
		dx = coord3[0]-coord2[0]
		dy = coord3[1]-coord2[1]
		
		if Dx==0 and dx==0:
			if Dy*dy>0:
				return "#face;"
			else:
				return "#turnback;"
		if Dy==0 and dy==0:
			if Dx*dx>0:
				return "#face;"
			else:
				return "#turnback;"
		if Dx==0:
			if Dy*dx>0:
				return "#droite;"
			else:
				return "#gauche;"
		if Dy==0:
			if Dx*dy>0:
				return "#gauche;"
			else:
				return "#droite;"
				
	def getSemaphore(self):
		return self.semaphore