#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test communication arduino pi
  Created: 13/03/2016
"""

import comSerialArduino
import time

arduino = comSerialArduino.SerialArduinoClass()

#----------------------------------------------------------------------
def main():
    """Fonction main"""
    
    while(True):
        arduino.Send("#yo;")
        time.sleep(2)
        print(arduino.Read())
        
    
#----------------------------------------------------------------------
if __name__ == '__main__':
    main()
