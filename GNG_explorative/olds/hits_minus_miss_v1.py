import os 
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2' 
specific_dir= r'\1F\GNG_explorative_noTrialManager_2\Session Data' ###
os.chdir(general_dir + specific_dir)
plot_title= '1F - Day 1' ###

import pickle 
with open('data_dict', 'rb') as data_dict_fil:
    data_1f= pickle.load(data_dict_fil)

# Setting up data
trial_types= data_1f['TrialTypes']
number_of_trials= data_1f['nTrials']
trials_data= data_1f['RawEvents']  # a list with every trial


# Preprocessing data
hits= np.empty(300)
hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
miss= np.empty(300)
miss[:]= np.nan
correct_rejections= np.empty(300)
correct_rejections[:]= np.nan
false_alarm= np.empty(300)
false_alarm[:]= np.nan
rewarding_trials= np.zeros(300)
neutral_trials= np.zeros(300)

for i in range(0, 300):                                                 # for each trial
    if trial_types[i]== 1 or trial_types[i]== 3:                        # if it's o1 or o2 rewarded
        rewarding_trials[i]= 1                                 # store trial index
        if not np.isnan(trials_data[i]['States']['Reward'][0]):         # if rewarded
            hits[i]= 1
            miss[i]= 0
        else:  
            hits[i]= 0
            miss[i]= 1
    elif trial_types[i]== 2 or trial_types[i]== 4:                      # if it's o1 or o2 fake rewarded
        rewarding_trials[i]= 1
        if not np.isnan(trials_data[i]['States']['FakeReward'][0]):
            hits[i]= 1
            miss[i]= 0
        else:  
            hits[i]= 0
            miss[i]= 1   
    elif trial_types[i]== 5 or trial_types[i]== 6:                      # if it's neural trials
        neutral_trials[i]= 1
        if np.isnan(trials_data[i]['States']['TimeOut'][0]):
            correct_rejections[i]= 1
            false_alarm[i]= 0
        else:
            correct_rejections[i]= 0
            false_alarm[i]= 1
cum_hits= np.empty(300)
cum_miss= np.empty(300)
cum_corr_rejections= np.empty(300)
cum_false_alarm= np.empty(300)
cum_rewarding= np.empty(300)
cum_neutral= np.empty(300)
for i in range(0,300):
    cum_rewarding[i]= np.nansum(rewarding_trials[:i+1])
    cum_neutral[i]= np.nansum(neutral_trials[:i+1])
    cum_hits[i]=np.nansum(hits[:i+1])
    cum_miss[i]= np.nansum(miss[:i+1])
    cum_corr_rejections[i]=np.nansum(correct_rejections[:i+1])
    cum_false_alarm[i]= np.nansum(false_alarm[:i+1])
cum_diff_hits_miss= cum_hits - cum_miss
cum_diff_corrRej_falseAlarm= cum_corr_rejections - cum_false_alarm


# Plots 
fig,ax= plt.subplots(constrained_layout=True)   
fig.suptitle(plot_title)
x_axes= np.arange(1,301)
ax.plot(x_axes, cum_diff_hits_miss, 'b', label='Hits - Misses')
ax.plot(x_axes, cum_diff_corrRej_falseAlarm, 'r', label='Correct rejections - False alarms')
ax.legend(loc='lower right')
#ax.set_ylabel('%')
#ax.set_ylim([0,101])
ax.set_xlabel('Trials')
#fig.tight_layout()
fig.show()