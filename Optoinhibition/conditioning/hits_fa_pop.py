# -*- coding: utf-8 -*-
"""
Created on Wed May 19 19:49:36 2021

@author: ricca
"""

# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import matplotlib
import glob
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.stats import sem 


# Mpl parameters
mpl.rc('font', size=14)  
mpl.use('qt5agg')


# Load data
# List of dirs
# index        0       1       2      3       4       
expGroup= ['PV92','PV94','PV100','PV104','PV107']
conGroup= ['WT58','WT96','WT97','WT98','WT101']
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'

dataExp= [[],[],[]]  # a sublist for each day 
dataCon= [[],[],[]] 

# Load data for experimental group 
for mouse in range(0,5):
    mouseName= expGroup[mouse]
    mouse_dir= general_dir + '\\'+ mouseName
    os.chdir(mouse_dir)
    data_mouse=[]
    for file in glob.glob('*.mat'):
        data_mouse.append(loadmat(file, simplify_cells=True))
    for day in range(0,len(data_mouse)):
        trial_types= data_mouse[day]['SessionData']['TrialTypes']
        trials_data= data_mouse[day]['SessionData']['RawEvents']['Trial'] # a list with every trial
        nTrials= len(trial_types)
        nTrialPlus= len(np.where(trial_types==2)[0])
        nTrialMinus= len(np.where(trial_types==1)[0])
        # Preprocessing data
        hits= np.empty(nTrials)
        hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
        false_alarm= np.empty(nTrials)
        false_alarm[:]= np.nan
        minusTrials= np.zeros(nTrials)
        plusTrials= np.zeros(nTrials)
        #
        for trial in range(0, nTrials):                       
            # MInus trials    
            if trial_types[trial]== 1:                                     
                minusTrials[trial]= 1       
                infBound= trials_data[trial]['States']['LEDon'][0]             
                supBound= trials_data[trial]['States']['LEDon'][1]      
                if 'Port1In' in trials_data[trial]['Events']:
                    licks= trials_data[trial]['Events']['Port1In'] 
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        false_alarm[trial]= 1
                    else:
                        false_alarm[trial]= 0
                else:
                    false_alarm[trial]= 0
            # Plus trials
            if trial_types[trial]== 2:                                      
                plusTrials[trial]= 1       
                infBound= trials_data[trial]['States']['LEDon'][0]             
                supBound= trials_data[trial]['States']['LEDon'][1]      
                if 'Port1In' in trials_data[trial]['Events']:
                    licks= trials_data[trial]['Events']['Port1In'] 
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        hits[trial]= 1
                    else:
                        hits[trial]= 0
                else:
                    hits[trial]= 0
        cum_hits= np.zeros(nTrials)
        cum_fa= np.zeros(nTrials)
        cumPlusTrials= np.zeros(nTrials)
        cumMinusTrials= np.zeros(nTrials)
        cumDiff= np.zeros(nTrials)
        for trial in range(0,nTrials):
            cumPlusTrials[trial]= np.sum(plusTrials[:trial+1])
            cumMinusTrials[trial]= np.sum(minusTrials[:trial+1])
            cum_hits[trial]= np.nansum(hits[:trial+1])
            cum_fa[trial]= np.nansum(false_alarm[:trial+1])
        cumDiff= cum_hits - cum_fa
        cumDiff= np.convolve(cumDiff, np.ones(5)/5, mode= 'valid')
        dataExp[day].append(cumDiff)

