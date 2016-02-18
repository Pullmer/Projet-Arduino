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

serveur = cameraDebugServer.CameraDebugServer()

camera = picamera.PiCamera()
camera.led = False
camera.resolution = (640, 480)
camera.framerate = 15
camera.hflip, camera.vflip = True, True

while True:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        image = stream.array.tostring()
        serveur.sendData(image)
    
del serveurDebug
del camera