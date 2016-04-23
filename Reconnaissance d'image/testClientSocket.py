#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire communication socket (client)
  Created: 23/04/2016
"""

import libComSocket
import time

host = '10.0.0.5'
port = 1111

#----------------------------------------------------------------------
def main():
    """Main function"""
    
    try:
        sock = libComSocket.ComSocket(host, port)

        while True:
            sock.envoyer("yolo")
            time.sleep(1)
            
    except Exception as e:
        print(str(e))
        
    finally:
        sock.close()

if __name__ == '__main__':
    main()
    