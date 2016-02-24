#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire reconnaissance de ligne
  Created: 16/02/2016
"""

import socket
import numpy
import cv2

#----------------------------------------------------------------------
def recvall(sock, count):
    """Receive data"""
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#----------------------------------------------------------------------
def nothing(x):
    """Magic function : Do nothing"""
    pass

#----------------------------------------------------------------------
def deleteSameLines(lines):
    """Permet de supprimer les lignes quasi-superposées"""
    index = list() # Liste qui contiendra les index des coordonnées à supprimer
    
    for i in range(len(lines)):
        rho_i, theta_i = lines[i][0]
        for j in range(len(lines)):
            rho_j, theta_j = lines[j][0]
            if theta_i != theta_j and rho_i != rho_j and abs(rho_i - rho_j) < 5 and abs(theta_i - theta_j) < 0.2:
                index.append(j)
                
    index = sorted(index[:len(index)/2], reverse=True) # Supprime les paires d'index et trie la liste
    for i in index:
        lines = numpy.delete(lines, i, 0)
        
    return lines

#----------------------------------------------------------------------

resolution = (640, 480) # Résolution caméra
TCP_IP = '10.12.152.110' # Adresse du serveur
TCP_PORT = 8123 # Port de communication

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

cv2.namedWindow('Reglages')
cv2.createTrackbar("t1", "Reglages", 132, 255, nothing)
cv2.createTrackbar("t2", "Reglages", 114, 255, nothing)
cv2.createTrackbar("Threshold", "Reglages", 100, 255, nothing) # Longueur minimale admissible d'un segment

while(True):

    length = recvall(sock, 16)
    
    if(length):
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8').reshape(resolution[1], resolution[0], -1) # Image reçue originale  
        
        #----------------------------------------------------------------------
        
        t1 = cv2.getTrackbarPos("t1", "Reglages")
        t2 = cv2.getTrackbarPos("t2", "Reglages")
        HoughLinesThreshold = cv2.getTrackbarPos("Threshold", "Reglages")
        
        imgGray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY) # Conversion en niveau de gris
        imgEdges = cv2.Canny(imgGray, t1, t2) # Détection des bords
        HoughLines = cv2.HoughLines(imgEdges, 1, numpy.pi/180, HoughLinesThreshold) # Transformée de Hough Lines
        imgHoughLines = data.copy()
        HoughLines = deleteSameLines(HoughLines)
        
        try:
            for i in range(min(30, len(HoughLines))):
                for rho, theta in HoughLines[i]:
                    a, b = numpy.cos(theta), numpy.sin(theta)
                    x0, y0 = a*rho, b*rho
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))
                
                    cv2.line(imgHoughLines, (x1, y1), (x2, y2), (0, 0, 255), 2) # Ajout des lignes détectées sur l'image originale      
        except:
            pass
        
        #cv2.imshow("imgGray", imgGray); 
        cv2.imshow("imgEdges", imgEdges); 
        cv2.imshow("Houghlines", imgHoughLines);  
        
        #----------------------------------------------------------------------
        
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break        

sock.close()
cv2.destroyAllWindows() 
