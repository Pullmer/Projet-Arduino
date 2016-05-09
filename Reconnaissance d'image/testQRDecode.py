#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas --<>
  Purpose: Test unitaire décodeur QRCode
  Created: 17/02/2016
"""

import picamera
import picamera.array
import qrCodeDecoder
import cv2
import time

with picamera.PiCamera() as camera:
    camera.hflip, camera.vflip = True, True
    camera.resolution = (640, 480)
    time.sleep(1)
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        stream.truncate(0)
        image = stream.array # Image capturée
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Conversion en niveau de gris
        cv2.imwrite('qrcode.jpg', image)

camera.close()
stream.close()
print("Message décodé : " + qrCodeDecoder.decode('qrcode.jpg'))
