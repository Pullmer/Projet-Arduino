#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas --<>
  Purpose: Lecteur QRCode
  Created: 17/02/2016
"""

import qrtools

def decode(imageRef):
    """Décode le QRCode d'imageRef"""
    qrcode = qrtools.QR()
    qrcode.decode(imageRef)        
    return qrcode.data_to_string()
        