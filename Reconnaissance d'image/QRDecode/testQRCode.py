#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas --<>
  Purpose: Lecteur QRCode
  Created: 17/02/2016
"""

import qrtools
import picamera

qrcode = qrtools.QR()

camera = picamera.PiCamera()
camera.resolution = (300, 300)
camera.hflip, camera.vflip = True, True

while True:
    ask = raw_input("Ready ? o/n : ")
    if ask == "o":
        camera.capture('qrcode.jpg')
        qrcode.decode('qrcode.jpg')
        print("Type des donnees : " + qrcode.data_type)
        print("Donnees lues : " + qrcode.data_to_string())
    else:
        break