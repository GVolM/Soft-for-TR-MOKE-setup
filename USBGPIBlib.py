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
        
        self.inputConfig={'A':0,'A-B':1,'I(1mOm)':2,'I(100mOm)':3}
        
        self.inputShield={'Float':0,'Ground':1}
        
        self.inputCoupling={'AC':0,'DC':1}
        
        self.inputLineNotchFilter={'no filters':0,'Line notch':1,'2xLine notch':2,'Both notch':3}
        
        self.reserveMode={'Nigh Reserve':0, 'Normal':1,'Low Noise':2}
        
        self.synchronousFilter={'Off':0,'below 200Hz':1}
        
        self.referenceSource={'internal':0,'external':1}
        
        self.referenceTrigger={'Zero crossing':0,'Rising edge':1,'Falling edge':2}
        
        self.configuration={'Sensitivity':0,'Time constant':0,'Low pass filter slope':0,'Input configuration':0,'Input shield':0,
                            'Input coupling':0, 'Input notch filter':0, 'Reserve mode':0,'Synchronous filter':0,'Reference source':0,
                            'Frequency':1,'Reference trigger':0,'Detection harmonic':1,'Sine output amplitude':2}
        
#%% conection to Prologix USB-GPIB adapter

    def connect(self):
        '''Set up the the connection with USB to GPIB adapter, opens port, sets up adater for communication with Lokin SR830m
        After using Lockin use Disconnect function to close the port
        '''
        try:    
            self.ser.open() # opens COM port with values in this class, Opens ones so after using use disconnecnt function to close it
            self.ser.write('++ver\r\n'.encode('utf-8')) # query version of the prologix USB-GPIB adapter to test connection
            Value=self.ser.readline() # reads version
            print(Value)
            #self.ser.close()
            self.sendCommand('++eoi 1') # enable the eoi signal mode, which signals about and of the line
            self.sendCommand('++eos 2') # sets up the terminator <lf> wich will be added to every command for Lockin, this is only for GPIB connetction
        except Exception as xui: 
            print('error'+str(xui))
            self.ser.close()   
            
    def disconnect(self):
        '''Close com port
        '''
        self.ser.close()
        
    def sendCommand(self,Command):
        '''Send any command to the opened port in right format. 
        Comands which started with ++ goes to the prologix adapter, others go directly to device(Lockin)
        '''
        try:
            #self.ser.open()
            self.ser.write((Command+'\r\n').encode('utf-8'))
            #self.ser.close()
        except: 
            print('xui')
            #self.ser.close()
            
#%% Reading Lockin SR830 functions
    
    def readLockIn(self, Command):
        '''reads any information from lockin, input command should be query command for lockin, see manual.
        Returns answer from lockin as a byte
        '''
        try:
            #self.ser.open()
            self.ser.write((Command+'\r\n').encode('utf-8')) # query info from lockin. adapter reads answer automaticaly and store it
            self.ser.write(('++read eoi\r\n').encode('utf-8')) # query data stored in adapter, eoi means that readin will end as soon as special caracter will recieved. without it will read before timeout, which slow down reading
            Value=self.ser.readline() # reads answer
            #self.ser.close()
            return Value 
        except Exception as r:
            self.ser.close()
            print(r)
            
    def readValue(self,parametr):
        '''Reads measured value from lockin. Parametr is a string like in manual. 
        except Theta. Che the dictionary of parametrs for Output
        '''
        Command='OUTP ?' + str(self.OutputDict[parametr])
        Value=float(self.readLockIn(Command)) # returns value as a float 
        print(str(Value)+' V')
        return Value
        
    def readSnap(self, parametrs):
        '''Read chosen Values from Lokin simultaniously. returns dictionary of values. 
        Parametrs is a list of strings from outputDict. Sould be at least 2
        '''
        command='SNAP ? '
        for item in parametrs:
            command=command + str(self.OutputDict[item]) + ', ' # compose command string with parametrs in input
        command=command[:-2] # cut last ', ' 
        string=str(self.readLockIn(command))[2:-3] #reads answer, transform it to string, cut system characters
        values=string.split(',') # split answer to separated values
        output={}
        for idx, item in enumerate(parametrs): 
            output[item]=float(values[idx]) # compose dictionary of values(float)
        print(output)
        return output
        
