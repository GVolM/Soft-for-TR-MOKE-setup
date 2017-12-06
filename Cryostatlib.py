# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 00:18:00 2017

@author: vgrigore
"""

import serial
class Cryostat(object):
    
    def __init__(self):
        self.temperuture=0              
        self.ser=serial.Serial()
        self.ser.port='COM1'
        self.ser.baudrate=9600
        
    def writestring(self, SCPICommands):
        '''Transform list of SCPI commands to strig for writing to RS-485 port. Adds address of port and seporator, transform it to required format. SCPICommands should be list of strings'''
        String=''
        for item in SCPICommands:
            String=String+item + ':'
        String=String - ':'+'\n'
        return String.encode('utf-8')
    
    def SendCommand(self, Command):
        self.ser.open()
        self.ser.write((Command).encode('utf-8'))
        self.ser.close()
    
    def connect(self):
        try:
            self.ser.open()
            self.ser.write(self.writestring('*IDN?'))
            print(self.ser.readline())
            commands=['READ','SYS','TIME']
            self.ser.write(self.writestring(commands))
            print(self.ser.readline())
            self.ser.close()
        except: 
            self.ser.close()
            
    def SetTemperature(self, temperature):
        try:
            self.ser.open()
            command=['SET','DEV','MB1.T1','TEMP','TSET',str(temperature)]
            self.ser.write(self.writesttring(command))
            self.ser.close()
        except:
            self.close
