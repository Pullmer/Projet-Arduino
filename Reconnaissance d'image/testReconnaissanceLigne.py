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

resolution = (640, 480) #Résolution caméra
TCP_IP = '10.12.152.110' #Adresse du serveur
TCP_PORT = 8123 #Port de communication

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
    """Magic function : do nothing"""
    pass

#----------------------------------------------------------------------
def rhothetaToPoints(rho, theta):
    """Conversion de rho et theta en deux points constituant une droite"""
    a, b = numpy.cos(theta), numpy.sin(theta)
    x0, y0 = a*rho, b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    
    if y1 > y2:
        (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
    return (x1, y1), (x2, y2)

#----------------------------------------------------------------------
def lineToAngle(((x1, y1), (x2, y2))):
    """Calcul l'angle d'une droite par rapport à la verticale"""
    if y1 != y2:
        return numpy.arctan(float(x1 - x2)/(y1 - y2))*180/numpy.pi
    else:
        return 90.0

#----------------------------------------------------------------------
def keepVerticalLines(lines):
    """Garde uniquement les lignes verticales"""
    if lines is not None:
        index = list()
        for i in range(len(lines)):
            for rho, theta in lines[i]:
                if not (theta > numpy.pi/180*130 or theta < numpy.pi/180*40):
                    index.append(i)
    
        #Suppression des lignes horizontales
        for i in sorted(index, reverse=True):
            lines = numpy.delete(lines, i, 0)
     
    return lines

#----------------------------------------------------------------------
def deleteSameLines(lines):
    """Supprime les lignes quasi-superposées"""
    return lines
    
#----------------------------------------------------------------------
def drawMiddleLine(img, lines):
    """Trace la ligne qui doit être suivie par le robot"""
    if lines is not None:
        
        #On supprime les lignes horizontales
        lines = keepVerticalLines(lines)
        
        if len(lines) >= 2:
            (x1a, y1a), (x2a, y2a) = rhothetaToPoints(lines.item(0), lines.item(1))
            (x1b, y1b), (x2b, y2b) = rhothetaToPoints(lines.item(2), lines.item(3))    
            x1 = (x1a + x1b)/2
            x2 = (x2a + x2b)/2
            y1 = (y1a + y1b)/2
            y2 = (y2a + y2b)/2
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 7)
            print("Deviation : {0}".format(lineToAngle(((x1,y1),(x2,y2)))))
            
    return drawLines(img, lines, color=(0, 255, 0))
    
#----------------------------------------------------------------------
def drawLines(img, lines, color=(0, 0, 255), thickness=2):
    """Affiche les lignes sur img"""
    if lines is not None:
        for x in lines:
            rho = numpy.take(x, [0])
            theta = numpy.take(x, [1])
            (x1, y1), (x2, y2) = rhothetaToPoints(rho, theta)
            cv2.line(img, (x1, y1), (x2, y2), color, thickness) #Ajout des lignes sur l'image originale
            
    return img

#----------------------------------------------------------------------
def main():
    """Fonction main"""
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))
    print("Socket ouvert")
    
    cv2.namedWindow('Reglages')
    cv2.resizeWindow('Reglages', 400, 400)
    cv2.createTrackbar("t1", "Reglages", 180, 255, nothing)
    cv2.createTrackbar("t2", "Reglages", 110, 255, nothing)
    cv2.createTrackbar("Threshold", "Reglages", 90, 255, nothing) #Longueur minimale admissible d'un segment
    cv2.createTrackbar("minDist", "Reglages", 90, 255, nothing)
    cv2.createTrackbar("param1", "Reglages", 80, 255, nothing)
    cv2.createTrackbar("param2", "Reglages", 140, 255, nothing)
    cv2.createTrackbar("minRadius", "Reglages", 50, 255, nothing)
    cv2.createTrackbar("maxRadius", "Reglages", 90, 255, nothing)
    
    while(True):
        length = recvall(sock, 16)
        
        if(length):
            stringData = recvall(sock, int(length))
            data = numpy.fromstring(stringData, dtype='uint8').reshape(resolution[1], resolution[0], -1) #Image reçue 
            imgHoughLines = data.copy() #Création d'une copie de l'image
            imgHoughCircle = data.copy() #Création d'une copie de l'image
            
            #----------------------------------------------------------------------
            
            t1 = cv2.getTrackbarPos("t1", "Reglages")
            t2 = cv2.getTrackbarPos("t2", "Reglages")
            HoughLinesThreshold = cv2.getTrackbarPos("Threshold", "Reglages")
            mindist = cv2.getTrackbarPos("minDist", "Reglages")
            p1 = cv2.getTrackbarPos("param1", "Reglages")
            p2 = cv2.getTrackbarPos("param2", "Reglages")
            minR = cv2.getTrackbarPos("minRadius", "Reglages")
            maxR = cv2.getTrackbarPos("maxRadius", "Reglages")
            
            imgGray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY) #Conversion en niveau de gris
            imgEdges = cv2.Canny(imgGray, t1, t2, apertureSize=3) #Binarisation de l'image
            houghLines = cv2.HoughLines(imgEdges, 3, 5*numpy.pi/180, HoughLinesThreshold) #Transformée de Hough Lines
            houghLines = deleteSameLines(houghLines)
            imgHoughLines = drawLines(imgHoughLines, houghLines)
            imgHoughLines = drawMiddleLine(imgHoughLines, houghLines)
            
            imgBlurred = cv2.medianBlur(imgGray, 5)
            houghCircles = cv2.HoughCircles(imgBlurred, cv2.HOUGH_GRADIENT, 3, mindist, param1=p1, param2=p2, minRadius=minR, maxRadius=maxR)
            if houghCircles is not None:
                houghCircles = numpy.uint16(numpy.around(houghCircles))
                for i in houghCircles[0,:]:
                    # draw the outer circle
                    cv2.circle(imgHoughCircle, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # draw the center of the circle
                    cv2.circle(imgHoughCircle, (i[0], i[1]), 2, (0, 0, 255), 3)            

            #Affichage 
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
