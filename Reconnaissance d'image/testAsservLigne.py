#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire suivi ligne
  Created: 13/04/2016
"""

import picamera.array
import numpy
import cv2
import libReconnaissanceImage as libRI
import picamera
import comSerialArduino
import time

arduino = comSerialArduino.SerialArduino()
camera = picamera.PiCamera() # Démarrage caméra
camera.led = False # Eteint la led de la caméra
camera.resolution = (640, 480) # Résolution
camera.framerate = 4
camera.video_stabilization = True # Default : false
camera.hflip, camera.vflip = True, True
stream = picamera.array.PiRGBArray(camera)

#----------------------------------------------------------------------
def main():
    """Programme principal"""
    
    try:
        while True:
            debut = time.time()
            camera.capture(stream, format='bgr')
            stream.truncate(0)
            data = stream.array # Image capturée
            imgHoughLines = data.copy() # Création d'une copie de l'image
            
            # Reconnaissance lignes
            imgGray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY) # Conversion en niveau de gris
            imgEdges = cv2.Canny(imgGray, 70, 70, apertureSize=3) # Binarisation de l'image
            houghLines = cv2.HoughLines(imgEdges, 3, 3*numpy.pi/180, 100) # Transformée de Hough Lines
                
            middleLine = libRI.getMiddleLine(houghLines) # Acquisition ligne de la route
            if middleLine is not None:
                print("Deviation : " + str(libRI.lineToAngle((middleLine[0], middleLine[1]))))
                #arduino.Send("#deviation;"  + ";")
                
            a = arduino.Read()
            if len(a) > 0:
                print(a)
            
    finally:
        camera.close()
        stream.close()
        print("Error : stream and camera closed")
            
if __name__ == '__main__':
    main()