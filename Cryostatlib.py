# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 00:18:00 2017

@author: vgrigore
"""

import serial
import time
class Cryostat(object):
    
    def __init__(self):
        self.temperuture=0              
        self.COMPort='COM8'
        self.Baud=115200
        self.ser=serial.Serial()
        self.ser.baudrate=self.Baud
        self.ser.port=self.COMPort
        self.device='MB1.T1'
#%%    
    def connect(self):
        '''Set up the the connection with USB to GPIB adapter, opens port, sets up adater for communication with Lokin SR830m
        After using Lockin use Disconnect function to close the port
        '''
        try:    
            self.ser.open() # opens COM port with values in this class, Opens ones so after using use disconnecnt function to close it
            self.ser.write(b'*IDN?\r\n') # query version of the temperature controller
            
            Value=self.ser.readline() # reads version
            print(Value)
            
            
        except Exception as xui: 
            print('error'+str(xui))
            self.ser.close()   
            
    def disconnect(self):
        '''Close com port
        '''
        self.ser.close()
        
    def send_command(self,Command):
        '''Send any command to the opened port in right format. 
       
        '''
        try:
            #self.ser.open()
            self.ser.write((Command+'\r\n').encode('utf-8'))# xxx.encode() does the same as b'xxx'
            #self.ser.close()
        except: 
            print('xui')
            #self.ser.close()
            
    def read(self, Command):
        '''reads any information from tempereture controller, input command should be query command for tempereture controller, see manual.
        Returns answer from lockin as a byte
        '''
        try:
            #self.ser.open()
            self.send_command(Command) # query info from device.
            
            Value=self.ser.readline() # reads answer
            #self.ser.close()
            return Value 
        except Exception as r:
            self.ser.close()
            print(r)
            
    def writestring(self, SCPICommands):
        '''Transform list of SCPI commands to strig for writing to USB. Adds seporator, transform it to required format. SCPICommands should be list of strings'''
        String=''
        for item in SCPICommands:
            String=String+item + ':'
        String=String[:-1] +'\r\n'
        return String.encode('utf-8')

#%% 
    def test(self):
        print('hjijk')
        
    def set_temperature(self, temperature):
        '''Sets temperature on the device, temperature should be givet in kelvin.'''
        try:
            command=['SET','DEV','MB1.T1','TEMP','LOOP','TSET',str(temperature)]
            self.ser.write(self.writestring(command))
            responce=str(self.ser.readline())
            print(responce)
            if response.split(sep=':')[-1]='VALID':
                
            
        except Exception as xui: 
            print('error'+str(xui))
            self.ser.close
    
    def get_temperature(self, Units='TEMP'):
        
        try:
            command=['READ','DEV','MB1.T1','TEMP','SIG',Units]
            self.ser.write(self.writestring(command))
            response=self.ser.readline()
            
            print(response)
            temperature1=str(response).split(sep=':')[6]
            temperature=float(temperature1[:-5])
            return(temperature)
        except Exception as xui: 
            print('error'+str(xui))
            self.ser.close
#%%
if __name__=='__main__':
    cryo=Cryostat()
    cryo.connect()
    time.sleep(0.3)
    T=cryo.get_temperature()
    time.sleep(1)
    cryo.set_temperature(T+10)
    time.sleep(10)
    cryo.set_temperature(T)
    cryo.disconnect()
    print('good night')