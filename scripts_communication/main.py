# coding: utf-8 
from server import *
from labyrinthe import Labyrinthe

labyrinthe = Labyrinthe()
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",1111))

while True:
    
    newthread = ClientThread(ip, port, clientsocket, labyrinthe)
    newthread.start()