# Load data for control group 
HitsCon= [np.zeros((5,150)),np.zeros((5,150)),np.zeros((5,150))] 
FaCon= [np.zeros((5,150)),np.zeros((5,150)),np.zeros((5,150))] 
for mouse in range(0,5):
    mouseName= conGroup[mouse]
    mouse_dir= general_dir + '\\'+ mouseName
    os.chdir(mouse_dir)
    data_mouse=[]
    for file in glob.glob('*.mat'):
        data_mouse.append(loadmat(file, simplify_cells=True))
    for day in range(0,len(data_mouse)):
        trial_types= data_mouse[day]['SessionData']['TrialTypes']
        trials_data= data_mouse[day]['SessionData']['RawEvents']['Trial'] # a list with every trial
        nTrials= len(trial_types)
        nTrialPlus= len(np.where(trial_types==2)[0])
        nTrialMinus= len(np.where(trial_types==1)[0])
        # Preprocessing data
        hits= np.empty(nTrials)
        hits[:]= np.nan     # nan if it is not a rewarding trial, 0 if missed, 1 if rewarded
        false_alarm= np.empty(nTrials)
        false_alarm[:]= np.nan
        minusTrials= np.zeros(nTrials)
        plusTrials= np.zeros(nTrials)
        #
        for trial in range(0, nTrials):                       
            # MInus trials    
            if trial_types[trial]== 1:                                     
                minusTrials[trial]= 1       
                infBound= trials_data[trial]['States']['LEDon'][0]             
                supBound= trials_data[trial]['States']['LEDon'][1]      
                if 'Port1In' in trials_data[trial]['Events']:
                    licks= trials_data[trial]['Events']['Port1In'] 
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        false_alarm[trial]= 1
                    else:
                        false_alarm[trial]= 0
                else:
                    false_alarm[trial]= 0
            # Plus trials
            if trial_types[trial]== 2:                                      
                plusTrials[trial]= 1       
                infBound= trials_data[trial]['States']['LEDon'][0]             
                supBound= trials_data[trial]['States']['LEDon'][1]      
                if 'Port1In' in trials_data[trial]['Events']:
                    licks= trials_data[trial]['Events']['Port1In'] 
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        hits[trial]= 1
                    else:
                        hits[trial]= 0
                else:
                    hits[trial]= 0
        cum_hits= np.zeros(nTrials)
        cum_fa= np.zeros(nTrials)
        cumPlusTrials= np.zeros(nTrials)
        cumMinusTrials= np.zeros(nTrials)
        cumDiff= np.zeros(nTrials)
        for trial in range(0,nTrials):
            cumPlusTrials[trial]= np.sum(plusTrials[:trial+1])
            cumMinusTrials[trial]= np.sum(minusTrials[:trial+1])
            cum_hits[trial]= np.nansum(hits[:trial+1])
            cum_fa[trial]= np.nansum(false_alarm[:trial+1])
        cumDiff= cum_hits - cum_fa
        cumDiff= np.convolve(cumDiff, np.ones(5)/5, mode= 'valid')
        dataCon[day].append(cumDiff)
            
# Compute mean 
meanExp=[[],[],[]]
semExp= [[],[],[]]
meanCon=[[],[],[]]
semCon= [[],[],[]]
for day in range(0,3):
    data=np.zeros((5, len(cumDiff)))
    for mouse in range(0,5):
        data[mouse]= dataExp[day][mouse]
    mean= np.mean(data, axis=0)
    sem_d= sem(data, axis=0) 
    meanExp[day]= mean
    semExp[day]= sem_d
    
for day in range(0,3):
    data=np.zeros((5, len(cumDiff)))
    data[:]= np.nan
    for mouse in range(0,5):
        data[mouse][:len(dataCon[day][mouse])]= dataCon[day][mouse]
    mean= np.nanmean(data, axis=0)
    sem_d= sem(data, axis=0, nan_policy='omit') 
    meanCon[day]= mean
    semCon[day]= sem_d



# Plot 
colors= [31,120,180],[106,61,154],[227,26,28],[251,127,0],[82,82,82]
colors= np.divide(colors, 251)

fig, ax= plt.subplots(nrows=3, ncols=2,constrained_layout=True)
fig.suptitle('Hits-False Alarms', fontweight='bold')
# Exp 
for day in range(0,3):
    for mouse in range(0,5):
        plot_trials= len(dataExp[day][mouse])
        x_axes= np.arange(0,plot_trials)
        ax[day,0].plot(x_axes,dataExp[day][mouse], color= colors[mouse], label=expGroup[mouse], 
                       ls='--', lw=3)
    # plot mean and sem 
    ax[day,0].plot(x_axes, meanExp[day], color='blue', lw=4, label='Mean')
    ax[day,0].fill_between(x_axes, meanExp[day]+semExp[day], meanExp[day]-semExp[day], 
                           'blue', alpha=0.5)
# Con 
for day in range(0,3):
    for mouse in range(0,5):
        plot_trials= len(dataCon[day][mouse])
        x_axes= np.arange(0,plot_trials)
        ax[day,1].plot(x_axes,dataCon[day][mouse], color= colors[mouse], label=conGroup[mouse],
                       ls='--', lw=3)
    # plot mean and sem 
    ax[day,1].plot(x_axes, meanCon[day], color='red', lw=4, label='Mean')
    ax[day,1].fill_between(x_axes, meanCon[day]+semCon[day], meanCon[day]-semCon[day], 
                           color='red', alpha=0.5)
for i in range(0,3):
    ax[i,0].set_ylim(-12,70)
    ax[i,1].set_ylim(-12,70)
    ax[i,0].set_xlim(0,145)
    ax[i,1].set_xlim(0,145)
    ax[i,0].set_ylabel('Day '+str(i+1), fontweight='bold')
ax[0,0].legend()
ax[0,1].legend()    
ax[0,0].set_title('Experimental group')
ax[0,1].set_title('Control group')
ax[2,0].set_xlabel('Trials')
ax[2,1].set_xlabel('Trials')
