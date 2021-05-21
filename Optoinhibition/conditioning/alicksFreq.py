# -*- coding: utf-8 -*-
"""
Created on Thu May 20 15:25:17 2021

@author: ricca
"""
# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import os 
import glob 
from scipy.io import loadmat
from scipy.stats import sem 
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
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'


# Experimental group 
meanExpPlus= [[],[],[]] 
semExpPlus= [[],[],[]] 
meanExpMinus= [[],[],[]] 
semExpMinus= [[],[],[]] 
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
        meanExpPlus[day].append(np.mean(alicksPlus))
        meanExpMinus[day].append(np.mean(alicksMinus))
        semExpPlus[day].append(sem(alicksPlus))
        semExpMinus[day].append(sem(alicksMinus))

        
# Control group 
meanConPlus= [[],[],[]] 
semConPlus= [[],[],[]] 
meanConMinus= [[],[],[]] 
semConMinus= [[],[],[]] 
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

        meanConPlus[day].append(np.mean(alicksPlus))
        meanConMinus[day].append(np.mean(alicksMinus))
        semConPlus[day].append(sem(alicksPlus))
        semConMinus[day].append(sem(alicksMinus))
        
        
# Boxlot alicksFreq exp VS control   
x_axesExp= np.arange(0.7,7.7,3)
x_axesCon= np.arange(1.3,8.3,3)

fig, ax= plt.subplots(ncols=2, constrained_layout=True)
fig.suptitle('Frequency of anticipatory lickings', fontweight='bold')
exp1= ax.flat[0].boxplot(meanExpPlus, patch_artist=True, positions=x_axesExp, showfliers= False)
con1= ax.flat[0].boxplot(meanConPlus, patch_artist=True, positions= x_axesCon, showfliers= False)
exp2= ax.flat[1].boxplot(meanExpMinus, patch_artist=True, positions=x_axesExp, showfliers= False)
con2= ax.flat[1].boxplot(meanConMinus, patch_artist=True, positions= x_axesCon, showfliers= False)

ax.flat[0].set_title('CS+ trials')
ax.flat[1].set_title('CS- trials (no odor)')
for day in range(0,3):                  # set control group in red and median line in black 
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
    ax.flat[plot].set_ylim(0,1.5)
    ax.flat[plot].set_ylabel('Hz')
    ax.flat[plot].set_xticks([1,4,7])
    ax.flat[plot].set_xticklabels(['Day 1', 'Day 2', 'Day 3'])
ax.flat[1].legend(handles=[expL, conL],
                     bbox_to_anchor=(1,1), loc='best')


# Boxplot alicksFreq cs+ VS cs-
fig, ax= plt.subplots(ncols=2, constrained_layout=True)
fig.suptitle('Frequency of anticipatory lickings', fontweight='bold')
exp1= ax.flat[0].boxplot(meanExpPlus, patch_artist=True, positions=x_axesExp, showfliers= False)
exp2= ax.flat[0].boxplot(meanExpMinus, patch_artist=True, positions=x_axesCon, showfliers= False)
con1= ax.flat[1].boxplot(meanConPlus, patch_artist=True, positions= x_axesExp, showfliers= False)
con2= ax.flat[1].boxplot(meanConMinus, patch_artist=True, positions= x_axesCon, showfliers= False)

ax.flat[0].set_title('Experimental group')
ax.flat[1].set_title('Control group')
for day in range(0,3):                  # set control group in red and median line in black 
    exp1['boxes'][day].set_facecolor('blue')
    exp2['boxes'][day].set_facecolor('red')
    con1['boxes'][day].set_facecolor('blue')
    con2['boxes'][day].set_facecolor('red')
    plt.setp(exp1['medians'][day], color='black')
    plt.setp(con1['medians'][day], color='black')
    plt.setp(exp2['medians'][day], color='black')
    plt.setp(con2['medians'][day], color='black')
cspL= mpatches.Patch(color='blue', label='CS+ trials')
csmL= mpatches.Patch(color='red', label='Cs- trials')
for plot in range(0,2):
    #ax.flat[plot].set_ylim(0,1.5)
    ax.flat[plot].set_ylabel('Hz')
    ax.flat[plot].set_xticks([1,4,7])
    ax.flat[plot].set_xticklabels(['Day 1', 'Day 2', 'Day 3'])
ax.flat[1].legend(handles=[cspL, csmL],
                     bbox_to_anchor=(1,1), loc='best')



# Plot mean and sem plus individual data
meanExpPlus_pop= np.zeros(3)
meanExpMinus_pop= np.zeros(3)
meanConPlus_pop= np.zeros(3)
meanConMinus_pop= np.zeros(3)
for day in range(0,3):
    meanExpPlus_pop[day]= np.mean(meanExpPlus[day])
    meanExpMinus_pop[day]= np.mean(meanExpMinus[day])
    meanConPlus_pop[day]= np.mean(meanConPlus[day])
    meanConMinus_pop[day]= np.mean(meanConMinus[day])
semExpPlus_pop= sem(semExpPlus)
semExpMinus_pop= sem(semExpMinus)
semConPlus_pop= sem(semConPlus)
semConMinus_pop= sem(semConMinus)


x_axesExp= np.arange(0.8,7.8,3)
x_axesCon= np.arange(1.2,8.2,3)
fig, ax= plt.subplots(ncols=2, constrained_layout=True)
fig.suptitle('Frequency of anticipatory lickings \n mean and sem', fontweight='bold')
# Exp
ax[0].plot(x_axesExp, meanExpPlus_pop,  
           ls='-', marker='o', ms=16, color='blue', label='Experimental group')
ax[0].plot(x_axesExp, meanExpPlus,  
           ls='none', marker='o', ms=12, color='blue', alpha=0.6)
ax[1].plot(x_axesExp, meanExpMinus_pop,  
           ls='-', marker='o', ms=16, color='blue', label='Experimental group')
ax[1].plot(x_axesExp, meanExpMinus,  
           ls='none', marker='o', ms=12, color='blue', alpha=0.6)

# Con
ax[0].plot(x_axesCon, meanConPlus_pop,  
           ls='-', marker='o', ms=16, color='red', label='Control group')
ax[0].plot(x_axesCon, meanConPlus,  
           ls='none', marker='o', ms=12, color='red', alpha=0.6)
ax[1].plot(x_axesCon, meanConMinus_pop,  
           ls='-', marker='o', ms=16, color='red', label='Control group')
ax[1].plot(x_axesCon, meanConMinus,  
           ls='none', marker='o', ms=12, color='red', alpha=0.6)

ax[0].set_title('CS+ trials')
ax[1].set_title('CS- trials (no odor)')
for plot in range(0,2):
    ax.flat[plot].set_ylim(-0.05,3)
    ax.flat[plot].set_ylabel('Hz')
    ax.flat[plot].set_xticks([1,4,7])
    ax.flat[plot].set_xticklabels(['Day 1', 'Day 2', 'Day 3'])
ax.flat[1].legend(handles=[expL, conL],
                     bbox_to_anchor=(1,1), loc='best')


