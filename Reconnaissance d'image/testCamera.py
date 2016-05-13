#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire streaming caméra, code à lancer sur la Raspberry Pi
  Created: 16/02/2016
"""

import cameraDebugServer
import picamera
import picamera.array

serveur = cameraDebugServer.CameraDebugServer() # Démarrage du serveur de streaming

camera = picamera.PiCamera() # Démarrage caméra
camera.led = False # Eteint la led de la caméra
camera.resolution = (640, 480) # Résolution
camera.framerate = 3
camera.video_stabilization = True # Default : false
camera.hflip, camera.vflip = True, True

try:
    while True:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr') # Prise d'une image
            image = stream.array.tostring() # Conversion en string
            serveur.sendData(image) # Envoi de l'image sur le réseau
            
except Exception as e:
    print(str(e))
    
finally:
    serveur.close()
    camera.close()
    