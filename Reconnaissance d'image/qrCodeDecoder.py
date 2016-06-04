#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Lecteur QRCode
  Created: 17/02/2016
"""

import qrtools
import picamera

########################################################################
class QRDecode:
    """Classe pour décoder les QRCode"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.camera = picamera.PiCamera() # Démarrage caméra
        self.camera.resolution = (1296, 972) # Résolution de l'image

    def decodeQRCode(self):
        """Prend une image et décode"""
        camera.capture('qrcode.jpg')
        qrcode = qrtools.QR()
        qrcode.decode('qrcode.jpg')
        return qrcode.data_to_string()

    #----------------------------------------------------------------------
    def close(self):
        """Fermeture de la classe"""
        self.camera.close()
