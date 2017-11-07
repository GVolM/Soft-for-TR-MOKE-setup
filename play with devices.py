# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:14:30 2017

@author: vgrigore
"""

import visa

rm = visa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource('ASRL3::INSTR')
print(inst.query("*IDN?"))