#%% Set parametrs functions
        
    def setToDefault(self):
        '''Reset lockin
        '''
        self.sendCommand('*RST')
    
    def setSensitivity(self, sens):
        '''Sets the sensitivity on SR830 Lock in. sens is string like on the front panel, mk=u
        '''
        if type(sens)==str:
            command='SENS'+str(self.SensDict[sens])
        else:
            command='SENS'+str(sens)
        self.sendCommand(command)
        self.getSensitivity()
        
        
    def setTimeConstant(self, timeConst):
        '''Sets the Time Constant on SR830 Lock in. sens is string like on the front panel, mk=u
        '''
        if type(timeConst)==str:
            command='OFLT'+str(self.TimeConstDict[timeConst])
        else:
            command='OFLT'+str(timeConst)
        self.sendCommand(command)
        self.getTimeConstant()
    
    def setLowPassFilterSlope(self, LPFilt):
        '''Sets the low pass filter slope on SR830 Lock in. sens is string like on the front panel
        '''
        if type(LPFilt)==str:    
            command='OFSL'+str(self.LowPassFilterSlopeDict[LPFilt])
        else:
            command='OFSL'+str(LPFilt)
        self.sendCommand(command)
        self.getLowPassFilterSlope()
        
    def setInputConfig(self, config):
        if type(config)==str:    
            command='ISRC'+str(self.inputConfig[config])
        else:
            command='ISRC'+str(config)
        self.sendCommand(command)
        self.getInputConfig()
    
    def setInputShield(self, shield):
        if type(shield)==str:    
            command='IGND'+str(self.inputShield[shield])
        else:
            command='IGND'+str(shield)
        self.sendCommand(command)
        self.getInputShield()
        
    def setInputCoupling(self, coupling):
        if type(coupling)==str:    
            command='ICPL'+str(self.inputConfig[coupling])
        else:
            command='ICPL'+str(coupling)
        self.sendCommand(command)
        self.getInputCoupling()
    
    def setInputNotchFilter(self, notchFilter):
        if type(notchFilter)==str:
            command='ILIN'+str(self.inputLineNotchFilter[notchFilter])
        else:
            command='ILIN'+str(notchFilter)
        self.sendCommand(command)
        self.getInputNotchFilter()
        
    def setReserveMode(self, mode):
        if type(mode)==str:
            command='RMOD'+str(self.reserveMode[mode])
        else:
            command='RMOD'+str(mode)
        self.sendCommand(command)
        self.getReserveMode()
    
    def setSynchronousFilter(self, synchronousFilter):
        if type(synchronousFilter)==str:    
            command='SYNC'+str(self.reserveMode[synchronousFilter])
        else:
            command='SYNC'+str(synchronousFilter)
        self.sendCommand(command)
        self.getSynchronousFilter()
        
    def setPhase(self, phase):
        command='PHAS'+str(phase)
        self.sendCommand(command)
        self.getPhase()
    
    def setReferenceSource(self, source):
        if type(source)==str:    
            command='FMOD'+str(self.referenceSource[source])
        else:
            command='FMOD'+str(source)
        self.sendCommand(command)
        self.getReferenceSource()
    
    def setFrequency(self, freq):
        command='FREQ'+str(freq)
        self.sendCommand(command)
        self.getFrequency()
    
    def setReferenceTrigger(self, refTrigger):
        if type(refTrigger)==str:    
            command='RSPL'+str(self.referenceTrigger[refTrigger])
        else:
            command='RSPL'+str(refTrigger)
        self.sendCommand(command)
        self.getReferenceTrigger()
        
    def setHarmonic(self,harm):
        '''sets detection harmonic, harm is integer drom 1 to 19999
        '''
        command='HARM'+str(harm)
        self.sendCommand(command)
        self.getHarmonic()
   
    def setSineOutputAmplitude(self,ampl):
        '''setsthe amplitude of the sine output. Value of ampl is a voltage in Volts 0.004<=ampl<=5
        '''
        command='SLVL'+str(ampl)
        self.sendCommand(command)
        self.getSineOutputAmplitude()
        
