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
import libReconnaissanceImage as libRI

resolution = (640, 480) # Résolution caméra
TCP_IP = '10.12.152.157' # Adresse du serveur
TCP_PORT = 8123 # Port de communication

#----------------------------------------------------------------------
def recvall(sock, count):
    """Receive data via network"""
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
def main():
    """Fonction main"""
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))
    print("Socket ouvert")
    
    # Création des barres de réglages
    cv2.namedWindow('Reglages')
    cv2.resizeWindow('Reglages', 400, 400)
    cv2.createTrackbar("t1", "Reglages", 70, 255, nothing) # Seuil houghlines t1
    cv2.createTrackbar("t2", "Reglages", 70, 255, nothing) # Seuil houghlines t2
    cv2.createTrackbar("Threshold", "Reglages", 100, 500, nothing) # Longueur minimale admissible d'un segment
    cv2.createTrackbar("minDist", "Reglages", 110, 255, nothing) # distance minimale entre chaque cercles de houghcircles
    cv2.createTrackbar("param1", "Reglages", 70, 255, nothing)
    cv2.createTrackbar("param2", "Reglages", 70, 255, nothing)
    cv2.createTrackbar("minRadius", "Reglages", 70, 255, nothing) # rayon cercle minimum
    cv2.createTrackbar("maxRadius", "Reglages", 85, 255, nothing) # rayon cercle maximum
    
    while(True):
        length = recvall(sock, 16)
        
        if(length):
            stringData = recvall(sock, int(length))
            data = numpy.fromstring(stringData, dtype='uint8').reshape(resolution[1], resolution[0], -1) #Image reçue 
            imgHoughLines = data.copy() # Création d'une copie de l'image
            imgHoughCircle = data.copy() # Création d'une copie de l'image
            
            #----------------------------------------------------------------------
            
            # Actualisation paramètres
            t1 = cv2.getTrackbarPos("t1", "Reglages")
            t2 = cv2.getTrackbarPos("t2", "Reglages")
            HoughLinesThreshold = cv2.getTrackbarPos("Threshold", "Reglages")
            mindist = cv2.getTrackbarPos("minDist", "Reglages")
            p1 = cv2.getTrackbarPos("param1", "Reglages")
            p2 = cv2.getTrackbarPos("param2", "Reglages")
            minR = cv2.getTrackbarPos("minRadius", "Reglages")
            maxR = cv2.getTrackbarPos("maxRadius", "Reglages")
            
            # Reconnaissance lignes
            imgGray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY) # Conversion en niveau de gris
            imgEdges = cv2.Canny(imgGray, t1, t2, apertureSize=3) # Binarisation de l'image
            houghLines = cv2.HoughLines(imgEdges, 3, 3*numpy.pi/180, HoughLinesThreshold) # Transformée de Hough Lines
            imgHoughLines = libRI.drawLines(imgHoughLines, libRI.keepHorizontalLines(houghLines)) # Tracée lignes horizontales
            imgHoughLines = libRI.drawLines(imgHoughLines, libRI.keepVerticalLines(houghLines), color=(0,255,0)) # Tracée lignes verticales
            middleLine = libRI.getMiddleLine(houghLines) # Acquisition ligne de la route
            if middleLine is not None:
                imgHoughLines = libRI.drawLine(imgHoughLines, middleLine[0], middleLine[1], color=(0,255,255)) # Trace la ligne à suivre par le robot
                print("Deviation : " + str(libRI.lineToAngle((middleLine[0], middleLine[1])))) # Affichage de l'erreur angulaire
            
            # Reconnaissance cercle et couleur
            imgBlurred = cv2.medianBlur(imgGray, 5)
            houghCircles = cv2.HoughCircles(imgBlurred, cv2.HOUGH_GRADIENT, 3, mindist, param1=p1, param2=p2, minRadius=minR, maxRadius=maxR) # Transformée de HoughCircle
            if houghCircles is not None:
                houghCircles = numpy.uint16(numpy.around(houghCircles))
                for i in houghCircles[0,:]:
                    cv2.circle(imgHoughCircle, (i[0], i[1]), i[2], (0, 255, 0), 2) # Affichage cercles
                    cv2.circle(imgHoughCircle, (i[0], i[1]), 2, (0, 0, 255), 3) # Affichage centres des cercles
                    color = libRI.getPixelColor(data, (i[0], i[1])) # Affichage couleur pixel
                    if(i[0] < 320 and color[0] < 220 and color[0] > 134 and color[1] < 160 and color[1] > 110 and color[2] < 80 and color[2] > 35):
                        print("Panneau stop bleu detecte !\r\n")

            # Affichage des images
            cv2.imshow("imgEdges", imgEdges);
            cv2.imshow("imgHoughLines", imgHoughLines);
            cv2.imshow("imgHoughCircle", imgHoughCircle);
            
            #----------------------------------------------------------------------
            
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break        
    
    sock.close()
    print("Socket closed")
    cv2.destroyAllWindows() 
    
#----------------------------------------------------------------------
if __name__ == '__main__':
    main()
