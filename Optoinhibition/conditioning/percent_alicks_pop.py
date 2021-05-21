# -*- coding: utf-8 -*-
"""
Created on Wed May 19 18:19:46 2021

@author: ricca
"""


# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import os 
import glob 
from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
mpl.use('qt5agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# List of dirs
# index        0       1       2      3       4       
expGroup= ['PV92','PV94','PV100','PV104','PV107']
conGroup= ['WT58','WT96','WT97','WT98','WT101']
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'


# Experimental group 
alicksExpPlusPercent= [np.zeros(5),np.zeros(5),np.zeros(5)]  
alicksExpMinusPercent= [np.zeros(5),np.zeros(5),np.zeros(5)]  
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
        alicksPlus= np.zeros(nTrials)
        alicksMinus= np.zeros(nTrials)
        for trial in range(0,nTrials):
            infBound= trials_data[trial]['States']['LEDon'][0]             
            supBound= trials_data[trial]['States']['LEDon'][1]      
            if 'Port1In' in trials_data[trial]['Events']:
                licks= trials_data[trial]['Events']['Port1In'] 
                if trial_types[trial]== 1:
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        alicksMinus[trial]= 1
                elif trial_types[trial]== 2:                
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        alicksPlus[trial]= 1
        alicksExpPlusPercent[day][mouse]= np.sum(alicksPlus)/(nTrialPlus)*100
        alicksExpMinusPercent[day][mouse]= np.sum(alicksMinus)/(nTrialMinus)*100
        
# Control group 
alicksConPlusPercent= [np.zeros(5),np.zeros(5),np.zeros(5)]  
alicksConMinusPercent= [np.zeros(5),np.zeros(5),np.zeros(5)]  
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
        alicksPlus= np.zeros(nTrials)
        alicksMinus= np.zeros(nTrials)
        for trial in range(0,nTrials):
            infBound= trials_data[trial]['States']['LEDon'][0]             
            supBound= trials_data[trial]['States']['LEDon'][1]      
            if 'Port1In' in trials_data[trial]['Events']:
                licks= trials_data[trial]['Events']['Port1In'] 
                if trial_types[trial]== 1:
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        alicksMinus[trial]= 1
                elif trial_types[trial]== 2:                
                    if np.any(licks>infBound) and np.any(licks<supBound):
                        alicksPlus[trial]= 1
        alicksConPlusPercent[day][mouse]= np.sum(alicksPlus)/(nTrialPlus)*100
        alicksConMinusPercent[day][mouse]= np.sum(alicksMinus)/(nTrialMinus)*100
        

# Compute mean 
meanExpPlus= np.zeros(3)
meanExpMinus= np.zeros(3)
meanConPlus= np.zeros(3)
meanConMinus= np.zeros(3)
for day in range(0,3):
    meanExpPlus[day]= np.mean(alicksExpPlusPercent[day])
    meanExpMinus[day]= np.mean(alicksExpMinusPercent[day])
    meanConPlus[day]= np.mean(alicksConPlusPercent[day])
    meanConMinus[day]= np.mean(alicksConMinusPercent[day])
        
# Plot  
mpl.rc('font', size=12)      
x_axesExp= np.arange(0.6,7.6,3)
x_axesCon= np.arange(1.4,8.4,3)
fig, ax= plt.subplots(ncols=2, constrained_layout=True)
fig.suptitle('Percent of trials with anticipatory licks', fontweight='bold')
exp1= ax.flat[0].boxplot(alicksExpPlusPercent, patch_artist=True, positions=x_axesExp)
con1= ax.flat[0].boxplot(alicksConPlusPercent, patch_artist=True, positions= x_axesCon)
exp2= ax.flat[1].boxplot(alicksExpMinusPercent, patch_artist=True, positions=x_axesExp)
con2= ax.flat[1].boxplot(alicksConMinusPercent, patch_artist=True, positions= x_axesCon)

ax.flat[0].set_title('CS+ trials')
ax.flat[1].set_title('CS- trials (no odor)')

# set control group in red and median line in black 
for day in range(0,3):
    exp1['boxes'][day].set_facecolor('blue')
    exp2['boxes'][day].set_facecolor('blue')
    con1['boxes'][day].set_facecolor('red')
    con2['boxes'][day].set_facecolor('red')
    plt.setp(exp1['medians'][day], color='black')
    plt.setp(con1['medians'][day], color='black')
    plt.setp(exp2['medians'][day], color='black')
    plt.setp(con2['medians'][day], color='black')

expL= mpatches.Patch(color='blue', label='Experimental group')
conL= mpatches.Patch(color='red', label='Control group')
for plot in range(0,2):
    ax.flat[plot].set_ylim(0,100)
    ax.flat[plot].set_xticks([1,4,7])
    ax.flat[plot].set_xticklabels(['Day 1', 'Day 2', 'Day 3'])
ax.flat[1].legend(handles=[expL, conL],
                     bbox_to_anchor=(1,1.02), loc='best')
