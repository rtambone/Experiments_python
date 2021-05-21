# -*- coding: utf-8 -*-
"""
Created on Sun May 16 10:04:20 2021

@author: ricca
"""

# Script for comparing the learning trials between experimental and control groups

# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import matplotlib
import glob
import os
import pingouin as pg
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
matplotlib.use('qt5agg')


# List of dirs
# index        0       1       2      3       4       5      6      7     8       9
mouse_list= ['PV92','PV94','PV100','PV104','PV107','WT58','WT96','WT97','WT98','WT101']
mouse_name = mouse_list[1]  # CHANGE THIS
#day = '2'                   # AND THIS
#general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'
#mouse_dir = general_dir + '\\' + mouse_name

exp_group_idx= mouse_list[0:5]
control_group_idx= mouse_list[5:]

exp_learningTrials= [166, 151]
control_learningTrials= []

# Compute mean and std 
exp_mean= np.mean(exp_learningTrials)
control_mean= np.mean(control_learningTrials)
exp_std= np.std(exp_learningTrials)
control_std= np.std(control_learningTrials)

# Mann-Whitney U test
results= pg.mwu(exp_learningTrials, control_learningTrials, tail='one-sided')


# Plot
fig, ax= plt.subplots(nrows=1, ncols=1,constrained_layout=True)
fig.suptitle('Learning trials differences')




# Plot to copy 
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

