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
        
        self.OutputDict={'X':1,'Y':2,'R':3,'Theta':4,'Aux in 1':5,'Aux in 2':6,'Aux in 3':7,
                    'Aux in 4':8,'Reference Frequency':9,'CH1 display': 10,'CH2 diplay': 11}
        
        self.TimeConstDict={'10us':0,'30us':1,'100us':2,'300us':3,'1ms':4,'3ms':5,
                            '10ms':6,'30ms':7,'100ms':8,'300ms':9,'1s':10,'3s':11,
                            '10s':12,'30s':13,'100s':14,'300s':15,'1ks':16,'3ks':17,
                            '10ks':18,'30ks':19}
        
        self.LowPassFilterSlopeDict={'6 dB':0, '12 dB':1, '18 dB':2, '24 dB':3}
        
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
            self.ser.write((Command+'\r\n').encode('utf-8'))
            self.ser.write(('++read\r\n').encode('utf-8'))
            Value=self.ser.readline()
            self.ser.close()
            return float(Value)
        except:
            self.ser.close()
            print('error')
            
    def ReadValue(self,parametr):
        '''parametr is a string like in manual. except Theta'''
        Command='OUTP ?' + str(self.OutputDict[parametr])
        Value=self.ReadLockIn(Command)
        print(str(Value)+' V')
        return Value
        
    def SetToDefault(self):
        self.SendCommand('*RST')
    
    def SetSensitivity(self, sens):
        '''Sets the sensitivity on SR830 Lock in. sens is string like on the front panel, mk=u'''
        command='SENS'+str(self.SensDict[sens])
        self.SendCommand(command)
        
    def SetTimeConstant(self, TimeConst):
        '''Sets the Time Constant on SR830 Lock in. sens is string like on the front panel, mk=u'''
        command='OFLT'+str(self.TimeConstDict[TimeConst])
        self.SendCommand(command)
    
    def SetLowPassFilterSlope(self, LPFilt):
        '''Sets the low pass filter slope on SR830 Lock in. sens is string like on the front panel'''
        command='OFSL'+str(self.LowPassFilterSlopeDict[LPFilt])
        self.SendCommand(command)
    
    
    def GetSensetivity(self):
        self.SendCommand('SENS ?')

if __name__ == '__main__':
       
    a=USBGPIB()
    a.connect()
    time0=time.clock()
    for i in range(0,10):
        a.ReadValue('X')
    
    time1=time.clock()
    print(time1-time0)