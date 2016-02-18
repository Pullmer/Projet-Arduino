#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test reconnaissance de ligne
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
    """Do nothing"""
    pass
    
#----------------------------------------------------------------------

resolution = (640, 480) # Résolution caméra
TCP_IP = '10.12.152.110' # Adresse du serveur
TCP_PORT = 8123 # Port de communication

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

cv2.namedWindow('Reglages')
cv2.createTrackbar("t1", "Reglages", 47, 255, nothing)
cv2.createTrackbar("t2", "Reglages", 29, 255, nothing)
cv2.createTrackbar("Threshold", "Reglages", 159, 255, nothing) # Longueur minimale admissible d'un segment

while(True):

    length = recvall(sock, 16)
    
    if(length):
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8').reshape(resolution[1], resolution[0], -1)    
        
        #----------------------------------------------------------------------
        
        t1 = cv2.getTrackbarPos("t1", "Reglages")
        t2 = cv2.getTrackbarPos("t2", "Reglages")
        HoughLinesThreshold = cv2.getTrackbarPos("Threshold", "Reglages")
        
        imgGray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY) # Conversion en niveau de gris
        imgEdges = cv2.Canny(imgGray, t1, t2) # Détection des bords
        HoughLines = cv2.HoughLines(imgEdges, 1, numpy.pi/180, HoughLinesThreshold)
        imgHoughLines = data.copy()
        
        try:
            for i in range(min(10, len(HoughLines))):
                for rho, theta in HoughLines[i]:
                    a, b = numpy.cos(theta), numpy.sin(theta)
                    x0, y0 = a*rho, b*rho
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0 + 1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 - 1000*(a))
                
                    cv2.line(imgHoughLines, (x1, y1), (x2, y2), (0, 0, 255), 2)       
        except:
            pass
        
        cv2.imshow("imgEdges", imgEdges);  
        cv2.imshow("Houghlines", imgHoughLines);  
        
        #----------------------------------------------------------------------
        
    if cv2.waitKey(5) == 27: # Attend la touche "échap pendant 10ms"
        print("Finish")
        break

sock.close()
cv2.destroyAllWindows() 
