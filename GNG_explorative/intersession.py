# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:07:42 2021

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
#mouse1f=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\1F\GNG_explorative_noTrialManager_2\Session Data'
#mouse2f=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2F\GNG_explorative_noTrialManager_2\Session Data'
mouse4f=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\4F\GNG_explorative_noTrialManager_2\Session Data'
mouse2m=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2M\GNG_explorative_noTrialManager_2'
mouse3m=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\3M\GNG_explorative_noTrialManager_2\Session Data'

#mouse1f_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\1F\GNG_reversal\Session Data'
#mouse2f_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2F\GNG_reversal\Session Data'
mouse4f_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\4F\GNG_reversal\Session Data'
mouse2m_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\2M\GNG_reversal\Session Data'
mouse3m_r=r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2\3M\GNG_reversal\Session Data'


# Load data 
os.chdir(mouse3m)
data=[]
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))
os.chdir(mouse3m_r)
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))


# Preprocess data
hits_corr_rej_percent= np.zeros(len(data))
false_alarm_percent= np.zeros(len(data))
for day in range(0,len(data)):
    trial_types= data[day]['SessionData']['TrialTypes']
    trials_data= data[day]['SessionData']['RawEvents']['Trial']  # a list with every trial
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

# Plot
x_axes= np.arange(1,len(data)+1)
fig, ax= plt.subplots(constrained_layout=True)
fig.suptitle('Mouse 3M')
ax.plot(x_axes, hits_corr_rej_percent, 'b--', marker='s',
        markersize= 10, label='Hits+Correct rejections')
ax.plot(x_axes, false_alarm_percent, 'r--', marker='o',
        markersize=10, label='False Alarms')
ax.legend()
ax.set_ylabel('%')
#ax.set_ylim([50,102])
ax.set_xticks(x_axes)
ax.set_xlabel('Session')
ax.axvline(x= 5, color='black', ls='--')
ax.text(5.05,95, 'Reversal', fontsize=14)
fig.show()