# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:51:36 2018

@author: vgrigore
"""

import h5py
import numpy as np

File=h5py.File("testdata.hdf5", "w")
XX=np.arange(1,100)
YY=np.arange(1,100)
data=np.array([XX,YY])
dset=File.create_dataset("fieldcal",(len(XX),2))
dset[...]=data.T
File.close()