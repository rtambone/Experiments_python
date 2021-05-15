import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib 
# matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Categorization_no_punishment\3M\GNG_exporative_noTrialManager' ###
data_dir= r'\Session Data' 
plot_dir= r'\Plots'  
plot_name= '01.23.2020' ###
os.chdir(general_dir + data_dir)
data= loadmat('3M_GNG_exporative_noTrialManager_20210123_125531.mat', simplify_cells=True)

# Setting up data
data= data['SessionData']
trial_types= data['TrialTypes']
number_of_trials= data['nTrials']
trials_data= data['RawEvents']['Trial']  # a list with every trial

# Data preprocessing 
licked_trials_timestamps=[] # port1in timestamps
licked_trials_types=[]      # types of trials
licked_trials=[]            # trial number  
for trial in range(0, number_of_trials):    #check all trials   
    if 'Port1In' in trials_data[trial]['Events']:    #if there was a PortIn 
        port1in_timestamps= np.array([trials_data[trial]['Events']['Port1In']])
        licked_trials_timestamps.append(port1in_timestamps)    
        licked_trials_types.append(trial_types[trial])
        licked_trials.append(trial)

for trial in range(0,len(licked_trials)):
    if licked_trials_types[trial]== 1 or licked_trials_types[trial]== 2 or licked_trials_types[trial]== 3 or licked_trials_types[trial]==4:
        for ts in range(0, len(licked_trials[trial])): # for each port1in timestamp
            if licked_trials_timestamps[trial][ts] => trials_data[trial]

rewarding_trials=[]
rewarding_trials_idx=[]
neutral_trials=[]
neutral_trials_idx=[]
us_trials=[]
us_trials_idx=[]
for i in range(0, number_of_trials):
    if trial_types[i]== 1 or trial_types[i]== 2 or trial_types[i]== 3 or trial_types[i]== 4:
        rewarding_trials.append(trials_list[i])
        rewarding_trials_idx.append(i+1)
    elif trial_types[i]== 5 or trial_types[i]== 6:
        neutral_trials.append(trials_list[i])
        neutral_trials_idx.append(i+1)
    elif trial_types[i]== 7:
        us_trials.append(trials_list[i])
        us_trials_idx.append(i+1)
        
reward_opening_time=[]        
for i in range(0, number_of_trials):
    if trial_types[i]== 1 or trial_types[i]== 2 or trial_types[i]== 3 or trial_types[i]== 4:
        reward_opening_time.append(trial_data[i]['States']['Reward'][0])

for i in range(0, len(rewarding_trials)):
    rewarding_trials[i]= rewarding_trials[i] - reward_opening_time[i]


# pseudocode for hitting and missing 
if trial_types




# Plots
fig, axes= plt.subplots(nrows=3, ncols=1, dpi=100)  # default dpi 
fig.tight_layout()
# rewarding trials
for i in range(0,len(rewarding_trials_idx)):
    if not isinstance(rewarding_trials[i][0], list): # if it's an array - exclude where there aren't response
        if not isinstance(rewarding_trials[i][0], np.float):
          yaxes= np.array([rewarding_trials_idx[i]]*len(rewarding_trials[i][0]))
          axes[0].plot(rewarding_trials[i][0], yaxes, 'bo')  
axes[0].axvline(color='red')
axes[0].set_xlabel('Time (s)')
axes[0].set_ylabel('Trials')
axes[0].set_title('Rewarding trials')

# neutral trials
for i in range(0,len(neutral_trials_idx)):
    if not isinstance(neutral_trials[i][0], list): # if it's an array - exclude where there aren't response
        if not isinstance(neutral_trials[i][0], np.float):
          yaxes= np.array([neutral_trials_idx[i]]*len(neutral_trials[i][0]))
          axes[1].plot(neutral_trials[i][0], yaxes, 'bo')  
axes[1].axvline(color='red')
axes[1].set_xlabel('Time (s)')
axes[1].set_ylabel('Trials')
axes[1].set_title('Neutral trials')

# US trials
for i in range(0,len(us_trials_idx)):
    if not isinstance(us_trials[i][0], list): # if it's an array - exclude where there aren't response
        if not isinstance(us_trials[i][0], np.float):
          yaxes= np.array([us_trials_idx[i]]*len(us_trials[i][0]))
          axes[1].plot(us_trials[i][0], yaxes, 'bo')  
axes[2].axvline(color='red')
axes[2].set_xlabel('Time (s)')
axes[2].set_ylabel('Trials')
axes[2].set_title('US trials')
fig.show()