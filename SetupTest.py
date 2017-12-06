# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:51:16 2017

@author: vgrigore
"""

import CurrentSupplyLib
import USBGPIBlib
import time
import matplotlib 

Lockin=USBGPIBlib.USBGPIB()
Lockin.connect()
Magnet=CurrentSupplyLib.CurrentSUP()
Magnet.initcurrentsupply()
Magnet.SetVoltage(40)
Magnet.SetCurrent(0)
Magnet.SwitchForward()


def MeasureHys():
    time.sleep(1)
    Magnet.SwitchForward()
    Magnet.OutputON()
    Currents=[]
    Currents2=[]
    CurrStart=0
    CurrStop=5
    step=0.1
    Signal=[]
    for i in range(0,50):
        Currents.append(CurrStart+i*step)
    for i in range(0,51):
        Currents.append(CurrStop - i*step)  
    for item in Currents:
        Currents2.append(-item)
    for item in Currents2:
        Currents.append(item)   
    
    
    for item in Currents2:
        print(-item)
        Magnet.SetCurrent(-item)
        time.sleep(1)
        Signal.append(Meas())
    Magnet.OutputOFF()
    time.sleep(1)
    Magnet.SwitchReverse()
    Magnet.OutputON()
    
    for item in Currents2:
        print(item)
        Magnet.SetCurrent(-item)
        time.sleep(1)
        Signal.append(Meas())
    Magnet.OutputOFF()
    matplotlib.pyplot.plot(Currents, Signal)
        
def Meas():
    signal=[]
    avg=2
    for i in range(avg):
        signal.append(Lockin.ReadValue('X'))
    print(signal)
    val=sum(signal)/avg
    return val   
    
MeasureHys()
 
#Magnet.SetCurrent(5)
#Magnet.SwitchForward()
#Magnet.OutputON()
#time.sleep(10)
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Magnet.OutputOFF()
#Magnet.SwitchReverse()
#Magnet.OutputON()
#time.sleep(10)
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Lockin.ReadValue('R')
#Magnet.initcurrentsupply()
#Magnet.ToLocalMode()