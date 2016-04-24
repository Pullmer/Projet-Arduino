#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire communication socket (serveur)
  Created: 23/04/2016
"""

import socket

HOST = ''   
PORT = 1111

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(True)
    conn, addr = s.accept()
    print("Socket ouvert : " + str(addr))
    while True:
        a = raw_input("Entrez un msg : ")
        conn.send(a)
        print(conn.recv(1024))

except Exception as e:
    print(str(e))

finally:
    s.close()