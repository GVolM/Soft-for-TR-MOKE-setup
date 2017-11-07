# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:50:27 2017

@author: vgrigore
"""

import serial
ser=serial.Serial()
ser.baudrate=115200
ser.port='COM4'
ser.open()
ser.write('A007SYST:REM;'.encode('utf-8'))
ser.close()