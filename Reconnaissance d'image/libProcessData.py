#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Librairie pour traiter les données
  Created: 23/04/2016
"""

#----------------------------------------------------------------------
def traiter(r, sock, arduino):
    """Fonction traitement données"""
    data = r.split('#')
    print(data)
    
    for i in data:
        if "bat_level" in i:
            sock.envoyer(i.split(';'))
    
        elif "bat_level" in i:
            arduino.Send("#bat_level;")
            