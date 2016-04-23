#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire communication arduino pi
  Created: 13/03/2016
"""

import comSerialArduino
import time

arduino = comSerialArduino.SerialArduino()

#----------------------------------------------------------------------
def main():
    """Fonction main"""
    try:
        while(True):
            arduino.Send("#bat_level;")
            time.sleep(2)
            a = arduino.Read()
            if len(a) > 0:
                print(a)
    
    except Exception as e:
        print(str(e))
           
    finally:
        arduino.close()
    
#----------------------------------------------------------------------
if __name__ == '__main__':
    main()
