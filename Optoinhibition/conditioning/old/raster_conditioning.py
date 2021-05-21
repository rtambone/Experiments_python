# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:09:48 2021

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
mouse_name = 'WT97'  # CHANGE THIS
day = '0'            # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\conditioning'
mouse_dir = general_dir + '\\' + mouse_name


# Load data
os.chdir(mouse_dir)
data = []
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))

trial_types = data[int(day)]['SessionData']['TrialTypes']
# a list with every trial
trials_data = data[int(day)]['SessionData']['RawEvents']['Trial']

csMinus = []
csPlus = []
csPlusN = []
csPlus_idx = np.array(np.where(trial_types == 2))
csPlus_idx = csPlus_idx.reshape(csPlus_idx.shape[1])
csMinus_idx = np.array(np.where(trial_types == 1))
csMinus_idx = csMinus_idx.reshape(csMinus_idx.shape[1])
csPlusN_idx = np.array(np.where(trial_types == 3))
csPlusN_idx = csPlusN_idx.reshape(csPlusN_idx.shape[1])


for TrialType in range(1, 4):
    licksXtrial = []
    idxTrialType = np.array(np.where(trial_types == TrialType))
    for Trial in range(0, idxTrialType.size):
        # if there was a PortIn
        if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:
            # centered on valve opening
            licks_ts = np.array(
                trials_data[idxTrialType[0][Trial]]['Events']['Port1In'] - 5)
            if licks_ts.shape == ():
                licks_ts = licks_ts.reshape(1)
            if TrialType == 1:    # valve click no odor
                csMinus.append(licks_ts)
            elif TrialType == 2:
                csPlus.append(licks_ts)
            elif TrialType == 3:
                csPlusN.append(licks_ts)
fig, ax = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
fig.suptitle(mouse_name)
ax[0].eventplot(csMinus, colors='black')  # lineoffsets= csMinus_idx)
ax[1].eventplot(csPlus, colors='black')
ax[1].eventplot(csPlusN, colors='red')
ax[0].set_title('No odor')
ax[1].set_title('Limonene')
for i in range(0, 2):
    ax[i].axvline(color='blue', x=6)
    y_opto= ax[i].get_ylim()[1] - 0.5
    ax[i].plot([-1,3],[y_opto,y_opto], color='red')
    ax[i].set_xlabel('Time (s)')
    ax[i].set_ylabel('Trials')
    ax[i].add_patch(Rectangle((0, ax[i].get_ylim()[0]),
                              2, ax[i].get_ylim()[1] +
                              abs(ax[i].get_ylim()[0]),
                              alpha=0.5))
