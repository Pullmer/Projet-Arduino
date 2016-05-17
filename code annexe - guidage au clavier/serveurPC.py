#!/usr/bin/env python
#coding:utf-8
"""
	Autor: Cyprien
  Purpose: Partie serveur (sur PC) du guidage clavier
"""

import socket
import sys
from thread import *
import Tkinter as tk
import time


#########################################################
# thread de gestion de reception de données
# cette fonction est appellée en créant un nouveau thread

def clientthread(conn):

    
    while True:
        
        data = conn.recv(1024)

        print data
        #gérer les données recues ici
        
        if not data:
            break

    conn.close()
#########################################################

#########################################################
#prend en arguement une liste de deux entiers compris entre 0 et MAX_SPEED
#envoie la commande des moteurs à la Pi
def envoiCommande():
    global commande
    s="speed0;"
    s+=str(commande[0])
    s+=";"
    s+=str(commande[1])
    s+=";"
    print 'Commande envoyée : ' + s
    conn.send(s)
#########################################################

#########################################################
#fonction executées lors d'un evenement clavier
#a chaque evenement clavier, on met à jour la commande et on l'envoie

def onKeyPress(event):
    global commande

    if (event.keysym=='Up'):
        commande[0]+=MAX_SPEED;
        commande[0]+=MAX_SPEED;
    elif (event.keysym=='Down'):
        commande[0]-=MAX_SPEED;
        commande[0]-=MAX_SPEED;
        
    
    envoiCommande()


def onKeyRelease(event):
    global commande

    if (event.keysym=='Up'):
        commande[0]-=MAX_SPEED;
        commande[0]-=MAX_SPEED;

    envoiCommande()


#########################################################


#creation de la fenetre
root = tk.Tk()
root.geometry('300x200')
text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 12))
text.pack()

#creation des liens entre evenement clavier et fonctions à executer
root.bind('<KeyPress>', onKeyPress)
root.bind('<KeyRelease>', onKeyRelease)

commande=[0,0]


#creation et initialisation du socket
HOST = ''
PORT = 1111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(True)
print 'Socket now listening'


while 1:
    print 'Wait to accept a connection'
    conn, addr = s.accept() 
    print 'Connected with ' + addr[0] + ':' + str(addr[1]) 

    
    #créé un nouveau thread pour gerer la reception de données
    start_new_thread(clientthread ,(conn,))

    #boucle du thread principal qui gère les envois de données
    root.mainloop()
    #conn.send(a)

s.close()
