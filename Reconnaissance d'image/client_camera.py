#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 16/02/2016
"""

import socket
import numpy
import cv2

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = '10.0.0.200'
TCP_PORT = 8123

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

cv2.namedWindow('Client')

end = False

while(not end):
    
    length = recvall(sock, 16)
    if(length):
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8').reshape(360, 640, -1)
        
        cv2.imshow('Client', data)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        end = True

sock.close()
cv2.destroyAllWindows() 