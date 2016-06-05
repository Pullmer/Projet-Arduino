#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Jonas
  Purpose: Test unitaire décodeur QRCode
  Created: 17/02/2016
"""

import qrCodeDecoder

qrReader = qrCodeDecoder.QRDecode()
print("Message décodé : " + qrReader.decodeQRCode())

qrReader.close()
