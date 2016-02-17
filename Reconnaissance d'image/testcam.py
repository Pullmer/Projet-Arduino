#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: 
  Created: 16/02/2016
"""

import cameraDebugServer
import picamera
import picamera.array
import time

serveur = cameraDebugServer.CameraDebugServer()

camera = picamera.PiCamera()
camera.resolution = (400, 300)
camera.framerate = 5
camera.hflip, camera.vflip = True, True
time.sleep(1)

while True:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        image = stream.array.tostring()
        serveur.sendData(image)
    
del serveurDebug
del camera