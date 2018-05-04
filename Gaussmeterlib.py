# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 18:39:44 2017

@author: vgrigore
"""

import serial
import time


class Gaussmeter(object):
    def __init__(self):
        self.COMport='COM5'
        self.delta=10 # error parametr in mT
        self.ser=serial.Serial()
        self.ser.baudrate=9600
        self.ser.port=self.COMport
        #self.ser.open()
        
    def Meas(self):   
        time.sleep(0.1)
        self.ser.open()
        try:
            string=self.ser.read(16)
            sign=(-1)**(int(string[5:6]))
            Value=sign*float(string[7:-1])/10   
            print(int(string[5:6]))
            print('H=', Value, ' mT')
        except: 
            Value=0
        time.sleep(0.1)
        self.ser.close()
        return(Value)
        
    
    def close(self):
        self.ser.close()
        
    def MeasureField(self,Avg):
        fields=[]
        for i in range(Avg+2):
            fields.append(self.Meas())
        field=sum(fields[2:])/len(fields[2:])
        return(field)
        
    
    