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

Lockin=USBGPIBlib.USBGPIB()
Lockin.connect()
Stage=NewPortStagelib.NewPortStage()
Stage.Initilize()


def CreatePoints(start, stop, N):
    Points=[]
    step=(stop-start)/N
    Points.append(start)
    for i in range(0,N):
        Points.append(start+i*step)
    return Points
def Meas(avg=10, sleep=0.2, var='R'):
    signal=[]
    time.sleep(sleep)
    for i in range(avg):
        signal.append(Lockin.readValue(var))
    val=sum(signal)/avg
    return val     

def stepscanMeas(start, stop, N):
    X=CreatePoints(start,stop,N)
    Y=[]
    for item in X:
        Stage.MoveTo(item)
        time.sleep(0.2)
        Y.append(Meas())
    matplotlib.pyplot.plot(X,Y)
    return X,Y
    
stepscanMeas(-54.5,-52,100)
 

