#!/usr/bin/env python
#coding:utf-8
"""
    Autor: Cyprien
  Purpose: annexe creation d'une fenetre de controle manuel
"""

import sys
from thread import *
import Tkinter as tk
import time


#creation de la fenetre
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


ButtonPic=tk.Button(LabelFrameControles,text="Take Picture")
ButtonPic.pack(side=tk.TOP,pady=5)

LabelBatterie=tk.Label(LabelFrameControles,text="Niveau Batterie : ----")
LabelBatterie.pack(side=tk.TOP,pady=5)

ButtonBatterie=tk.Button(LabelFrameControles,text="Lire niveau batterie")
ButtonBatterie.pack(side=tk.TOP,pady=5)

root.mainloop()

