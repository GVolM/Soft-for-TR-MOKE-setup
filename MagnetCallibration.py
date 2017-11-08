# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:37:26 2017

@author: vgrigore
"""

import CurrentSupplyLib
import Gaussmeterlib
import matplotlib



class MagnetCallibration(object):
    
    def __init__(self):
        self.Currents=[]
        self.Fields=[]
        
    def CreateCurrents(self, startCurr, finCurr, Points):
        step=(finCurr-startCurr)/Points
        curr=startCurr
        for item in range(0,Points):
            curr=startCurr+step*item
            self.Currents.append(curr)
        self.Currents.append(finCurr)
        
    def MeasureFields(self):
        self.Fields=[]
        CurrentSup=CurrentSupplyLib.CurrentSUP()
        CurrentSup.initcurrentsupply()
        CurrentSup.SetVoltage(40)
        CurrentSup.SetCurrent(0)
        CurrentSup.OutputON()
        Gauss=Gaussmeterlib.Gaussmeter()
        for item in self.Currents:
            CurrentSup.SetCurrent(item)
            self.Fields.append(Gauss.MeasureField(10))
        CurrentSup.OutputOFF()    
        CurrentSup.SetVoltage(0)
        CurrentSup.SetCurrent(0)
        matplotlib.pyplot.plot(self.Currents,self.Fields)
        
