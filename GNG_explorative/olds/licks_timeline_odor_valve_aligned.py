# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:21:11 2021

@author: ricca
"""

import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2' ###
specific_dir= r'\3M\GNG_explorative_noTrialManager_2\Session Data' 
plot_dir= r'\2M\Plots'  
os.chdir(general_dir + specific_dir)
plot_title= '3M - day 3' ###

data= loadmat('3M_GNG_explorative_noTrialManager_2_20210130_142708.mat', simplify_cells=True)

# Setting up data
trial_types= data['SessionData']['TrialTypes']
number_of_trials= data['SessionData']['nTrials']
trials_data= data['SessionData']['RawEvents']['Trial']  # a list with every trial


# Data preprocessing
licked_trials_timestamps=[] # port1in timestamps
licked_trials_types=[]      # types of trials
licked_trials=[]            # trial number  
for trial in range(0, number_of_trials):    #check all trials   
    if 'Port1In' in trials_data[trial]['Events']:    #if there was a PortIn 
        port1in_timestamps= np.array([trials_data[trial]['Events']['Port1In']]) - 3
        licked_trials_timestamps.append(port1in_timestamps)    
        licked_trials_types.append(trial_types[trial])
        licked_trials.append(trial)


rewarding_trials_timestamps=[]         # port1in timestamps
rewarding_trials_ntrials=[]            # number of trials
neutral_trials_timestamps=[]
neutral_trials_ntrials=[]
us_trials_timestamps=[]
us_trials_ntrials=[]
for i in range(0, len(licked_trials)):
    if trial_types[i]== 1 or trial_types[i]== 2 or trial_types[i]== 3 or trial_types[i]== 4:
        rewarding_trials_timestamps.append(licked_trials_timestamps[i])
        rewarding_trials_ntrials.append(licked_trials[i])
    elif trial_types[i]== 5 or trial_types[i]== 6:
        neutral_trials_timestamps.append(licked_trials_timestamps[i])
        neutral_trials_ntrials.append(licked_trials[i])
    elif trial_types[i]== 7:
        us_trials_timestamps.append(licked_trials_timestamps[i])
        us_trials_ntrials.append(licked_trials[i])
        


# Plots
fig, axes= plt.subplots(nrows=3, ncols=1, dpi=100, constrained_layout=True)  # default dpi 
fig.suptitle(plot_title)
# rewarding trials
for i in range(0,len(rewarding_trials_ntrials)):
    yaxes= np.array([rewarding_trials_ntrials[i]]*len(rewarding_trials_timestamps[i]))
    axes[0].plot(rewarding_trials_timestamps[i], yaxes, 'bo')  
axes[0].axvline(color='red')
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Trials')
axes[0].set_title('Rewarding trials')

# neutral trials
for i in range(0,len(neutral_trials_ntrials)):
    yaxes= np.array([neutral_trials_ntrials[i]]*len(neutral_trials_timestamps[i]))
    axes[1].plot(neutral_trials_timestamps[i], yaxes, 'bo')  
axes[1].axvline(color='red')
axes[1].set_xlabel('Time (s)')
axes[1].set_ylabel('Trials')
axes[1].set_title('Neutral trials')

# US trials
for i in range(0,len(us_trials_ntrials)):
    yaxes= np.array([us_trials_ntrials[i]]*len(rewarding_trials_timestamps[i]))
    axes[2].plot(us_trials_timestamps[i], yaxes, 'bo')  
axes[2].axvline(color='red')
axes[2].set_xlabel('Time (s)')
axes[2].set_ylabel('Trials')
axes[2].set_title('US trials')
#fig.tight_layout()
fig.show()
#plt.savefig(fname=general_dir+plot_dir+plot_name)