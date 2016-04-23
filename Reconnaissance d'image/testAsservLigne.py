#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire suivi ligne
  Created: 13/04/2016
"""

import picamera.array
import cv2
import libReconnaissanceImage as libRI
import picamera
import comSerialArduino

arduino = comSerialArduino.SerialArduino()
camera = picamera.PiCamera() # Démarrage caméra
camera.led = False # Eteint la led de la caméra
camera.resolution = (640, 480) # Résolution
camera.framerate = 3
camera.video_stabilization = True # Default : false
camera.hflip, camera.vflip = True, True
stream = picamera.array.PiRGBArray(camera)

# Réglage PID
arduino.Send("#kp;0;#kd;0;#ki;0;#askPIDParameters;")
arduino.waitMsg(timeout=10)
a = arduino.Read()
if len(a) > 0:
    print(a)

#----------------------------------------------------------------------
def main():
    """Programme principal"""
    
    try:
        while True:
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
                print("Deviation : " + str(-1*libRI.lineToAngle((middleLine[0], middleLine[1]))))
                arduino.Send("#deviation;"  + str(-1*libRI.lineToAngle((middleLine[0], middleLine[1]))) + ";")
                
    except Exception as e:
        print(str(e))
        
    finally:
        arduino.Send("#stop;#kp;0;#kd;0;#ki;0;")
        camera.close()
        stream.close()
        arduino.close()
            
if __name__ == '__main__':
    main()
    