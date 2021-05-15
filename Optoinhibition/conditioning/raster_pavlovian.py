# -*- coding: utf-8 -*-
"""
Created on Thu May 13 12:07:10 2021

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
mouse_name = mouse_list[1]  # CHANGE THIS
day = '2'                   # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'
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


# Compute how many trials with aLicks
alicksOdor= np.zeros(nTrials)
alicksNoOdor= np.zeros(nTrials)
for trial in range(0,nTrials):
    infBound= trials_data[trial]['States']['LEDon'][0]             
    supBound= trials_data[trial]['States']['LEDon'][1]      
    if 'Port1In' in trials_data[trial]['Events']:
        licks= trials_data[trial]['Events']['Port1In'] 
        if trial_types[trial]== 1:
            if np.any(licks>infBound) and np.any(licks<supBound):
                alicksNoOdor[trial]= 1
        elif trial_types[trial]== 2:                
            if np.any(licks>infBound) and np.any(licks<supBound):
                alicksOdor[trial]= 1
percent_alicksOdor= round(np.sum(alicksOdor)/(nTrials/2)*100, 2)
percent_alicksNoOdor= round(np.sum(alicksNoOdor)/(nTrials/2)*100,2)



# Processing for raster plots 
csMinus = []
csPlus = []
csPlus_idx = np.array(np.where(trial_types == 2))
csPlus_idx = csPlus_idx.reshape(csPlus_idx.shape[1])
csMinus_idx = np.array(np.where(trial_types == 1))
csMinus_idx = csMinus_idx.reshape(csMinus_idx.shape[1])
for TrialType in range(1, 3):
    licksXtrial = []
    idxTrialType = np.array(np.where(trial_types == TrialType))
    for Trial in range(0, idxTrialType.size):
        # if there was a PortIn
        if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:
            licks_ts = np.array(
                trials_data[idxTrialType[0][Trial]]['Events']['Port1In'])
            if licks_ts.shape == ():
                licks_ts = licks_ts.reshape(1)
            if TrialType == 1:    # valve click no odor
                csMinus.append(licks_ts)
            elif TrialType == 2:
                csPlus.append(licks_ts)



# Plotting 
fig, ax = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
fig.suptitle(mouse_name)
ax[0].eventplot(csMinus, colors='black')  # lineoffsets= csMinus_idx)
ax[1].eventplot(csPlus, colors='black')
ax[0].set_title('No odor \n trials with aLicks = ' + str(percent_alicksNoOdor)+'%')
ax[1].set_title('Cymene \n trials with aLicks = ' + str(percent_alicksOdor)+'%')
for i in range(0, 2):
    ax[i].set_ylim([0,nTrials/2])
    ax[i].plot([4,8],[0.3,0.3], color='red')                # red line for optoinhibition
    #ax[i].axvline(color='blue', x=5)                        # blue vertical line for odor onset
    ax[i].set_xlabel('Time (s)')
    ax[i].set_ylabel('Trials')
    ax[i].add_patch(Rectangle((5,0), 
                              width= 2, height= abs(ax[i].get_ylim()[1]),
                              alpha=0.5))
    ax[i].add_patch(Rectangle((10,0), 
                              width= 1, height= abs(ax[i].get_ylim()[1]),
                              alpha=0.5, color= 'red'))
