# -*- coding: utf-8 -*-
"""
Created on Thu May 20 21:26:31 2021

@author: ricca

Script for computing and plotting the count of alicks during the 
generalization test 
"""

from IPython import get_ipython
get_ipython().magic('reset -sf')


import os 
import glob 
from scipy.io import loadmat
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Mpl parameters
mpl.rc('font', size=14)  
mpl.use('qt5agg')


# Define function to count number of licks 
def count_licks(data, window):
    count= 0 
    if isinstance(data, float):
        if window[0]<data<window[1]:
            count+=1
    else:
        for el in data:
            if window[0]<el<window[1]:
                count+= 1
    return count 

# List of dirs
# index        0       1       2      3       4       
expGroup= ['PV92','PV94','PV100','PV104','PV107']
conGroup= ['WT58','WT96','WT97','WT98','WT101']
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\discrimination'
nTrials= 20

# Experimental group 
meanExpPlus= [] 
meanExpMinus= []
for mouse in range(0,5):
    mouseName= expGroup[mouse]
    mouse_dir= general_dir + '\\'+ mouseName
    os.chdir(mouse_dir)
    data_mouse=[]
    for file in glob.glob('*.mat'):
        data_mouse.append(loadmat(file, simplify_cells=True))
    data= data_mouse[0]
    trial_types= data['SessionData']['TrialTypes'][0:nTrials]
    trials_data= data['SessionData']['RawEvents']['Trial'][0:nTrials] # a list with every trial
    nTrialPlus= len(np.where(trial_types==2)[0])
    nTrialMinus= len(np.where(trial_types==1)[0])
    alicksPlus= []
    alicksMinus= []
    for trial in range(0,nTrials):
        infBound= trials_data[trial]['States']['LEDon'][0]             
        supBound= trials_data[trial]['States']['LEDon'][1]                  
        if 'Port1In' in trials_data[trial]['Events']:
            licks= trials_data[trial]['Events']['Port1In'] 
            if trial_types[trial]== 1:
                alicksMinus.append(count_licks(licks, [infBound, supBound]))
            elif trial_types[trial]== 2:                
                alicksPlus.append(count_licks(licks, [infBound, supBound]))
        else:
            if trial_types[trial]==1:
                alicksMinus.append(0)
            if trial_types[trial]==2:
                alicksMinus.append(0)
    meanExpPlus.append(np.nanmean(alicksPlus))
    meanExpMinus.append(np.nanmean(alicksMinus))

        
# Control group 
meanConPlus= []
meanConMinus= []
for mouse in range(0,5):
    mouseName= conGroup[mouse]
    mouse_dir= general_dir + '\\'+ mouseName
    os.chdir(mouse_dir)
    data_mouse=[]
    for file in glob.glob('*.mat'):
        data_mouse.append(loadmat(file, simplify_cells=True))
    data= data_mouse[0]
    trial_types= data['SessionData']['TrialTypes'][0:nTrials]
    trials_data= data['SessionData']['RawEvents']['Trial'][0:nTrials] # a list with every trial
    nTrialPlus= len(np.where(trial_types==2)[0])
    nTrialMinus= len(np.where(trial_types==1)[0])
    alicksPlus= []
    alicksMinus= []
    for trial in range(0,nTrials):
        infBound= trials_data[trial]['States']['LEDon'][0]             
        supBound= trials_data[trial]['States']['LEDon'][1]                  
        if 'Port1In' in trials_data[trial]['Events']:
            licks= trials_data[trial]['Events']['Port1In'] 
            if trial_types[trial]== 1:
                alicksMinus.append(count_licks(licks, [infBound, supBound]))
            elif trial_types[trial]== 2:                
                alicksPlus.append(count_licks(licks, [infBound, supBound]))
        else:
            if trial_types[trial]== 1:
                alicksMinus.append(0)
            if trial_types[trial]== 2:
                alicksMinus.append(0)       
    meanConPlus.append(np.nanmean(alicksPlus))
    meanConMinus.append(np.nanmean(alicksMinus))
        
        
# Boxlot alicksFreq exp VS control 
meanPlus=[]     # data of exp and con group with novel odor
meanPlus.append(meanExpPlus)
meanPlus.append(meanConPlus)
meanMinus=[]    # data of exp and con group with familiar odor
meanMinus.append(meanExpMinus)
meanMinus.append(meanConMinus)
x_axes1= [0.9, 1.1]
x_axes2= [1.9, 2.1]
fig, ax= plt.subplots(constrained_layout=True)
fig.suptitle('Frequency of anticipatory lickings', fontweight='bold')
familiar= ax.boxplot(meanPlus, patch_artist=True, showfliers= True, positions= x_axes1)
novel= ax.boxplot(meanMinus, patch_artist=True, showfliers= True, positions=x_axes2)
familiar['boxes'][0].set_facecolor('blue')
familiar['boxes'][1].set_facecolor('red')
novel['boxes'][0].set_facecolor('blue')
novel['boxes'][1].set_facecolor('red')
for i in range(0,2):
    plt.setp(familiar['medians'][i], color='black')
    plt.setp(novel['medians'][i], color='black')
expL= mpatches.Patch(color='blue', label='Experimental group')
conL= mpatches.Patch(color='red', label='Control group')
ax.set_ylabel('Hz')
ax.set_xticks([1,2])
ax.set_xticklabels(['Familiar odor', 'Novel odor'])
ax.legend(handles=[expL, conL],
          bbox_to_anchor=(1,1), loc='best')
#plt.setp(novel['medians'][1], color='black')