#%% Get parametrs function
    
    def getSensitivity(self):
        self.configuration['Sensitivity']=int(self.readLockIn('SENS ?'))
        
    def getTimeConstant(self):
        self.configuration['Time constant']=int(self.readLockIn('OFLT ?'))
        
    def getLowPassFilterSlope(self):
        self.configuration['Low pass filter slope']=int(self.readLockIn('OFSL ?'))
        
    def getInputConfig(self):
        self.configuration['Input configuration']=int(self.readLockIn('ISRC ?'))
        
    def getInputShield(self):
        self.configuration['Input shield']=int(self.readLockIn('IGND ?'))
        
    def getInputCoupling(self):
        self.configuration['Input coupling']=int(self.readLockIn('ICPL ?'))
        
    def getInputNotchFilter(self):
        self.configuration['Input notch filter']=int(self.readLockIn('ILIN ?'))
        
    def getReserveMode(self):
        self.configuration['Reserve mode']=int(self.readLockIn('RMOD ?'))
        
    def getSynchronousFilter(self):
        self.configuration['Synchronous filter']=int(self.readLockIn('SYNC ?'))
        
    def getReferenceSource(self):
        self.configuration['Reference Source']=int(self.readLockIn('FMOD ?'))
        
    def getPhase(self):
        self.configuration['Phase']=float(self.readLockIn('PHAS ?'))
        
    def getFrequency(self):
        self.configuration['Frequency']=float(self.readLockIn('FREQ ?'))
    
    def getReferenceTrigger(self):
        self.configuration['Reference trigger']=int(self.readLockIn('RSLP ?'))
    
    def getHarmonic(self):
        self.configuration['Detection harmonic']=int(self.readLockIn('HARM ?'))
    
    def getSineOutputAmplitude(self):
        self.configuration['Sine output amplitude']=float(self.readLockIn('SLVL ?'))
        
#%% Configuration of lockin functions
        
    def getConfiguration(self):
        self.getInputConfig()
        self.getInputCoupling()
        self.getInputNotchFilter()
        self.getInputShield()
        self.getSynchronousFilter()
        self.getLowPassFilterSlope()
        self.getReserveMode()
        self.getSensitivity()
        self.getTimeConstant()
        self.getFrequency()
        self.getHarmonic()
        self.getPhase()
        self.getReferenceSource()
        self.getReferenceTrigger()
        self.getSineOutputAmplitude()
    
    def setConfiguration(self):
        self.setInputConfig(self.configuration['Input configuration'])
        self.setInputCoupling(self.configuration['Input coupling'])
        self.setInputNotchFilter(self.configuration['Input notch filter'])
        self.setInputShield(self.configuration['Input shield'])
        self.setSynchronousFilter(self.configuration['Synchronous filter'])
        self.setLowPassFilterSlope(self.configuration['Low pass filter slope'])
        self.setReserveMode(self.configuration['Reserve mode'])
        self.setSensitivity(self.configuration['Sensitivity'])
        self.setTimeConstant(self.configuration['Time constant'])
        self.setFrequency(self.configuration['Frequency'])
        self.setHarmonic(self.configuration['Detection harmonic'])
        self.setPhase(self.configuration['Phase'])
        self.setReferenceSource(self.configuration['Reference source'])
        self.setReferenceTrigger(self.configuration['Reference trigger'])
        self.setSineOutputAmplitude(self.configuration['Sine output amplitude'])
        
    def saveConfiguration(self):
        pass
    
    def laodConfiguration(self):
        pass
    
#%%



if __name__ == '__main__':
    a=USBGPIB()
    a.connect()    #a.ser.write((Command+'\r\n').encode('utf-8'))
    #a.ser.write(('++read\r\n').encode('utf-8'))
    time0=time.clock()
    for i in range(0,10):
        a.readValue('X')
        
    time1=time.clock()
    print(time1-time0)
    a.disconnect()