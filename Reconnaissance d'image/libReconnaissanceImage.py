#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Bibliothèque qui gère la reconnaissance d'image
  Created: 11/04/2016
"""

import numpy
import cv2

#----------------------------------------------------------------------
def rhothetaToXY(rho, theta):
    """Conversion d'une droite de paramètres rho et theta (transformée de HoughLines) en coordonnées cartésiennes"""
    a, b = numpy.cos(theta), numpy.sin(theta)
    x0, y0 = a*rho, b*rho
    x1 = int(x0 + 2000*(-b))
    y1 = int(y0 + 2000*(a))
    x2 = int(x0 - 2000*(-b))
    y2 = int(y0 - 2000*(a))
    
    if y1 > y2:
        (x1, y1), (x2, y2) = (x2, y2), (x1, y1)
    return (x1, y1), (x2, y2)

#----------------------------------------------------------------------
def lineToAngle(((x1, y1), (x2, y2))):
    """Conversion d'une droite en un angle par rapport à la verticale"""
    if y1 != y2:
        return numpy.arctan(float(x1 - x2)/(y1 - y2))*180/numpy.pi
    else:
        return 90.0

#----------------------------------------------------------------------
def keepVerticalLines(lines):
    """Garde uniquement les lignes verticales"""
    if lines is not None:
        verticalLines = lines.copy()
        index = list()
        for i in range(len(lines)):
            for rho, theta in lines[i]:
                if not (theta > numpy.pi/180*130 or theta < numpy.pi/180*40):
                    index.append(i)
    
        # Suppression des lignes horizontales
        for i in sorted(index, reverse=True):
            verticalLines = numpy.delete(verticalLines, i, 0)
     
        return verticalLines
    
    else:
        return lines

#----------------------------------------------------------------------
def keepHorizontalLines(lines):
    """Garde uniquement les lignes horizontales"""
    if lines is not None:
        horizontalLines = lines.copy()
        index = list()
        for i in range(len(lines)):
            for rho, theta in lines[i]:
                if (theta > numpy.pi/180*130 or theta < numpy.pi/180*40):
                    index.append(i)
    
        # Suppression des lignes verticales
        for i in sorted(index, reverse=True):
            horizontalLines = numpy.delete(horizontalLines, i, 0)
     
        return horizontalLines
    
    else:
        return lines

#----------------------------------------------------------------------
def drawLines(img, lines, color=(0, 0, 255), thickness=2):
    """Affiche les lignes (lines) sur l'image (img)"""
    if lines is not None:
        for x in lines:
            rho = numpy.take(x, [0])
            theta = numpy.take(x, [1])
            (x1, y1), (x2, y2) = rhothetaToXY(rho, theta) # Conversion en coordonnées cartésiennes
            cv2.line(img, (x1, y1), (x2, y2), color, thickness) # Ajout des lignes sur l'image
            
    return img

#----------------------------------------------------------------------
def drawLine(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2):
    """Affiche la ligne sur l'image (img)"""
    cv2.line(img, (x1, y1), (x2, y2), color, thickness) # Ajout des lignes sur l'image
            
    return img

#----------------------------------------------------------------------
def getMiddleLine(lines):
    """Retourne la ligne de la route, c'est la ligne que doit suivre le robot"""
    if lines is not None:
        # On supprime les lignes horizontales
        verticalLines = keepVerticalLines(lines)
        
        if len(verticalLines) >= 2: # L'algorithme de HoughLines trie les lignes par ordre de probabilité, on sélectionne donc les 2 premières
            (x1a, y1a), (x2a, y2a) = rhothetaToXY(verticalLines.item(0), verticalLines.item(1))
            (x1b, y1b), (x2b, y2b) = rhothetaToXY(verticalLines.item(2), verticalLines.item(3))    
            x1 = (x1a + x1b)/2
            x2 = (x2a + x2b)/2
            y1 = (y1a + y1b)/2
            y2 = (y2a + y2b)/2
            
            return (x1,y1), (x2,y2)
        
    return None

#----------------------------------------------------------------------
def getPixelColor(img, (x, y)):
    """Donne la couleur BlueGreenRed d'un pixel"""
    print((x, y))
    print("Blue : " + str(img[y][x][0]))
    print("Green : " + str(img[y][x][1]))
    print("Red : " + str(img[y][x][2]))