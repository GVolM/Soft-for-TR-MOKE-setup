# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 14:50:27 2017

@author: vgrigore
"""

import serial

class CurrentSUP(object):
    '''CLass with basic methods for current supply'''
    def __init__(self):
        self.COMport='COM4'     #'''Com port wich current suply is connected to'''
        self.RSaddress='A007'    # '''address of RS-485 port(have no idea where to get it)'''
        self.Current=0 
        self.Voltage=0
        
    def writestring(self, SCPICommands):
        String=''
        for item in SCPICommands:
            String=String+self.RSaddress + item + ';'
        return String.encode('utf-8')
        
    def writeSCPICommand(self, SCPICommand):
        ser=serial.Serial()
        ser.baudrate=115200
        ser.port=self.COMport
        ser.open()
        ser.write(self.writestring(SCPICommand))
        ser.close()
        
    def initcurrentsupply(self):
        SCPICommands=['SYST:REM', 'SOUR:VOLT 40.0', 'SOUR:CURR 10.0', 'OUTP 1','SOUR:VOLT 0.0', 'SOUR:CURR 0.0', 'OUTP 0']
        #print(self.writestring(SCPICommands))
        self.writeSCPICommand(SCPICommands)
    
    def SetCurrent(self, Current):
        self.Current=Current
        SCPICommands=['SYST:REM', 'SOUR:CURR '+str(self.Current)]
        self.writeSCPICommand(SCPICommands)
        
    def SetVoltage(self, Voltage):
        self.Voltage=Voltage
        SCPICommands=['SYST:REM', 'SOUR:VOLT '+str(self.Voltage)]
        self.writeSCPICommand(SCPICommands)
    
    def OutputON(self):
        SCPICommands=['SYST:REM', 'OUTP 1']
        self.writeSCPICommand(SCPICommands)
        print( 'Current are put on magnet!!!')
    
    def OutputOFF(self):
        SCPICommands=['SYST:REM', 'OUTP 0']
        self.writeSCPICommand(SCPICommands)
        print('Output OFF')
        
    def ToLocalMode(self):
        SCPICommands=['SYST:REM','SOUR:VOLT 0.0', 'SOUR:CURR 0.0', 'OUTP 0', 'SYST:LOC']
        self.writeSCPICommand(SCPICommands)
        
    def ReadOut(self):
        ser=serial.Serial()
        ser.baudrate=115200
        ser.port=self.COMport
        ser.open()
        Value=ser.read()
        ser.close()
        return Value
        
    def GetCurrent(self):
        SCPICommands=['SOUR:VOLT?']
        self.writeSCPICommand(SCPICommands)
        self.Current= self.ReadOut()
        
        