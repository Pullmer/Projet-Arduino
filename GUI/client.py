# coding: utf-8

"""
	Author : Nicolas Gonçalves
	Purpose : Simulation de la trajectoire d'un robot
"""


import socket
import time

x=0
y=0
bat = 100;
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1111))
ordre = s.recv(255)
print(ordre)
if ordre =="#face;":

	i=1
	y=y+5
	buffer = "DIRECTION?\n"
	buffer += "X : "+ str(x) +"\n"
	buffer += "Y : "+ str(y) +"\n"
	buffer += "Droite : OUI;NOIR\nFace : OUI;NOIR\nGauche : NON\n"
	buffer += "Batterie : " + str(bat)
	s.send(buffer)
	ordre = s.recv(255)
	print(ordre)
	bat = bat - 1
	time.sleep(5)

	k=5
	while k>0 :
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
		
		s.send(buffer)
		ordre = s.recv(255)
		print(ordre)
		bat = bat - 1
		i = (i+1)%4
		time.sleep(5)
		k = k-1
	print("fin")
	s.send("CLOSE_CONNEXION")
