#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas --<>
  Purpose: Test unitaire décodeur QRCode
  Created: 17/02/2016
"""

import picamera
import qrCodeDecoder

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.hflip, camera.vflip = True, True

camera.color_effects = (128,128) #noir et blanc

camera.capture('qrcode.jpg')
print("Lecture du QRCode : " + qrCodeDecoder.decode('qrcode.jpg'))
