# -*- coding: utf-8 -*-
"""
Created on Sat May 15 12:56:33 2021

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
filepath= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian\learning analysis results'
file= mouse_name + '_alldays.mat'

os.chdir(filepath)
data= loadmat(file, simplify_cells=True)
data= data['data']

# Preprocess data 
t= np.arange(0, data['p'].size - 1)

# Plot learning curve
fig, ax = plt.subplots(nrows=2, ncols=1, constrained_layout=True)
fig.suptitle(mouse_name.upper())
ax[0].plot(t, data['pmode'][1:], 'r' ) 
ax[0].fill_between(t, data['p05'][1:], data['p95'][1:], alpha=0.4)
'''
if data['MaxResponse'] == 1:
    x= np.array(np.where(data['Responses'] > 0))
    y= np.ones((1, x.size))
    h= ax[0].plot(x, y+0.05, 's', markerfacecolor= 'black', markeredgecolor='black')
    x= np.array(np.where(data['Responses'] == 0))
    y= np.ones((1, x.size))
    h= ax[0].plot(x,y+0.05, 's', markerfacecolor= [0.75, 0.75, 0.75], markeredgecolor='black')

else:
    ax[0].plot(t, data['Responses']/data['MaxResponse'],'ko')
'''
ax[0].axhline(y= data['BackgroundProb'], color='black', ls='--')
ax[0].set_title('IO(0.95)  Learning trial= '+str(data['cback'])+' Learning state process variance= '+str(round(data['SigE']**2,4)))
ax[0].set_xlabel('Trial number')
ax[0].set_ylabel('Probability of a correct response') 
ax[0].set_ylim([0,1])

# Plot IO certainty 
ax[1].plot(t, 1-data['pmatrix'][1:], linewidth=2, color='black')
ax[1].axhline(y= 0.9, color='blue', ls='--')
ax[1].axhline(y= 0.95, color='blue', ls='--')
ax[1].axhline(y= 0.99, color='blue', ls='--')
ax[1].set_xlabel('Trial number')
ax[1].set_ylabel('Certainty') 
ax[1].set_ylim([0,1])

