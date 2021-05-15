# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:47:10 2021

@author: ricca
"""

# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import matplotlib
import glob
import os
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
matplotlib.use('qt5agg')


# List of dirs
# index        0       1       2      3       4       5      6      7     8       9
mouse_list= ['PV92','PV94','PV100','PV104','PV107','WT58','WT96','WT97','WT98','WT101']
mouse_name = mouse_list[9]  # CHANGE THIS
day = '-1'                   # AND THIS
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\habituation'
mouse_dir = general_dir + '\\' + mouse_name


# Load data
os.chdir(mouse_dir)
data = []
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))

trial_types = data[int(day)]['SessionData']['TrialTypes']
# a list with every trial
trials_data = data[int(day)]['SessionData']['RawEvents']['Trial']
nTrials= len(trial_types)

csMinus = []
csPlus = []
csPlus_idx = np.array(np.where(trial_types == 2))
csPlus_idx = csPlus_idx.reshape(csPlus_idx.shape[1])
csMinus_idx = np.array(np.where(trial_types == 1))
csMinus_idx = csMinus_idx.reshape(csMinus_idx.shape[1])


for TrialType in range(1, 4):
    licksXtrial = []
    idxTrialType = np.array(np.where(trial_types == TrialType))
    for Trial in range(0, idxTrialType.size):
        # if there was a PortIn
        if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:
            # centered on valve opening
            licks_ts = np.array(
                trials_data[idxTrialType[0][Trial]]['Events']['Port1In'])
            if licks_ts.shape == ():
                licks_ts = licks_ts.reshape(1)
            if TrialType == 1:    # valve click no odor
                #licks_ts= licks_ts -
                csMinus.append(licks_ts)
            elif TrialType == 2:  # reward
                csPlus.append(licks_ts)
fig, ax = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
fig.suptitle(mouse_name)
ax[0].eventplot(csMinus, colors='black')  # lineoffsets= csMinus_idx)
ax[1].eventplot(csPlus, colors='black')
ax[0].set_title('No odor')
ax[1].set_title('Reward')
for i in range(0, 2):
    ax[i].set_ylim([0,nTrials/2])
    ax[i].axvline(color='blue', x=2)
    ax[i].set_xlabel('Time (s)')
    ax[i].set_ylabel('Trials')
    ax[i].add_patch(Rectangle((2,0), 
                              width= 2, height= abs(ax[i].get_ylim()[1]),
                              alpha=0.5))
