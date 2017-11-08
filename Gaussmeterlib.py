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
            Value2=self.init()
            if type(Value)and(type(Value2))==float:
                if (Value - Value2)<self.delta:
                    fields.append((Value+Value2)/2)
                else: print(Value, Value2)
            else: print(Value,Value2)
        field=sum(fields)/len(fields)
        return(field)
        
    
    