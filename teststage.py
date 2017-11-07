# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:58:15 2017

@author: vgrigore
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May  9 14:06:55 2017

@author: vgrigore
"""

import sys
sys.path.append(r'C:\Windows\Microsoft.NET\assembly\GAC_64\Newport.XPS.CommandInterface\v4.0_1.0.0.0__9a267756cf640dcf')
import clr
clr.AddReference("Newport.XPS.CommandInterface") 
import CommandInterfaceXPS  
myXPS=CommandInterfaceXPS.XPS()
import System
import time
#Cimport numpy as np
def XPS_Open (address, port):
    # Create XPS interface
    myXPS = CommandInterfaceXPS.XPS()
    # Open a socket
    timeout = 1000
    result = myXPS.OpenInstrument(address, port, timeout)
    if result == 0:
        print( 'Open ', address, ":", port, " => Successful")
    else:
        print ('Open ', address, ":", port, " => failure ", result)
    return myXPS
    
def XPS_GetControllerVersion (myXPS, flag):
    result, version, errString = myXPS.FirmwareVersionGet(System.String(""),System.String(""))
    if flag == 1:
        if result == 0:
            print('XPS firmware version => ', version)
        else:
            print('FirmwareVersionGet Error => ',errString)
    return result, version
def XPS_GetControllerState (myXPS, flag):
    result, state, errString = myXPS.ControllerStatusGet(System.Int32(0),System.String(""))
    if flag == 1:
        if result == 0:
            print('XPS controller state => ', state)
        else:
            print('ControllerStatusGet Error => ',errString)
    return result, state
    
Stage=XPS_Open('192.168.254.254',5001)
Stage.GroupKill(System.String("CykBlyat"),System.String(""))
Stage.GroupInitialize(System.String("CykBlyat"),System.String(""))
Stage.GroupHomeSearch(System.String("CykBlyat"),System.String(""))
Stage.GroupMotionEnable(System.String("CykBlyat"),System.String(""))
print("asda!")
#Stage.GroupJogParametersSet(System.String("CykBlyat"),[System.Double(50)],[System.Double(100)],System.Int32(1),System.String(""))
#time.sleep(1)
#Stage.GroupJogParametersSet(System.String("CykBlyat"),[System.Double(0)],[System.Double(100)],System.Int32(1),System.String(""))
#==============================================================================
Stage.GroupMoveAbsolute(System.String("CykBlyat"),[System.Double(-150)],System.Int32(1),System.String(""))

Stage.GroupMoveAbsolute(System.String("CykBlyat"),[System.Double(150)],System.Int32(1),System.String(""))
Stage.GroupMoveAbsolute(System.String("CykBlyat"),[System.Double(-100)],System.Int32(1),System.String(""))
Stage.GroupMoveAbsolute(System.String("CykBlyat"),[System.Double(-100)],System.Int32(1),System.String(""))
Stage.GroupMoveAbsolute(System.String("CykBlyat"),[System.Double(-100)],System.Int32(1),System.String(""))



#==============================================================================

def moveto(pos):
    Stage.GroupMoveAbsolute(System.String("CykBlyat"),[System.Double(pos)],System.Int32(1),System.String(""))
