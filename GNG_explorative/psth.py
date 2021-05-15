# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:26:21 2021

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
from matplotlib.patches import Rectangle

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

# Load data 

os.chdir(mouse2m)
data=[]
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))
'''
os.chdir(mouse3m_r)
data=[]
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))
'''

# Plot
colors= [31,120,180],[106,61,154],[227,26,28],[251,127,0],[82,82,82]
colors= np.divide(colors, 251)

fig, ax= plt.subplots(nrows=2, ncols=2,constrained_layout=True)
fig.suptitle('Mouse 2M')
for day in range(0,len(data)):
    trial_types= data[day]['SessionData']['TrialTypes']
    trials_data= data[day]['SessionData']['RawEvents']['Trial']  # a list with every trial
    for TrialType in range(1,8):
        licksXtrial=[]
        idxTrialType= np.array(np.where(trial_types== TrialType))
        for Trial in range(0, idxTrialType.size):
            if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:    #if there was a PortIn 
                licks_ts= trials_data[idxTrialType[0][Trial]]['Events']['Port1In'] - 3
                licksXtrial.append(licks_ts)
        [R,t]= get_psth(licksXtrial, sig=0.1, time_windows= [-3, 15])
        if TrialType==1: 
            ax.flat[day].plot(t, R, color= colors[0], linewidth=2, label='CS1+')
        elif TrialType==2:
            ax.flat[day].plot(t, R, '--', color= colors[0], linewidth=2, label='CS1')
        elif TrialType==3: 
            ax.flat[day].plot(t, R, color= colors[1], linewidth=2, label='CS2+')
        elif TrialType==4: 
            ax.flat[day].plot(t, R, '--', color= colors[1], linewidth=2, label='CS2')
        elif TrialType==5: 
            ax.flat[day].plot(t, R, color= colors[2], linewidth=2, label='NS1')
        elif TrialType==6: 
            ax.flat[day].plot(t, R, color= colors[3], linewidth=2, label='NS2')
        elif TrialType==7: 
            ax.flat[day].plot(t, R, color= colors[4], linewidth=2, label='US')
        ax.flat[day].legend()
        ax.flat[day].set_title('Day '+str(day+1))
        ax.flat[day].axvline(color='black')
        ax.flat[day].set_xlabel('Time (s)')
        ax.flat[day].set_ylabel('Hz')
    ax.flat[day].add_patch(Rectangle((1,ax.flat[day].get_ylim()[0]),
                                     1,ax.flat[day].get_ylim()[1] + abs(ax.flat[day].get_ylim()[0]), 
                                     alpha=0.5))