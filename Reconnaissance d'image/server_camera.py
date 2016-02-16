#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 15/02/2016
"""

import socket
import picamera
import picamera.array

TCP_IP = ''
TCP_PORT = 8123

camera = picamera.PiCamera()
camera.resolution = (640, 360)
camera.start_preview()
camera.hflip, camera.vflip = True, True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)
conn, addr = s.accept()

end = False

while(not end):
    
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        image = stream.array.tostring()
        conn.send(str(len(image)).ljust(16))
        conn.send(image)

s.close()

