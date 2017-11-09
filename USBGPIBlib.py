# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 14:52:50 2017

@author: vgrigore
"""

import serial
import time

class USBGPIB(object):
    
    def __init__(self):
        self.COMPort='COM6'
        self.Baud=115200
        self.deviceAddr=8
        
    def connect(self):
        ser=serial.Serial()
        ser.baudrate=self.Baud
        ser.port=self.COMPort
        try:    
            ser.open()
            ser.write('++ver\r\n'.encode('utf-8'))
            Value=ser.readline()
            print(Value)
            ser.close()
        except: 
            print('xui')
            ser.close()    
        
    def SendCommand(self,Command):
        ser=serial.Serial()
        ser.baudrate=self.Baud
        ser.port=self.COMPort
        try:
            ser.open()
            ser.write((Command+'\r\n').encode('utf-8'))
            ser.close()
        except: 
            print('xui')
            ser.close()
            
    def ReadValue(self,parametr=1):
        ser=serial.Serial()
        ser.baudrate=self.Baud
        ser.port=self.COMPort
        try:    
            ser.open()
            ser.write(('OUTP ? '+str(parametr)+'\r\n').encode('utf-8'))
          # time.sleep(0.1)
            ser.write(('++read\r\n').encode('utf-8'))
           # time.sleep(0.1)
            Value=ser.readline()
            print(Value)
            ser.close()
        except: 
            print('xui')
            ser.close() 