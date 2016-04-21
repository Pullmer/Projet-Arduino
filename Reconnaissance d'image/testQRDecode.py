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
camera.resolution = (1920, 1080)
camera.hflip, camera.vflip = True, True

camera.color_effects = (128,128) # noir et blanc

camera.capture('qrcode.jpg')
print("Message décodé : " + qrCodeDecoder.decode('qrcode.jpg'))
