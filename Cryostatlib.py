# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 00:18:00 2017

@author: vgrigore
"""

import serial

def Cyostat(object):
    
    def __init__(self):
        self.temperuture=0
        self.COMport='COM4'
    
    def connect(self):
        ser=serial.Serial()
        ser.port=self.COMport


ser=serial.Serial()
ser.port='COM4'
ser.baudrate=115200
ser.open()
ser.write('*IDN?\n'.encode('utf-8'))
print(ser.readline())
ser.write('READ:SYS:TIME\n'.encode('utf-8'))
print(ser.readline())