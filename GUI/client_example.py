# coding: utf-8 

import time
import socket
import threading

class Reception(threading.Thread):
	
	def __init__(self,client,socket,semaphore):
		threading.Thread.__init__(self)   #on appelle le constructeur de la classe Thread
		self.socket = socket
		self.client = client
		self.semaphore = semaphore
		
	def run(self):
		while True:
			self.semaphore.acquire()
			try:
				reception = self.socket.recv(2048)
				self.traiter(reception)
			except:
				pass
			self.semaphore.release()
			
	def traiter(self,texte):
		print(texte)
		if texte == "pause":
			self.client.setState("pause")
		elif texte == "start":
			self.client.setState("working")
			

class Client():
	def __init__(self):
		self.state = "ready"
		
	def setState(self,etat):
		self.state = etat
		
	def getState(self):
		return self.state
		

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.settimeout(1)
semaphore = threading.Semaphore(value=1)
client = Client()
ecoute = Reception(client,socket,semaphore)
socket.connect(("127.0.0.1", 1111))
ecoute.start()

x=0
y=0
bat = 100

while client.getState() != "working":
	time.sleep(1)
y = y+5
buffer = "DIRECTION?\n"
buffer += "X : "+ str(x) +"\n"
buffer += "Y : "+ str(y) +"\n"
buffer += "Droite : OUI;NOIR\nFace : OUI;NOIR\nGauche : NON\n"
buffer += "Batterie : " + str(bat)
semaphore.acquire()
socket.send(buffer)
semaphore.release()
bat = bat - 1
time.sleep(5)
i=1

while True:
	if client.getState() == "working":
		if i==1:
			x = x+5
			buffer = "DIRECTION?\n"
			buffer += "X : "+ str(x) +"\n"
			buffer += "Y : "+ str(y) +"\n"
			buffer += "Droite : NON\nFace : NON\nGauche : OUI;NOIR\n"
			buffer += "Batterie : " + str(bat)
		if i==2:
			y = y+5
			buffer = "DIRECTION?\n"
			buffer += "X : "+ str(x) +"\n"
			buffer += "Y : "+ str(y) +"\n"
			buffer += "Droite : NON\nFace : NON\nGauche : OUI;NOIR\n"
			buffer += "Batterie : " + str(bat)
		if i==3:
			x = x-5
			buffer = "DIRECTION?\n"
			buffer += "X : "+ str(x) +"\n"
			buffer += "Y : "+ str(y) +"\n"
			buffer += "Droite : NON\nFace : NON\nGauche : OUI;NOIR\n"
			buffer += "Batterie : " + str(bat)
		if i==0:
			y = y-5
			buffer = "DIRECTION?\n"
			buffer += "X : "+ str(x) +"\n"
			buffer += "Y : "+ str(y) +"\n"
			buffer += "Droite : NON\nFace : OUI;NOIR\nGauche : OUI;NOIR\n"
			buffer += "Batterie : " + str(bat)		
		semaphore.acquire()
		socket.send(buffer)
		semaphore.release()
		i = (i+1)%4
		bat = bat - 1
	time.sleep(5)