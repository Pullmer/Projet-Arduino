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
#envoie la commande des moteurs à la Pi
def envoiCommande():
    global commande
    
    s="#speedO;"
    s+=str(commande[0])
    s+=";"
    s+=str(commande[1])
    s+=";"
    print 'Commande envoyée : ' + s
    conn.send(s)
#########################################################

#########################################################
#fonctions executées lors d'un evenement clavier


def onKeyPress(event):
    global commande
    global spam

    if (not spam):
        spam = True
        
        if (event.keysym=='e'):
            commande[0]=100
        elif (event.keysym=='d'):
            commande[0]=-100
        elif (event.keysym=='o'):
            commande[1]=100
        elif (event.keysym=='l'):
            commande[1]=-100
           
        envoiCommande()

    


def onKeyRelease(event):
    global commande
    global spam

    spam = False

    if (event.keysym=='e'):
        commande[0]=0
    elif (event.keysym=='d'):
        commande[1]=0
    elif (event.keysym=='o'):
        commande[0]=0
    elif (event.keysym=='l'):
        commande[1]=0

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


#variables globales utilisées pour la commande au clavier
commande=[0,0]
spam = False

#creation et initialisation du socket
HOST = '10.0.0.7' #Adresse de l'HOTE (donc du PC)
PORT = 1115

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



print 'Wait to accept a connection'
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1]) 

#créé un nouveau thread pour gerer la reception de données
start_new_thread(clientthread ,(conn,))

#boucle du thread principal qui gère les envois de données
root.mainloop()
#conn.send(a)
s.close()
