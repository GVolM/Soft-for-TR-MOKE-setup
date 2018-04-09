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
import clr 
import System
#import time

class NewPortStage(object):
    
    def __init__(self):
        self.NETAssemblyPath=r'C:\Windows\Microsoft.NET\assembly\GAC_64\Newport.XPS.CommandInterface\v4.0_1.0.0.0__9a267756cf640dcf'
        sys.path.append(self.NETAssemblyPath)
        clr.AddReference("Newport.XPS.CommandInterface")
        import CommandInterfaceXPS 
        self.myXPS=CommandInterfaceXPS.XPS()
        self.Address='192.168.254.254'
        self.Port=5001
        self.StageName="CykBlyat"
        self.ZeroPosition=0
        self.CurrentPosition=0
        
    def XPS_Open (self):
        # Create XPS interface
        # Open a socket
        timeout = 1000
        result = self.myXPS.OpenInstrument(self.Address, self.Port, timeout)
        if result == 0:
            print( 'Open ', self.Address, ":", self.Port, " => Successful")
        else:
            print ('Open ', self.Address, ":", self.Port, " => failure ", result)
        
    def Initilize(self):
        self.XPS_Open()
        self.myXPS.GroupKill(System.String(self.StageName),System.String(""))
        self.myXPS.GroupInitialize(System.String(self.StageName),System.String(""))
        self.myXPS.GroupHomeSearch(System.String(self.StageName),System.String(""))
        self.myXPS.GroupMotionEnable(System.String(self.StageName),System.String(""))
        self.MoveTo(self.ZeroPosition)
    
    def XPS_GetControllerVersion (self, myXPS, flag):
        result, version, errString = self.myXPS.FirmwareVersionGet(System.String(""),System.String(""))
        if flag == 1:
            if result == 0:
                print('XPS firmware version => ', version)
            else:
                print('FirmwareVersionGet Error => ',errString)
            return result, version
        
    def XPS_GetControllerState (self, myXPS, flag):
        result, state, errString = self.myXPS.ControllerStatusGet(System.Int32(0),System.String(""))
        if flag == 1:
            if result == 0:
                print('XPS controller state => ', state)
            else:
                print('ControllerStatusGet Error => ',errString)
        return result, state
    
    def MoveTo(self, Position):
        '''Moves stage to given position in range of +/- 150 mm '''
        self.myXPS.GroupMoveAbsolute(System.String(self.StageName),[System.Double(Position)],System.Int32(1),System.String(""))
        self.CurrentPosition=Position
        print(Position)
        
    def GetCurrentPosition(self):
        pos=self.myXPS.GetCurrentPosition(System.Double(0),System.Double(0),System.Int32(1),System.Int32(1),System.Int32(1),System.Int32(1),System.String(self.StageName))
        return pos
    
    def Close(self):
        self.myXPS.GroupKill(System.String(self.StageName),System.String(""))
    
    def Continue(self):
        self.XPS_Open()
        self.myXPS.GroupKill(System.String(self.StageName),System.String(""))
        self.myXPS.GroupInitialize(System.String(self.StageName),System.String(""))
        self.myXPS.GroupMotionEnable(System.String(self.StageName),System.String(""))
        self.MoveTo(self.CurrentPosition)
        
    def SetZeroPosition(self):
        self.ZeroPosition=self.CurrentPosition
        
#==============================================================================

    
