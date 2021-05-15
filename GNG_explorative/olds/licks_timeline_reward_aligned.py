# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 23:18:33 2021

@author: ricca
"""

import os 
from scipy.io import loadmat
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Categorization_no_punishment\Data\3M' ###
specific_dir= r'\GNG_exporative_noTrialManager\Session Data' 
plot_dir= r'\GNG_exporative_noTrialManager\Plots'  
os.chdir(general_dir + specific_dir)
plot_title= '1F - Day 2'
data= loadmat('3M_GNG_exporative_noTrialManager_20210123_125531.mat', simplify_cells=True)

# Setting up data
data= data['SessionData']
trial_types= data['TrialTypes']
number_of_trials= data['nTrials']
trials_data= data['RawEvents']['Trial']  # a list with every trial

# Data preprocessing 
port1in_timestamps=[]   # only for rewarding trials
rewarding_ntrials=[]     # number of trial
for i in range(0, number_of_trials):      
    if trial_types[i]== 1 or trial_types[i]== 3:
        if not np.isnan(trials_data[i]['States']['Reward'][0]):
            port1in= np.array([trials_data[i]['Events']['Port1In']])
            port1in_timestamps.append(port1in)
            rewarding_ntrials.append(i+1)
        else:
            port1in= np.nan
            port1in_timestamps.append(port1in)
            rewarding_ntrials.append(i+1)

reward_opening_time=[]        
for i in range(0, number_of_trials):
    if trial_types[i]== 1 or trial_types[i]== 3:
        if not np.isnan(trials_data[i]['States']['Reward'][0]):
            reward_opening_time.append(trials_data[i]['States']['Reward'][0])
        else:
            reward_opening_time.append(np.nan)
           

port1in_timestamps_aligned= []
for i in range(0, len(port1in_timestamps)):
    port1in_timestamps_aligned.append(port1in_timestamps[i] - reward_opening_time[i])

        
    
# Plots
fig, axes= plt.subplots(constrained_layout=True)  # default dpi 
fig.suptitle(plot_title)
# rewarding trials
for i in range(0,len(rewarding_ntrials)):
    if not isinstance(port1in_timestamps_aligned[i], np.float):
        yaxes= np.array([rewarding_ntrials[i]]*len(port1in_timestamps[i]))
        axes.plot(port1in_timestamps_aligned[i], yaxes, 'bo')  
axes.axvline(color='red')
axes.set_xlabel('Time (s)')
axes.set_ylabel('Trials')
#axes[0].set_title('Rewarding trials')
#fig.tight_layout()
fig.show()
#plt.savefig(fname=general_dir+plot_dir+plot_name)