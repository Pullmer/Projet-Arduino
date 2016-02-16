#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: 
  Created: 16/02/2016
"""

import server_camera
import picamera
import picamera.array

camera = picamera.PiCamera()
camera.resolution = (444, 250)    
camera.hflip, camera.vflip = True, True

serveur = server_camera.CameraDebugServer()

while True:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        image = stream.array.tostring()
        serveur.sendData(image)