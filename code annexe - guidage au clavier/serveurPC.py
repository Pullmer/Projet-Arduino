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

        print("Raw : "+data)
        #gérer les données recues ici
        if "Batterie" in data:
            LabelBatterie.config(text="Niveau Batterie : " + data[(len(data)-4):(len(data))])
        
        if not data:
            break

    conn.close()
#########################################################

#########################################################
#envoie la commande des moteurs à la Pi
def envoiCommande():
    global commande
    
    comm="#speedO;"
    comm+=str(commande[0])
    comm+=";"
    comm+=str(commande[1])
    comm+=";"
    print 'Commande envoyée : ' + comm
    conn.send(comm)
#########################################################

#########################################################
#fonctions executées lors d'un evenement clavier


def onKeyPress(event):
    global commande
    global spamG
    global spamD


    if (event.keysym=='e') and (not spamG):
        spamG = True
        commande[0]=100
        envoiCommande()
    elif (event.keysym=='d') and (not spamG):
        spamG = True
        commande[0]=-100
        envoiCommande()
    elif (event.keysym=='o') and (not spamD):
        spamD = True
        commande[1]=100
        envoiCommande()
    elif (event.keysym=='l') and (not spamD):
        spamD = True
        commande[1]=-100
        envoiCommande()
    


def onKeyRelease(event):
    global commande
    global spamG
    global spamD



    if (event.keysym=='e'):
        commande[0]=0
        spamG = False
    elif (event.keysym=='d'):
        commande[0]=0
        spamG = False
    elif (event.keysym=='o'):
        commande[1]=0
        spamD = False
    elif (event.keysym=='l'):
        commande[1]=0
        spamD = False

    envoiCommande()


#########################################################

#########################################################
#envoie commande avancer
def goUp(event):

    commande[0]=100
    commande[1]=100
    envoiCommande()
    
#########################################################

#########################################################
#envoie commande reculer
def goDown(event):

    commande[0]=-100
    commande[1]=-100
    envoiCommande()
    
#########################################################

#########################################################
#envoie commande tourner à gauche
def goLeft(event):

    commande[0]=-60
    commande[1]=+60
    envoiCommande()
    
#########################################################

#########################################################
#envoie commande tourner à droite
def goRight(event):

    commande[0]=60
    commande[1]=-60
    envoiCommande()
    
#########################################################


#########################################################
#envoi d'une commande nulle
def pasGo(event):

    commande[0]=0
    commande[1]=0
    envoiCommande()
    
#########################################################

#########################################################
#envoie la demande de niveau batterie
def askBat():

    comm="#bat_level;"
    conn.send(comm)
    
#########################################################

#########################################################
#prend une photo (pas encore implémenté sur la Pi
def askForPic():

    comm="#picture;"
    conn.send(comm)
    
#########################################################

#########################################################
#envoie la commande de coupure de connexion à la Pi et quitte tk
def quitter():

    comm="#quit;"
    conn.send(comm)
    s.close()
    root.destroy()
    
#########################################################

#creation de la fenetre et element graphiques
root = tk.Tk()
root.geometry('800x400')

root.resizable(0,0)

tk.Canvas(root, width=480, height=380, bg='grey').pack(side=tk.LEFT, padx=5, pady=5)

LabelFrameControles = tk.LabelFrame(root, borderwidth=2,text="Controles", relief=tk.GROOVE, height=370, width=280)
LabelFrameControles.pack(side=tk.LEFT, padx=5, pady=5)
LabelFrameControles.pack_propagate(0) #Empèche le frame de changer sa taille 

LabelFrameDirections = tk.LabelFrame(LabelFrameControles, borderwidth=2, text="Directions", relief=tk.GROOVE, height=120, width=160)
LabelFrameDirections.pack(side=tk.TOP)
LabelFrameDirections.pack_propagate(0)

ButtonUp=tk.Button(LabelFrameDirections,text="Avancer")
ButtonUp.pack(side=tk.TOP)
ButtonDown=tk.Button(LabelFrameDirections,text="Reculer")
ButtonDown.pack(side=tk.BOTTOM)
ButtonLeft=tk.Button(LabelFrameDirections,text="Gauche")
ButtonLeft.pack(side=tk.LEFT)
ButtonRight=tk.Button(LabelFrameDirections,text="Droite")
ButtonRight.pack(side=tk.RIGHT)

ButtonPic=tk.Button(LabelFrameControles,text="Take Picture",command=askForPic)
ButtonPic.pack(side=tk.TOP,pady=5)

LabelBatterie=tk.Label(LabelFrameControles,text="Niveau Batterie : ----")
LabelBatterie.pack(side=tk.TOP,pady=5)

ButtonBatterie=tk.Button(LabelFrameControles,text="Lire niveau batterie", command=askBat)
ButtonBatterie.pack(side=tk.TOP,pady=5)

ButtonQuit=tk.Button(LabelFrameControles,text="Quitter", command=quitter)
ButtonQuit.pack(side=tk.TOP,pady=5)


#creation des liens entre evenement clavier et fonctions à executer
root.bind('<KeyPress>', onKeyPress)
root.bind('<KeyRelease>', onKeyRelease)

ButtonUp.bind('<ButtonPress-1>',goUp)
ButtonUp.bind('<ButtonRelease-1>',pasGo)
ButtonDown.bind('<ButtonPress-1>',goDown)
ButtonDown.bind('<ButtonRelease-1>',pasGo)
ButtonLeft.bind('<ButtonPress-1>',goLeft)
ButtonLeft.bind('<ButtonRelease-1>',pasGo)
ButtonRight.bind('<ButtonPress-1>',goRight)
ButtonRight.bind('<ButtonRelease-1>',pasGo)

#variables globales utilisées pour la commande au clavier
commande=[0,0]
spamG = False
spamD = False


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
