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
        self.ser=serial.Serial()
        self.ser.baudrate=self.Baud
        self.ser.port=self.COMPort
        self.SensDict={'2nV/fA':0,'5nV/fA':1,'10nV/fA':2,'20nV/fA':3,'50nV/fA':4,'100nV/fA':5,
        '200nV/fA':6,'500nV/fA':7,'1uV/pA':8,'2uV/pA':9,'5uV/pA':10,'10uV/pA':11,'20uV/pA':12,
        '50uV/pA':13,'100uV/pA':14,'200uV/pA':15,'500uV/pA':16,'1mV/nA':17,'2mV/nA':18,
        '5mV/nA':19,'10mV/nA':20,'20mV/nA':21,'50mV/nA':22,'100mV/nA':23,'200mV/nA':24,
        '500mV/nA':25,'1V/uA':26}
        
    def connect(self):
        try:    
            self.ser.open()
            self.ser.write('++ver\r\n'.encode('utf-8'))
            Value=self.ser.readline()
            print(Value)
            self.ser.close()
        except: 
            print('xui')
            self.ser.close()    
        
    def SendCommand(self,Command):
        try:
            self.ser.open()
            self.ser.write((Command+'\r\n').encode('utf-8'))
            self.ser.close()
        except: 
            print('xui')
            self.ser.close()
    
    def ReadLockIn(self, Command):
        try:
            self.ser.open()
            self.ser.write(Command)
            self.ser.write(('++read\r\n').encode('utf-8'))
            Value=self.ser.readline()
            return Value
        except:
            self.ser.close()
            
    def ReadValue(self,parametr):
        '''parametr is a string like in manual. except Theta'''
        OutputDict={'X':1,'Y':2,'R':3,'Theta':4,'Aux in 1':5,'Aux in 2':6,'Aux in 3':7,
                    'Aux in 4':8,'Reference Frequency':9,'CH1 display': 10,'CH2 diplay': 11}
        Command='OUTP ?' + OutputDict[parametr]
        Value=self.ReadLockIn(Command)
        print(Value)
        
    def SetToDefault(self):
        self.SendCommand('*RST')
    
    def SetSensitivity(self, sens):
        '''Sets the sensitivity on SR830 Lock in. sens is string like on the front panel'''
        command='SENS'+str(self.SensDict[sens])
        self.SendCommand(command)
    
    def GetSensetivity(self):
        self.SendCommand('SENS ?')
        