#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas --<>
  Purpose: Test décodeur QRCode
  Created: 17/02/2016
"""

import picamera
import qrCodeDecoder
from os import remove

camera = picamera.PiCamera()
camera.resolution = (1280, 720)
camera.hflip, camera.vflip = True, True

camera.contrast = 70 #default 0
camera.brightness = 40 #default 50

camera.capture('qrcode.jpg')
print("Lecture du QRCode : " + qrCodeDecoder.decode('qrcode.jpg'))
