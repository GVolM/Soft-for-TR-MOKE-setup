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
def Meas(avg=10, sleep=0.9, var='R'):
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
    CurrStop=10
    step=0.5
    
    for i in range(0,20):
        Currents.append(CurrStart+i*step)
    for i in range(0,21):
        Currents.append(CurrStop - i*step)  
    for item in Currents:
        Currents2.append(-item)
    for item in Currents2:
        Currents.append(item)   
    
    
    for item in Currents2:
        Filename='RuCl3-Kerr-T=4.2k=pr-0.3-pu-0.5-H-pos-'+str(item)+'-after-'+str(item-1)
        print(-item)
        Magnet.SetCurrent(-item)
        time.sleep(10)
        stepscanMeas(Filename,-110,150,500)
    Magnet.OutputOFF()
    time.sleep(1)
    Magnet.SwitchReverse()
    Magnet.OutputON()
    
    for item in Currents2:
        Filename='RuCl3-Kerr-T=4.2k=pr-0.3-pu-0.5-H-neg-'+str(item)+'-after-'+str(item+2)

        print(item)
        Magnet.SetCurrent(-item)
        time.sleep(10)
        stepscanMeas(Filename,-110,150,500)
    Magnet.OutputOFF()
#Filename='RuCl3-Kerr-T=4.3k=pr-0.2-pu-0.2-H-0AFWD-circpolafterheat'    
#stepscanMeas(Filename,-107,150,200)
MeasureHys()

