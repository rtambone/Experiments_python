# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:44:22 2021

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
mouse_name = mouse_list[3]  # CHANGE THIS
session= 0
#session_type= '\\pavlovian'
session_type= '\\discrimination'
filepath= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp' + session_type+'\learning analysis results'
os.chdir(filepath)
###
'''
filenameCond= mouse_name + '_day'+str(session+1)+'.mat'
data= loadmat(filenameCond, simplify_cells=True)
'''
###

filenameDiscr= mouse_name + 'discr'+str(session+1)+'.mat'
data= loadmat(filenameDiscr, simplify_cells=True)

###
data= data['data']



fig, ax= plt.subplots(nrows=2, ncols=1,constrained_layout=True)
fig.suptitle(mouse_name)
# Plot learning curve
t= np.arange(0, data['p'].size - 1)
ax.flat[0].plot(t, data['pmode'][1:], 'r' ) 
ax.flat[0].fill_between(t, data['p05'][1:], data['p95'][1:], alpha=0.4)
ax.flat[0].axhline(y= data['BackgroundProb'], color='black', ls='--')
ax.flat[0].set_title('IO(0.95)  Learning trial= '+str(data['cback'])+
                           ' Learning state process variance= '+
                           str(round(data['SigE']**2,3)))
ax.flat[0].set_xlabel('Trial number')
ax.flat[0].set_ylabel('Probability of a correct response') 
ax.flat[0].set_ylim([0,1])

# IO certainty
ax.flat[1].plot(t, 1-data['pmatrix'][1:], linewidth=2, color='black')
#ax.flat[3].set_title('')
ax.flat[1].axhline(y= 0.9, color='blue', ls='--')
ax.flat[1].axhline(y= 0.95, color='blue', ls='--')
ax.flat[1].axhline(y= 0.99, color='blue', ls='--')
ax.flat[1].set_xlabel('Trial number')
ax.flat[1].set_ylabel('Certainty') 
ax.flat[1].set_ylim([0,1.05])


