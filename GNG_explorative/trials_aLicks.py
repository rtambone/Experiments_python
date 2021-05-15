# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:23:03 2021

@author: ricca
"""

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
import pandas as pd

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
processed_data=[[[],[],[],[]],      # a list with single mouse and single day data
                [[],[],[],[]],
                [[],[],[],[]],
                [[],[],[],[]],
                [[],[],[],[]]]
for mouse in (0,2,3,4):
    for day in range(0,4):
        if mouse== 0 and day== 0:  # single case of day 0 for 1f 
            trial_types= mice_data[mouse][day]['TrialTypes']
            trials_data= mice_data[mouse][day]['RawEvents']  # a list with every trial       
        else:
            trial_types= mice_data[mouse][day]['SessionData']['TrialTypes']
            trials_data= mice_data[mouse][day]['SessionData']['RawEvents']['Trial']  # a list with every trial
        csplus_trials= np.zeros(300)
        alick_csplus= np.zeros(300)
        csminus_trials= np.zeros(300)
        alick_csminus= np.zeros(300)
        cum_csplus= np.zeros(299)
        cum_csminus= np.zeros(299)
        cum_alicks_csplus= np.zeros(299)
        cum_alicks_csminus= np.zeros(299)
        for trial in range(0,300):
            bound_inf= trials_data[trial]['States']['DeliverStimulusLate'][0]             
            bound_sup= trials_data[trial]['States']['DeliverStimulusLate'][1]      
            if 'Port1In' in trials_data[trial]['Events']:
                licks= trials_data[trial]['Events']['Port1In'] 
            else: 
                licks= 0
            if trial_types[trial]== 1 or trial_types[trial]== 3 or trial_types[trial]== 2 or trial_types[trial]== 4:                        
                csplus_trials[trial]= 1 
                if np.any(licks>bound_inf) and np.any(licks<bound_sup):
                    alick_csplus[trial]= 1
            elif trial_types[trial]== 5 or trial_types[trial]== 6:                      # if it's neural trials
                csminus_trials[trial]=1
                if np.any(licks>bound_inf) and np.any(licks<bound_sup):
                    alick_csminus[trial]= 1
        for i, c in zip(range(1,300), range(0,299)):       
            cum_csplus[c]= np.nansum(csplus_trials[:i])
            cum_csminus[c]= np.nansum(csminus_trials[:i])
            cum_alicks_csplus[c]= np.nansum(alick_csplus[:i])
            cum_alicks_csminus[c]= np.nansum(alick_csminus[:i])
        percent_csplus= np.nan_to_num(cum_alicks_csplus/cum_csplus*100)
        percent_csminus= np.nan_to_num(cum_alicks_csminus/cum_csminus*100)
        csplus= np.convolve(percent_csplus, np.ones(10)/10, mode= 'full')
        csminus= np.convolve(percent_csminus, np.ones(10)/10, mode= 'full')
        processed_data[mouse][day]=[csplus,csminus]

        


# Compute the mean 
df_csplus= pd.DataFrame()
df_csminus= pd.DataFrame()
for mouse in (0,2,3,4):
    for day in range(0,4):
        d1= pd.Series(processed_data[mouse][day][0])
        df_csplus= df_csplus.append(d1, ignore_index=True)
        d2= pd.Series(processed_data[mouse][day][1])
        df_csminus= df_csminus.append(d2, ignore_index=True)
mean_csplus= df_csplus.mean(axis=0)
mean_csminus= df_csminus.mean(axis=0)
sem_csplus= df_csplus.sem()
sem_csminus= df_csminus.sem()
    
    
# Plot 
matplotlib.rcParams.update({'font.size':22})
x_axes= np.arange(0,298)
fig, ax= plt.subplots(constrained_layout=True)
#fig.suptitle('Population avaraged')
ax.plot(x_axes, mean_csplus[:298], 'b', label='CS+')
ax.fill_between(x_axes, mean_csplus[:298]-sem_csplus[:298], mean_csplus[:298]+sem_csplus[:298], alpha=0.4)
ax.plot(x_axes, mean_csminus[:298], 'r', label='CS-')
ax.fill_between(x_axes, mean_csminus[:298]-sem_csminus[:298], mean_csminus[:298]+sem_csminus[:298], alpha=0.4)
ax.legend(loc='center right')
ax.set_ylabel('% Trials with licks')
ax.set_ylim([0,100])
ax.set_xlabel('Trial')
ax.axhline(y= 20, color='black', ls='--')
ax.axhline(y= 80, color='black', ls='--')

fig.show()

