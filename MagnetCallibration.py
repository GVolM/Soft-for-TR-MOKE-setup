# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 10:37:26 2017

@author: vgrigore
"""

import CurrentSupplyLib
import Gaussmeterlib
import matplotlib
import time
import numpy as np
import h5py
'''script for magnet calibration. Before start set gaussmeter to ZERO manualy'''

class MagnetCallibration(object):
    
    def __init__(self):
        self.Currents=[]
        self.CurrentReal=[]
        self.Fields=[]
        
    def CreateCurrents(self, startCurr, finCurr, Points):
        self.Currents=[]
        step=(finCurr-startCurr)/Points
        curr=startCurr
        for item in range(0,Points):
            curr=startCurr+step*item
            self.Currents.append(curr)
        self.Currents.append(finCurr)
        
        
    def MeasureFields(self):
        self.Fields=[]
        self.CurrentReal=[]
        CurrentSup=CurrentSupplyLib.CurrentSUP()
        CurrentSup.initcurrentsupply()
        CurrentSup.SetVoltage(40)
        CurrentSup.SetCurrent(0)
        CurrentSup.OutputON()
        Gauss=Gaussmeterlib.Gaussmeter()
        for item in self.Currents:
            CurrentSup.SetCurrent(item)
            time.sleep(10)
            self.Fields.append(-Gauss.MeasureField(10))
            CurrentSup.GetCurrent()
            self.CurrentReal.append(CurrentSup.CurrentMeas)
        CurrentSup.OutputOFF()    
        CurrentSup.SetVoltage(0)
        CurrentSup.SetCurrent(0)
        Gauss.close()
        matplotlib.pyplot.plot(self.Currents,self.Fields)
        matplotlib.pyplot.plot(self.CurrentReal,self.Fields)
        
        
    def SaveCallibrationFile(self,name):
        File=h5py.File(name+".hdf5", "w")
        data=np.array([self.Currents,self.Fields])
        dset=File.create_dataset("fieldcal",(len(self.Currents),2))
        dset[...]=data.T
        File.close()
        
    
if __name__=='__main__':
    a=MagnetCallibration()
    a.CreateCurrents(0,10,100)
    a.MeasureFields()
    a.SaveCallibrationFile("Mgnetcalibration")
