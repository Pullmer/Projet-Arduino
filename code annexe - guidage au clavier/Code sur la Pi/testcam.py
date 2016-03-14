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
camera.led = False #Eteint la led de la caméra
camera.resolution = (640, 480)
camera.framerate = 30
camera.video_stabilization = True #Default : false
#camera.shutter_speed = 40000 #Default : 0
camera.hflip, camera.vflip = True, True

try:
    while True:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            image = stream.array.tostring()
            serveur.sendData(image)
finally:
    del serveur
    camera.close()
    print("Camera closed")