import networkx as nx

class Labyrinthe:

	def __init__(self):
		self.labyrinthe = nx.Graph()
		
	def add_node(self, coordonnees, ancien_noeud):
		nombre_noeuds = self.labyrinthe.number_of_nodes()
		self.labyrinthe.add_node(nombre_noeuds, coords = coordonnees)
		self.labyrinthe.add_edge(ancien_noeud, nombre_noeuds)
	
	def getNodes(self):
		return self.labyrinthe.nodes()
		
	def calculDistance(self, coord1, coord2):
		return ((coord2[0]-coord1[0])^2 + (coord2[1]-coord1[1])^2)
		
	
	def ajouterChemin(self, depart, arrivee, longueur):
		self.labyrinthe.add_edge(depart,arrivee, weight = longueur)
		
	def ajouterNoeud(self, coordonees):
		nombre_noeuds = self.labyrinthe.number_of_nodes()
		self.labyrinthe.add_node(nombre_noeuds, coords = coordonnees)
		
	#def trajet(self, coordonnes, ancien_noeud):
	
	#def disjktra(self, depart, arrivee):