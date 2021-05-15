# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 14:58:27 2021

@author: ricca
"""

import os 
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt


# setup and load data 
general_dir= r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Olfactory_go_nogo\Associative_learning_2' ###
specific_dir= r'1F\GNG_explorative_noTrialManager_2\Session Data' 
plot_dir= r'\1F\Plots'  
plot_name_date= '1F_day1' ###
os.chdir(general_dir + specific_dir)

#data= loadmat('3M_GNG_exporative_noTrialManager_20210124_120601.mat', simplify_cells=True)

import pickle 
with open('data_dict', 'rb') as data_dict_fil:
    data_1f= pickle.load(data_dict_fil)

# Setting up data
data= data['SessionData']
trial_types= data['TrialTypes']
number_of_trials= data['nTrials']
trial_data= data['RawEvents']['Trial']  # a list with every trial

# Data preprocessing 
trials_list=[]
for trial in range(0, number_of_trials):    #check all trials   
    if 'Port1In' in trial_data[trial]['Events']:    #if there was a PortIn 
        port1in= np.array([trial_data[trial]['Events']['Port1In']]) - 0.5
        trials_list.append(port1in)
    else:
        port1in= [0.0]
        trials_list.append(port1in)

rewarding_trials=[]
rewarding_trials_idx=[]
neutral_trials=[]
neutral_trials_idx=[]
us_trials=[]
us_trials_idx=[]
for i in range(0, number_of_trials):
    if trial_types[i]== 1 or trial_types[i]== 2 or trial_types[i]== 3 or trial_types[i]== 4:
        rewarding_trials.append(trials_list[i])
        rewarding_trials_idx.append(i+1)
    elif trial_types[i]== 5 or trial_types[i]== 6:
        neutral_trials.append(trials_list[i])
        neutral_trials_idx.append(i+1)
    elif trial_types[i]== 7:
        us_trials.append(trials_list[i])
        us_trials_idx.append(i+1)
 
    
# Plots
fig=go.Figure()
for i in range(0,len(rewarding_trials_idx)):
    if not isinstance(rewarding_trials[i][0], list): # if it's an array - exclude where there aren't response
        if not isinstance(rewarding_trials[i][0], np.float):
            yaxes= [rewarding_trials_idx[i]]*len(rewarding_trials[i][0])
            fig.add_trace(go.Scatter(x= rewarding_trials[i][0], y=yaxes,
                                     mode='markers', marker_color='blue', opacity=0.8))
fig.add_shape(type='line', y0=0, x0=0, y1=202, x1=0,
             line=dict(color='red', width=1))
fig.update_xaxes(title_text='Time (s)', showline=True, linecolor='black', linewidth=1, 
              autorange=True, ticks='outside') 
fig.update_yaxes(title_text= 'Trials', showline=True, linecolor='black', linewidth=1,
                 autorange='reversed', type='category', ticks='outside')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                  autosize=True,
                  margin=dict(t=25, b=0, r=10, l=10),
                  title='Rewarding trials')   
os.chdir(general_dir + plot_dir)
fig.write_image(plot_name_date+'_rewarding_stimulus_click_aligned.png')


fig=go.Figure()
for i in range(0,len(neutral_trials_idx)):
    if not isinstance(neutral_trials[i][0], list): # if it's an array 
                if not isinstance(neutral_trials[i][0], np.float):
                    yaxes= [neutral_trials_idx[i]]*len(neutral_trials[i][0])
                    fig.add_trace(go.Scatter(x= neutral_trials[i][0], y=yaxes,
                                             mode='markers', marker_color='blue', opacity=0.8))
fig.add_shape(type='line', y0=0, x0=0, y1=198, x1=0,
              line=dict(color='red', width=1))
fig.update_xaxes(title_text='Time (s)', showline=True, linecolor='black', linewidth=1, 
                autorange=True, ticks='outside') 
fig.update_yaxes(title_text= 'Trials', showline=True, linecolor='black', linewidth=1,
                 autorange='reversed', type='category', ticks='outside')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                  autosize=True,
                  margin=dict(t=25, b=0, r=10, l=10),
                  title='Neutral trials')   
os.chdir(general_dir + plot_dir)
fig.write_image(plot_name_date+'_neutral_stimulus_click_aligned.png')


fig=go.Figure()
for i in range(0,len(us_trials_idx)):
    if not isinstance(us_trials[i][0], list): # if it's an array 
            if not isinstance(us_trials[i][0], np.float):
                yaxes= [us_trials_idx[i]]*len(us_trials[i][0])
                fig.add_trace(go.Scatter(x= us_trials[i][0], y=yaxes,
                                         mode='markers', marker_color='blue', opacity=0.8))
fig.add_shape(type='line', y0=0, x0=0, y1=200, x1=0,
             line=dict(color='red', width=1))
fig.update_xaxes(title_text='Time (s)', showline=True, linecolor='black', linewidth=1, 
                autorange=True, ticks='outside') 
fig.update_yaxes(title_text= 'Trials', showline=True, linecolor='black', linewidth=1,
                 autorange='reversed', type='category', ticks='outside')
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
                  autosize=True,
                  margin=dict(t=25, b=0, r=10, l=10),
                  title='US trials')   
os.chdir(general_dir + plot_dir)
fig.write_image(plot_name_date+'_us_stimulus_click_aligned.png')