# coding: utf-8

import socket
import time

x=0
y=0
bat = 100;
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1111))


while True :
	buffer = "DIRECTION?\n"
	buffer += "X : "+ str(x) +"\n"
	buffer += "Y : "+ str(y) +"\n"
	buffer += "Droite : OUI;NOIR\nFace : OUI;NOIR\nGauche : NON\n"
	buffer += "Batterie : " + str(bat)
	s.send(buffer)
	ordre = s.recv(255)
	print(ordre)
	if ordre=="straight":
		x = x+5
		bat = bat - 1
	s.send("done")
	time.sleep(5)

