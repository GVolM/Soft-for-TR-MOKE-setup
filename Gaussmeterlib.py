# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 18:39:44 2017

@author: vgrigore
"""

import serial
import time
import numpy

class Gaussmeter(object):
    def __init__(self):
        self.COMport='COM5'
        
        
        
    def init(self):
        ser=serial.Serial()
        ser.baudrate=9600
        ser.port=self.COMport
        time.sleep(0.1)
        try:
            ser.open()
            string=ser.read(16)
            sign=(-1)**(int(string[5:6]))
            Value=sign*float(string[7:-1])/10   
            ser.close()
            print(int(string[5:6]))
            print('H=', Value, ' mT')
        except: 
            ser.close()
            Value='xui'
        time.sleep(0.1)
        return(Value)
    
    def MeasureField(self,Avg):
        fields=[]
        while len(fields)<Avg:
            Value=self.init()
            if type(Value)==float:
                fields.append(Value)
            else: print(Value)
        field=sum(fields)/len(fields)
        return(field)
        
    
    