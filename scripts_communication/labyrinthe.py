# coding: utf-8

import networkx as nx
from robot import *

class Labyrinthe:

	def __init__(self):
		self.labyrinthe = nx.Graph()
		self.labyrinthe.add_node(0, coords = (0,0))
		self.labyrinthe.add_node(1, coords = (0,0.1))
		self.ajouterChemin(0,1,0)
		
	#def add_node(self, coordonnees, ancien_noeud):
		#nombre_noeuds = self.labyrinthe.number_of_nodes()
		#self.labyrinthe.add_node(nombre_noeuds, coords = coordonnees)
		#self.labyrinthe.add_edge(ancien_noeud, nombre_noeuds)
	
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
		self.labyrinthe.add_node(nombre_noeuds, coords = coordonnees)
		
	#executé quand un robot demande sa direction
	def demandeDirection(self, robot):
		coord1 = robot.getAnciennePosition()
		coord2 = robot.getPosition()
		nouvelle_position = self.rechercheNoeud(coord2)
		ancienne_position = self.rechercheNoeud(coord1)
		
		if nouvelle_position == -1:
			adjacents = self.labyrinthe.neighbors(ancienne_position)
			Dx = coord2[0]-coord1[0]
			Dy = coord2[1]-coord1[1]
			for noeud in adjacents:
				position_noeud = self.labyrinthe.node[noeud]['coords']
				dx = position_noeud[0]-coord1[0]
				dy = position_noeud[1]-coord1[1]
				if (Dx==0 and dx==0 and Dy*dy>0) or (Dy==0 and dy==0 and Dx*dx>0):
					nouvelle_position = noeud
			
			self.labyrinthe.node[nouvelle_position]['coords'] = coord2
			distance_parcourue = self.calculDistance(coord1,coord2)
			self.labyrinthe.edge[ancienne_position][nouvelle_position]['weight'] = distance_parcourue
			print("modification noeud ",nouvelle_position," en :",coord2)
			intersection = robot.getIntersection()
			self.construireIntersection(intersection, coord1, coord2,nouvelle_position)
			
		elif self.estConnu(ancienne_position, nouvelle_position) == False:		
			distance_parcourue = self.calculDistance(coord1,coord2)
			self.labyrinthe.edge[ancienne_position][nouvelle_position]['weight'] = distance_parcourue
			
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
			
		else:
			print("chemin deja parcouru")
		
		direction = self.nouvelleDirection(ancienne_position, nouvelle_position)
		print(self.getNodes())
		robot.donnerOrdre(direction)
		
	#fonction qui retourne l'identifiant d'un noeud de coordonnées spécifiées
	def rechercheNoeud(self, coordonnees):
		noeuds = self.labyrinthe.nodes()
		taille = len(noeuds)
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
		droite = (intersection[0].split(";")[0])
		face = (intersection[1].split(";")[0])
		gauche = (intersection[2].split(";")[0])
		deplacementX = coord2[0] - coord1[0]
		deplacementY = coord2[1] - coord2[0]
		if droite == "OUI":
			if deplacementX ==0:
				coord = (coord2[0]+0.1*deplacementY/abs(deplacementY),coord2[1])
				nombre_noeuds = self.labyrinthe.number_of_nodes()
				self.labyrinthe.add_node(nombre_noeuds, coords = coord)
				print("creation noeud ",nombre_noeuds," en :",coord)
				self.ajouterChemin(nouvelle_position,nombre_noeuds,0)
			else:
				coord = (coord2[0],coord2[1]-0.1*deplacementX/abs(deplacementX))
				nombre_noeuds = self.labyrinthe.number_of_nodes()
				self.labyrinthe.add_node(nombre_noeuds, coords = coord)
				print("creation noeud ",nombre_noeuds," en :",coord)
				self.ajouterChemin(nouvelle_position,nombre_noeuds,0)
		if gauche == "OUI":
			if deplacementX ==0:
				coord = (coord2[0]-0.1*deplacementY/abs(deplacementY),coord2[1])
				nombre_noeuds = self.labyrinthe.number_of_nodes()
				self.labyrinthe.add_node(nombre_noeuds, coords = coord)
				print("creation noeud ",nombre_noeuds," en :",coord)
				self.ajouterChemin(nouvelle_position,nombre_noeuds,0)
			else:
				coord = (coord2[0],coord2[1]+0.1*deplacementX/abs(deplacementX))
				nombre_noeuds = self.labyrinthe.number_of_nodes()
				self.labyrinthe.add_node(nombre_noeuds, coords = coord)
				print("creation noeud ",nombre_noeuds," en :",coord)
				self.ajouterChemin(nouvelle_position,nombre_noeuds,0)
		if face == "OUI":
			if deplacementX ==0:
				coord = (coord2[0],coord2[1]+0.1*deplacementY/abs(deplacementY))
				nombre_noeuds = self.labyrinthe.number_of_nodes()
				self.labyrinthe.add_node(nombre_noeuds, coords = coord)
				print("creation noeud ",nombre_noeuds," en :",coord)
				self.ajouterChemin(nouvelle_position,nombre_noeuds,0)
			else:
				coord = (coord2[0]+0.1*deplacementX/abs(deplacementX),coord2[1])
				nombre_noeuds = self.labyrinthe.number_of_nodes()
				self.labyrinthe.add_node(nombre_noeuds, coords = coord)
				print("creation noeud ",nombre_noeuds," en :",coord)
				self.ajouterChemin(nouvelle_position,nombre_noeuds,0)
				
	def nouvelleDirection(self,ancienne_position,nouvelle_position):
		return "tout droit"
	#def trajet(self, coordonnes, ancien_noeud):
	
	#def disjktra(self, depart, arrivee):