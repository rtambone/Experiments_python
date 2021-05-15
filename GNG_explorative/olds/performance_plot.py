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
os.chdir(general_dir + specific_dir)
plot_title= '3M - Day 3' ###

data= loadmat('3M_GNG_explorative_noTrialManager_2_20210130_142708.mat', simplify_cells=True)


# Setting up data
trial_types= data['SessionData']['TrialTypes']
number_of_trials= data['SessionData']['nTrials']
trials_data= data['SessionData']['RawEvents']['Trial']  # a list with every trial

# Preprocessing data
hits= np.empty(300)
hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
correct_rejections= np.empty(300)
correct_rejections[:]= np.nan
rewarding_trials= np.zeros(300)
neutral_trials= np.zeros(300)

for i in range(0, 300):                                                 # for each trial
    if trial_types[i]== 1 or trial_types[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials[i]= 1                                 # store trial index
        if not np.isnan(trials_data[i]['States']['Reward'][0]):         # if rewarded
            hits[i]= 1
        else:  
            hits[i]=0
    elif trial_types[i]== 2 or trial_types[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials[i]= 1
        if not np.isnan(trials_data[i]['States']['FakeReward'][0]):
            hits[i]= 1
        else:  
            hits[i]= 0
    elif trial_types[i]== 5 or trial_types[i]== 6:                      # if it's neural trials
        neutral_trials[i]= 1
        if np.isnan(trials_data[i]['States']['TimeOut'][0]):
            correct_rejections[i]= 1
        else:
            correct_rejections[i]= 0

cum_hits= np.empty(30)
cum_corr_rejections= np.empty(30)
cum_rewarding= np.empty(30)
cum_neutral= np.empty(30)
for i,c in zip(range(0,300,10),range(31)):
    cum_rewarding[c]= np.nansum(rewarding_trials[:i+9])
    cum_neutral[c]= np.nansum(neutral_trials[:i+9])
    cum_hits[c]=np.nansum(hits[:i+9])
    cum_corr_rejections[c]=np.nansum(correct_rejections[:i+9])

cum_percent_hits= (cum_hits/cum_rewarding)*100
cum_percent_corr_rejection= (cum_corr_rejections/cum_neutral)*100


# Plots 
fig,ax= plt.subplots()   
fig.suptitle(plot_title)
x_axes= np.arange(10,310,10)
ax.plot(x_axes, cum_percent_hits, 'b', label='Hits')
ax.plot(x_axes, cum_percent_corr_rejection, 'r', label='Correct rejections')
ax.legend(loc='lower right')
ax.set_ylabel('%')
ax.set_ylim([0,101])
ax.set_xlabel('Trials')
fig.tight_layout()
fig.show()