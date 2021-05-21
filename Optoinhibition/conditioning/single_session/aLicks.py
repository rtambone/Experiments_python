# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:19:12 2021

@author: ricca
"""

# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import matplotlib
import glob
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
matplotlib.use('qt5agg')


# List of dirs
# index        0       1       2      3       4       5      6      7     8       9
mouse_list= ['PV92','PV94','PV100','PV104','PV107','WT58','WT96','WT97','WT98','WT101']
mouse_name = mouse_list[4]  # CHANGE THIS
day = '2'            # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'
mouse_dir = general_dir + '\\' + mouse_name


# Load data
os.chdir(mouse_dir)
data = []
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))

trial_types = data[int(day)]['SessionData']['TrialTypes']       # a list with every trial
trials_data = data[int(day)]['SessionData']['RawEvents']['Trial']
nTrials= len(trial_types)

odor_trials= np.zeros(nTrials)
alicksOdor= np.zeros(nTrials)
noOdor_trials= np.zeros(nTrials)
alicksNoOdor= np.zeros(nTrials)
for trial in range(0,nTrials):
    infBound= trials_data[trial]['States']['LEDon'][0]             
    supBound= trials_data[trial]['States']['LEDon'][1] 
    if trial_types[trial]== 1:
        noOdor_trials[trial]= 1 
    else:
        odor_trials[trial]=1
    if 'Port1In' in trials_data[trial]['Events']:
        licks= trials_data[trial]['Events']['Port1In'] 
        if trial_types[trial]== 1:
            if np.any(licks>infBound) and np.any(licks<supBound):
                alicksNoOdor[trial]= 1
        elif trial_types[trial]== 2:                
            if np.any(licks>infBound) and np.any(licks<supBound):
                alicksOdor[trial]= 1

percentOdor= np.zeros(nTrials-5)
percentNoOdor= np.zeros(nTrials-5)
for trial in range(5,nTrials):
    percentOdor[trial-5]= np.sum(alicksOdor[:trial])/np.sum(odor_trials[:trial])*100
    percentNoOdor[trial-5]= np.sum(alicksNoOdor[:trial])/np.sum(noOdor_trials[:trial])*100
cum_alicksOdor_convolved= np.convolve(percentOdor, np.ones(5)/5, mode= 'valid')
cum_alicksNoOdor_convolved= np.convolve(percentNoOdor, np.ones(5)/5, mode= 'valid')


# Plot 
#matplotlib.rcParams.update({'font.size':22})
plot_trials= len(cum_alicksOdor_convolved)
x_axes= np.arange(0,plot_trials)
fig, ax= plt.subplots(constrained_layout=True)
fig.suptitle(mouse_name)
ax.plot(x_axes, cum_alicksOdor_convolved[:plot_trials], 'b', label='Odor trials')
ax.plot(x_axes, cum_alicksNoOdor_convolved[:plot_trials], 'r', label='No odor trials')
ax.legend(loc='best')
ax.set_ylabel('% Trials with aLicks')
ax.set_xlabel('Trial')
#ax.set_ylim([-100,100])
ax.axhline(y= 20, color='black', ls='--')
ax.axhline(y= 80, color='black', ls='--')

