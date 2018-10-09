# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 19:53:18 2018

@author: vgrigore
"""

'Stepscantest'
import NewPortStagelib
import USBGPIBlib
import time
import matplotlib
import h5py
import numpy as np
import CurrentSupplyLib

Lockin=USBGPIBlib.USBGPIB()
Lockin.connect()
Stage=NewPortStagelib.NewPortStage()
Magnet=CurrentSupplyLib.CurrentSUP()
Magnet.initcurrentsupply()
#Magnet.SetVoltage(40)
#Magnet.SetCurrent(0)
#Magnet.SwitchForward()
Stage.Initilize()
time.sleep(5)
Stage.MoveTo(-115)
time.sleep(3)


def CreatePoints(start, stop, N):
    Points=[]
    step=(stop-start)/N
    Points.append(start)
    for i in range(0,N):
        Points.append(start+i*step)
    return Points
    
def Meas(avg=10, sleep=1, var='R'):
    signal=[]
    time.sleep(sleep)
    for i in range(avg):
        signal.append(Lockin.readValue(var))
    val=sum(signal)/avg
    return val     

def Save(name,X,Y):
    File=h5py.File(name+".hdf5", "w")
    data=np.array([X,Y])
    dset=File.create_dataset("stepscan",(len(X),2))
    dset[...]=data.T
    File.close()

def stepscanMeas(name, start, stop, N):
    Stage.MoveTo(-115)
    time.sleep(3)

    X=CreatePoints(start,stop,N)
    Y=[]
    for item in X:
        Stage.MoveTo(item)
        #time.sleep(0.0)
        Y.append(Meas())
    matplotlib.pyplot.plot(X,Y)
    Save(name+str(start)+'-'+str(stop)+'-'+str(N),X,Y)
    return X,Y

def MeasureHys():
    time.sleep(1)
    Magnet.SwitchForward()
    Magnet.SetVoltage(40)
    Magnet.SetCurrent(0)

    Magnet.OutputON()
    Currents=[]
    Currents2=[]
    CurrStart=0
    CurrStop=7
    step=1
    
    for i in range(0,7):
        Currents.append(CurrStart+i*step)
    for i in range(0,8):
        Currents.append(CurrStop - i*step)  
    for item in Currents:
        Currents2.append(-item)
    for item in Currents2:
        Currents.append(item)   
    
    
    for idx, item in enumerate(Currents2):
        Filename='20.05.2018-RuCl3-Refl-T=4.2k=pr-0.2-pu-0.15-H-pos-'+str(-item)+'-idx-'+str(idx)
        print(-item)
        Magnet.SetCurrent(-item)
        time.sleep(10)
        stepscanMeas(Filename,-110,150,250)
    Magnet.OutputOFF()
    time.sleep(1)
    Magnet.SwitchReverse()
    Magnet.OutputON()
    
    for idx, item in enumerate(Currents2):
        Filename='20.05.2018-RuCl3-Refl-T=4.2k=pr-0.2-pu-0.15-H-neg-'+str(item)+'-idx-'+str(idx)

        print(item)
        Magnet.SetCurrent(-item)
        time.sleep(10)
        stepscanMeas(Filename,-110,150,250)
    Magnet.OutputOFF()
Filename='CCF-NEWgratings_realigned'    
stepscanMeas(Filename,-93.3,-93.6,420)
#MeasureHys()
Lockin.disconnect()
Stage.Close()