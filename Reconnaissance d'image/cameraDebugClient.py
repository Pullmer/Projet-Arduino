#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Client pour recevoir un flux vidéo par le réseau
  Created: 16/02/2016
"""

import socket
import numpy
import cv2

#----------------------------------------------------------------------
def recvall(sock, count):
    """"""
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#----------------------------------------------------------------------

resolution = (640, 480)
TCP_IP = '10.12.152.110' # Adresse du serveur
TCP_PORT = 8123

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
cv2.namedWindow('Client')

while(True):

    length = recvall(sock, 16)
    
    if(length):
        stringData = recvall(sock, int(length))
        data = numpy.fromstring(stringData, dtype='uint8').reshape(resolution[1], resolution[0], -1)
        cv2.imshow('Client', data)           

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

sock.close()
cv2.destroyAllWindows() 
