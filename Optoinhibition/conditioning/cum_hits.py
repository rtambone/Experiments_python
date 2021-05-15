# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:00:02 2021

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
day = '0'            # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\conditioning'
mouse_dir = general_dir + '\\' + mouse_name

# Load data
os.chdir(mouse_dir)
data = []
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))

trial_types = data[int(day)]['SessionData']['TrialTypes']       # a list with every trial
trials_data = data[int(day)]['SessionData']['RawEvents']['Trial']
nTrials= len(trial_types)

# Preprocessing data
hits= np.empty(nTrials)
hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
miss= np.empty(nTrials)
miss[:]= np.nan
correct_rejections= np.empty(nTrials)
correct_rejections[:]= np.nan
false_alarm= np.empty(nTrials)
false_alarm[:]= np.nan
noOdor_trials= np.zeros(nTrials)
Limonene_trials= np.zeros(nTrials)


for trial in range(0, nTrials):                                     # for each trial
    if trial_types[trial]== 1:                                      # if no odor
        noOdor_trials[trial]= 1                                 
        if np.isnan(trials_data[trial]['States']['TimeOut'][0]):    # if correct
            correct_rejections[trial]= 1
            false_alarm[trial]= 0  
        else:                                                       # if wrong 
            correct_rejections[trial]= 0
            false_alarm[trial]= 1  
    if  trial_types[trial]==2:                                      # if odor rewarded
        Limonene_trials[trial]=1
        if not np.isnan(trials_data[trial]['States']['Reward'][0]): # if correct      
            hits[trial]= 1
            miss[trial]= 0
        else:                                                       # if wrong 
            hits[trial]= 0
            miss[trial]= 1
    if  trial_types[trial]==3:                                      # if odor not rewarded
        Limonene_trials[trial]=1
        if not 'Port1In' in trials_data[trial]['Events']:           # if there're not licking 
            hits[trial]= 0
            miss[trial]= 1
        else:                                                       # if they lick
            inf_bound= trials_data[trial]['States']['TimeForResponse'][0]
            sup_bound= trials_data[trial]['States']['TimeForResponse'][1]
            licks= trials_data[trial]['Events']['Port1In']
            if np.any(licks>inf_bound) and np.any(licks<sup_bound): # check if they happened 
                hits[trial]= 1                                      # in the right time window
                miss[trial]= 0
            else:
                hits[trial]=0
                miss[trial]=1



cum_hits= np.zeros(nTrials)
cum_miss= np.zeros(nTrials)
cum_corr_rejections= np.zeros(nTrials)
cum_false_alarm= np.zeros(nTrials)
cum_odor= np.zeros(nTrials)
cum_noOdor= np.zeros(nTrials)
for trial in range(0,nTrials):
    cum_odor[trial]= np.sum(Limonene_trials[:trial+1])
    cum_noOdor[trial]= np.sum(noOdor_trials[:trial+1])
    cum_hits[trial]=np.nansum(hits[:trial+1])
    cum_miss[trial]= np.nansum(miss[:trial+1])
    cum_corr_rejections[trial]=np.nansum(correct_rejections[:trial+1])
    cum_false_alarm[trial]= np.nansum(false_alarm[:trial+1])
cum_diff_hits_fa= cum_hits - cum_false_alarm
#cum_diff_corrRej_falseAlarm= cum_corr_rejections - cum_false_alarm


#percent_diff= np.nan_to_num(cum_diff_hits_fa/cum_odor*100)
#percent_hits= np.nan_to_num(cum_hits/cum_odor*100)

cumHits= np.convolve(cum_hits, np.ones(5)/5, mode= 'valid')
cumDiff= np.convolve(cum_diff_hits_fa, np.ones(5)/5, mode= 'valid')

    
    
# Plot 
plot_trials= len(cumHits)
x_axes= np.arange(0,plot_trials)
eightyPercent= 8*sum(Limonene_trials)/10
fig, ax= plt.subplots(constrained_layout=True)
fig.suptitle(mouse_name)
ax.plot(x_axes, cumHits[:plot_trials], 'b', label='Hits')
ax.plot(x_axes, cumDiff[:plot_trials], 'r', label='Hits - False Alarms')
ax.legend()
ax.set_ylabel('')
#ax.set_ylim([-100,100])
ax.set_xlabel('Trial')
#ax.axhline(y= 20, color='black', ls='--')
ax.axhline(y= eightyPercent, color='black', ls='--')


