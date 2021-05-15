# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 10:14:47 2021

@author: ricca
"""
#clear all
from IPython import get_ipython 
get_ipython().magic('reset -sf')

#
import os 
import glob 
from scipy.io import loadmat
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# List of dirs
mouse1f=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\1F\GNG_explorative_noTrialManager_2\Session Data'
mouse2f=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2F\GNG_explorative_noTrialManager_2\Session Data'
mouse4f=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\4F\GNG_explorative_noTrialManager_2\Session Data'
mouse2m=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2M\GNG_explorative_noTrialManager_2'
mouse3m=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\3M\GNG_explorative_noTrialManager_2\Session Data'

mouse1f_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\1F\GNG_reversal\Session Data'
mouse2f_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2F\GNG_reversal\Session Data'
mouse4f_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\4F\GNG_reversal\Session Data'
mouse2m_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2M\GNG_reversal\Session Data'
mouse3m_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\3M\GNG_reversal\Session Data'

mice_dir=[]
mice_dir.append((mouse1f, mouse1f_r))
mice_dir.append((mouse2f, mouse2f_r))
mice_dir.append((mouse4f, mouse4f_r))
mice_dir.append((mouse2m, mouse2m_r))
mice_dir.append((mouse3m, mouse3m_r))


# Load data 
# mice data contains an element for each mouse
mice_data=[]
for mouse in range(0, len(mice_dir)):
    data_m=[]
    for sess in range(0,2):
        data_s=[]
        os.chdir(mice_dir[mouse][sess])
        if mouse==0 and sess==0:
            import pickle 
            with open('1F_day1', 'rb') as data_dict_fil:
                data_s.append(pickle.load(data_dict_fil))
        for file in glob.glob('*.mat'):
            data_s.append(loadmat(file, simplify_cells=True))
        data_m.extend(data_s)
    mice_data.append(data_m)


# Preprocess data
processed_data=[] # each element is a mouse, with two elements for hits+rej and false alarm
for mouse in range(0,len(mice_data)):
    hits_corr_rej_percent= np.zeros(len(mice_data[mouse]))
    false_alarm_percent= np.zeros(len(mice_data[mouse]))
    for day in range(0,len(mice_data[mouse])):
        if mouse== 0 and day== 0:
            trial_types= mice_data[mouse][day]['TrialTypes']
            trials_data= mice_data[mouse][day]['RawEvents']  # a list with every trial       
        else:
            trial_types= mice_data[mouse][day]['SessionData']['TrialTypes']
            trials_data= mice_data[mouse][day]['SessionData']['RawEvents']['Trial']  # a list with every trial
        rewarding_trials=0
        neutral_trials=0
        hits=0
        false_alarm=0
        correct_rejections=0
        for trial in range(0,300):
            if trial_types[trial]== 1 or trial_types[trial]== 3:                        # if it's o1 or o2 rewarded
                rewarding_trials= rewarding_trials+1                                          # store trial index
                if not np.isnan(trials_data[trial]['States']['Reward'][0]):         # if rewarded
                    hits= hits+1
            elif trial_types[trial]== 2 or trial_types[trial]== 4:                      # if it's o1 or o2 fake rewarded
                rewarding_trials= rewarding_trials+1
                if not np.isnan(trials_data[trial]['States']['FakeReward'][0]):
                    hits= hits+1
            elif trial_types[trial]== 5 or trial_types[trial]== 6:                      # if it's neural trials
                neutral_trials=neutral_trials+1
                if not np.isnan(trials_data[trial]['States']['TimeOut'][0]):
                    false_alarm= false_alarm+1
                else:
                    correct_rejections= correct_rejections+1
        hits_corr_rej_percent[day]= (hits+correct_rejections)/(rewarding_trials+neutral_trials)*100
        false_alarm_percent[day]= false_alarm/neutral_trials*100
    processed_data.append((hits_corr_rej_percent, false_alarm_percent))

# Compute the mean 
nMice= 5 
nSessions= 9
correct_percent= np.zeros((nMice, nSessions))
correct_percent[1,0]= np.nan
false_alarm_percent= np.zeros((nMice, nSessions))
false_alarm_percent[1,0]= np.nan
for mouse in range(0,len(processed_data)):
    if not mouse==1:
        correct_percent[mouse,:]= processed_data[mouse][0]
        false_alarm_percent[mouse,:]= processed_data[mouse][1]
    else:
        correct_percent[mouse,1:]= processed_data[mouse][0]
        false_alarm_percent[mouse,1:]= processed_data[mouse][1]
mean_corr= np.nanmean(correct_percent, axis=0)
mean_false= np.nanmean(false_alarm_percent, axis=0)
    
    
# Plot 
x_axes= np.arange(1,len(mean_corr)+1)
fig, ax= plt.subplots(constrained_layout=True)
fig.suptitle('Population avaraged')
ax.plot(x_axes, mean_corr, 'b--', marker='s',
        markersize= 10, label='Hits+Correct rejections')
ax.plot(x_axes, mean_false, 'r--', marker='o',
        markersize=10, label='False Alarms')
for mouse in range(0, len(mice_data)):
    ax.plot(x_axes, correct_percent[mouse], 'b', marker='s', ls='none', alpha=0.6)
    ax.plot(x_axes, false_alarm_percent[mouse], 'r', marker='o', ls='none', alpha=0.6)
ax.legend()
ax.set_ylabel('%')
#ax.set_ylim([50,102])
ax.set_xticks(x_axes)
ax.set_xlabel('Session')
ax.axvline(x= 5, color='black', ls='--')
ax.text(5.05,95, 'Reversal', fontsize=14)
fig.show()
