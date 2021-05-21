# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:53:57 2021

@author: ricca
"""

# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import os 
from scipy.io import loadmat
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt


# List of dirs + load data
# index        0       1       2      3       4       5      6      7     8       9
mouse_list= ['PV92','PV94','PV100','PV104','PV107','WT58','WT96','WT97','WT98','WT101']
mouse_name = mouse_list[1]  # CHANGE THIS
filepath= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\discrimination\learning analysis results'
os.chdir(filepath)
file_all= mouse_name + '_alldays.mat'
data_singleDay=[]
for session in range(0,3):
    file_singleDay= mouse_name + 'discr'+str(session+1)+'.mat'
    provData= loadmat(file_singleDay, simplify_cells=True)
    provData= provData['data']
    data_singleDay.append(provData)
data_allDays= loadmat(file_all, simplify_cells=True)
data_allDays= data_allDays['data']



# Plot learning curve
fig, ax = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
fig.suptitle(mouse_name.upper())
fig2, ax2= plt.subplots(nrows=2, ncols=2, constrained_layout=True)
fig2.suptitle(mouse_name.upper())
for session in range(0,3):
    # Plot learning curve
    t= np.arange(0, data_singleDay[session]['p'].size - 1)
    ax.flat[session].plot(t, data_singleDay[session]['pmode'][1:], 'r' ) 
    ax.flat[session].fill_between(t, data_singleDay[session]['p05'][1:], data_singleDay[session]['p95'][1:], alpha=0.4)
    ax.flat[session].axhline(y= data_singleDay[session]['BackgroundProb'], color='black', ls='--')
    ax.flat[session].set_title('Session '+str(session+1)+
                               ' IO(0.95)  Learning trial= '+str(data_singleDay[session]['cback'])+
                               ' Learning state process variance= '+
                               str(round(data_singleDay[session]['SigE']**2,3)))
    ax.flat[session].set_xlabel('Trial number')
    ax.flat[session].set_ylabel('Probability of a correct response') 
    ax.flat[session].set_ylim([0,1])
    #Plot IO certainty
    ax2.flat[session].plot(t, 1-data_singleDay[session]['pmatrix'][1:], linewidth=2, color='black')
    ax2.flat[session].set_title('Session '+str(session+1))
    ax2.flat[session].axhline(y= 0.9, color='blue', ls='--')
    ax2.flat[session].axhline(y= 0.95, color='blue', ls='--')
    ax2.flat[session].axhline(y= 0.99, color='blue', ls='--')
    ax2.flat[session].set_xlabel('Trial number')
    ax2.flat[session].set_ylabel('Certainty') 
    ax2.flat[session].set_ylim([0,1.05])



# Plot all session combined data
# learning curve
t_all= np.arange(0, data_allDays['p'].size - 1)
ax.flat[3].plot(t_all, data_allDays['pmode'][1:], 'r' ) 
ax.flat[3].fill_between(t_all, data_allDays['p05'][1:], data_allDays['p95'][1:], alpha=0.4)
ax.flat[3].axhline(y= data_allDays['BackgroundProb'], color='black', ls='--')
ax.flat[3].set_title('IO(0.95)  Learning trial= '+str(data_allDays['cback'])+
                           ' Learning state process variance= '+
                           str(round(data_allDays['SigE']**2,3)))
ax.flat[3].set_xlabel('Trial number')
ax.flat[3].set_ylabel('Probability of a correct response') 
ax.flat[3].set_ylim([0,1])
# IO certainty
ax2.flat[3].plot(t_all, 1-data_allDays['pmatrix'][1:], linewidth=2, color='black')
ax2.flat[3].set_title('All sessions combined')
ax2.flat[3].axhline(y= 0.9, color='blue', ls='--')
ax2.flat[3].axhline(y= 0.95, color='blue', ls='--')
ax2.flat[3].axhline(y= 0.99, color='blue', ls='--')
ax2.flat[3].set_xlabel('Trial number')
ax2.flat[3].set_ylabel('Certainty') 
ax2.flat[3].set_ylim([0,1.05])


