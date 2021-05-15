# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd

data1= loadmat('1F_GNG_explorative_noTrialManager_2_20210128_090558.mat', simplify_cells=True)
data2= loadmat('1F_GNG_explorative_noTrialManager_2_20210128_093339.mat', simplify_cells=True)
data_dict= dict()


session_data1= data1['SessionData']
session_data2= data2['SessionData']

data_dict['TrialTypes']= np.append(session_data1['TrialTypes'], session_data2['TrialTypes'])
data_dict['nTrials']= session_data1['nTrials']+session_data2['nTrials']

list1= session_data1['RawEvents']['Trial']
list2= session_data2['RawEvents']['Trial']
for i in range(len(list2)):
    list1.append(list2[i])
data_dict['RawEvents']= list1

import pickle
with open('data_dict', 'wb') as save_dict:
    pickle.dump(data_dict, save_dict)


# trials_data[i]['States']['Reward'][0]
