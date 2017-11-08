# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:37:26 2017

@author: vgrigore
"""

import CurrentSupplylib
import Gaussmeterlib

class MagnetCallibration(object):
    
    def __init__(self):
        self.Currents=[]
        self.Fields=[]
        
    def CreateCurrents(self, startCurr, finCurr, Points):
        step=(finCurr-startCurr)/Points
        curr=startCurr
        self.Currents.append(curr)
        for item in Points:
            curr=curr+step*item
            self.Currents.append(curr)
        
    def MeasureFields(self):
        CurrentSup=CurrentSupplylib.CurrentSUP()
        CurrentSup.initcurrentsupply()
        CurrentSup.SetVoltage(40)
        Gauss=Gaussmeterlib.Gaussmeter()
        for item in self.Currents:
            CurrentSup.SetCurrent(item)
            CurrentSup.OutputON()
            self.Fields.append(Gauss.MeasureField(10))
            
        
        
        
