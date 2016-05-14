#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: Test unitaire communication socket (serveur)
"""

import socket
import sys
from thread import *

HOST = ''   
PORT = 1111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(True)
print 'Socket now listening'

def clientthread(conn):
    #Sending message to connected client

    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        print data
        if not data:
            break

    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread
    start_new_thread(clientthread ,(conn,))
    while 1:
        
        a = raw_input("entrez un msg : ")
        conn.send(a)

s.close()
