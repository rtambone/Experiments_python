# -*- coding: utf-8 -*-
"""
Created on Wed May 19 15:20:49 2021

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
mouse_name = mouse_list[9]  # CHANGE THIS                   # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'
mouse_dir = general_dir + '\\' + mouse_name


# Load data
os.chdir(mouse_dir)
data = []
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))



csMinus = [[],[],[]]
csPlus = [[],[],[]]
for day in range(0, len(data)):
    trial_types = data[day]['SessionData']['TrialTypes']
    trials_data = data[day]['SessionData']['RawEvents']['Trial']
    nTrials= len(trial_types)
    nTrialOdor= len(np.where(trial_types==2)[0])
    nTrialNoOdor= len(np.where(trial_types==1)[0])
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
                    csMinus[day].append(licks_ts)
                elif TrialType == 2:
                    csPlus[day].append(licks_ts)







'''
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
percent_alicksOdor= round(np.sum(alicksOdor)/(nTrialOdor)*100, 2)
percent_alicksNoOdor= round(np.sum(alicksNoOdor)/(nTrialNoOdor)*100,2)
'''

# Plotting 
fig, ax = plt.subplots(nrows=3, ncols=2,
                       sharey= 'col', sharex= True)
fig.suptitle(mouse_name)
for a in range(0,3):
    ax[a,0].eventplot(csPlus[a], colors='black', alpha=1)    
    ax[a,1].eventplot(csMinus[a], colors='black', alpha=1)
    ax[a,0].set_ylim(75,0)
    ax[a,1].set_ylim(75,0)
    ax[a,0].tick_params(left=False, labelleft=False)
    ax[a,1].tick_params(left=False, labelleft=False)
    ax[a,0].set_ylabel('Day'+str(a+1))
    ax[a,0].add_patch(Rectangle((5,0), 
                                 width= 2, height= abs(ax[a,0].get_ylim()[0]),
                                 alpha=0.5))
    ax[a,1].add_patch(Rectangle((5,0), 
                                 width= 2, height= abs(ax[a,1].get_ylim()[0]),
                                 alpha=0.5))    
    ax[a,0].add_patch(Rectangle((10,0), 
                                 width= 1, height= abs(ax[a,0].get_ylim()[0]),
                                 alpha=0.5, color= 'red'))
    ax[a,1].add_patch(Rectangle((10,0), 
                                 width= 1, height= abs(ax[a,1].get_ylim()[0]),
                                 alpha=0.5, color= 'red'))
    
plt.subplots_adjust(hspace=0, wspace=0)
ax[0,0].set_title('Cymene')
ax[0,1].set_title('No odor')
ax[2,0].set_xlabel('Time (s)')
ax[2,1].set_xlabel('Time (s)')
