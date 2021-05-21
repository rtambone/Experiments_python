# -*- coding: utf-8 -*-
"""
Created on Fri May 21 12:27:28 2021

@author: ricca

Script for computing the avaraged by group PSTH during the generalization test
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


# Mpl parameters
mpl.rc('font', size=14)  
mpl.use('qt5agg')


# Define psth function
def get_psth(data, sig, time_windows, error_type= 'bootstrap', adaptive_warp=False): 
    """
    Function to get psth with a Gaussian kernel, defined by sig
    It returns t (timeline for x axes) and R (counts of occurences)
    Data is a matrix with rows= trials and columns= licks
    """
    #time_windows= np.array(time_windows)   
    import math
    import numpy as np
    nTrials= len(data)      #NT
    #D= np.array(nTrials, )
    nLicks= 0       #N_tot
    ND= np.zeros(nTrials)
    for i in range(0, nTrials):
        if isinstance(data[i], float):
            ND[i]= 1
            nLicks= nLicks+1
        else: 
            nLicks= nLicks + len(data[i])
            ND[i]= len(data[i])      #ND
    #licksMax= max(ND)       #N_max
    
    # if kernel density is such that there are on avarage one or less spikes
    # under the kernel then the units are probably wrong 
    try:
        L= nLicks/(nTrials*(time_windows[1]-time_windows[0]))
        if 2*L*nTrials*sig < 1 or L < 0.1:
            print('timestamps very low density')
    except ZeroDivisionError:
        print('Zero Division Error occured')
        
    # smear each spike out 
    # std dev is sqrt(rate*(integral over kernel^2)/trials) 
    # for gaussian integral over kernel^2 is 1/(2*sig*sqrt(pi))
    N_pts= np.fix(5*(time_windows[1]-time_windows[0])/sig)
    t= np.linspace(time_windows[0], time_windows[1], int(N_pts))
    
    RR= np.zeros((nTrials, int(N_pts)))
    f= 1/(2*sig**2)
    for n in range(0,nTrials):
        for m in range(0, int(ND[n])):
            if not isinstance(data[n], float):
                RR[n,:]= RR[n,:] + np.exp(-f*np.power(t-data[n][m],2))
            else: 
                RR[n,:]= RR[n,:] + np.exp(-f*np.power(t-data[n],2))
    RR= RR*(1/np.sqrt(2*math.pi*sig**2))
    #if nTrials > 1:
    R= np.mean(RR, axis=0) 
    #else: 
    #   R= RR
    
    
    
    # adaptive warp sig, so that on avarage the number of spikes under the kernel
    # but regions where there is more data have a smaller kernel
    if adaptive_warp== True:
        sigt= np.mean(R)*sig/R
        RR= np.zeros(nTrials, N_pts)
        f= 1/(2*sigt**2)
        for n in range(0,nTrials):
            for m in range(0, int(ND[n])):
                RR[n,:]= RR[n,:] + np.exp(-f*np.power(t-data[n][m],2))
        RR= RR*(1/np.sqrt(2*math.pi*sig**2))
        if nTrials > 1:
            R= np.mean(RR, axis=0)
        else: 
            R= RR
    
    return R, t, 

# List of dirs
# index        0       1       2      3       4       
expGroup= ['PV92','PV94','PV100','PV104','PV107']
conGroup= ['WT58','WT96','WT97','WT98','WT101']
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\pavlovian'
nTrials= 20


# Load data for experimental group 
R_expF= np.zeros((5,1300))  
t_expF= np.zeros((5,1300))
R_expN= np.zeros((5,1300))
t_expN= np.zeros((5,1300))
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
    for TrialType in range(1,3):
        licksXtrial=[]
        idxTrialType= np.array(np.where(trial_types== TrialType))
        for Trial in range(0, idxTrialType.size):
            if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:    #if there was a PortIn 
               licks_ts= trials_data[idxTrialType[0][Trial]]['Events']['Port1In']   # centered on valve opening
               licksXtrial.append(licks_ts)
        [R,t]= get_psth(licksXtrial, sig=0.1, time_windows= [-1, 25])
        if TrialType==1:    # valve click no odor
            R_expN[mouse]= R
            t_expN[mouse]= t
        elif TrialType==2:
            R_expF[mouse]= R
            t_expF[mouse]= t


'''
meanExpR_fam=[[],[],[]]
meanExpR_novel=[[],[],[]]
semExpR_fam=[[],[],[]]
semExpR_novel= [[],[],[]]
for day in range(0,3):
    meanExpR_Plus[day]= np.mean(R_exp_csP[day], axis=0)
    meanExpR_Minus[day]= np.mean(R_exp_csM[day], axis=0)
    semExpR_Plus[day]= sem(R_exp_csP[day], axis=0)
    semExpR_Minus[day]= sem(R_exp_csM[day], axis=0)
'''

# Load data for control group 
R_conF= np.zeros((5,1300))  
t_conF= np.zeros((5,1300))
R_conN= np.zeros((5,1300))
t_conN= np.zeros((5,1300))
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
    for TrialType in range(1,3):
        licksXtrial=[]
        idxTrialType= np.array(np.where(trial_types== TrialType))
        for Trial in range(0, idxTrialType.size):
            if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:    #if there was a PortIn 
               licks_ts= trials_data[idxTrialType[0][Trial]]['Events']['Port1In']   # centered on valve opening
               licksXtrial.append(licks_ts)
        [R,t]= get_psth(licksXtrial, sig=0.1, time_windows= [-1, 25])
        if TrialType==1:    # valve click no odor
            R_conN[mouse]= R
            t_conN[mouse]= t
        elif TrialType==2:
            R_conF[mouse]= R
            t_conF[mouse]= t



#Plot 
colors= [31,120,180],[106,61,154],[227,26,28],[251,127,0],[82,82,82]
colors= np.divide(colors, 251)
# dividi in due i plot per ogni gruppo 
fig, ax= plt.subplots(ncols=2, constrained_layout=True)
fig.suptitle('Generalization test', fontweight='bold')
ax[0].plot(t, np.mean(R_expF, axis=0), color=colors[2], label='Familiar odor',
        lw=2)
ax[0].plot(t, np.mean(R_expN, axis=0), color=colors[2], label='Novel odor', 
        lw=2, ls='--')
ax[1].plot(t, np.mean(R_conF, axis=0), color=colors[4], label='Familiar odor',
        lw=2)
ax[1].plot(t, np.mean(R_conN, axis=0), color=colors[4], label='Novel odor', 
        lw=2, ls='--')




ax.axvline(color='blue', x=5, ls='--')
ax.axvline(color='blue', x=7, ls='--')
ax.axvline(color='black', x=10, ls='--')
ax.axvline(color='black', x=11, ls='--')
ax.legend()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Hz')

for day in range(0,3):
    ax[day,0].plot(t, meanExpR_Plus[day], color=colors[2], label='Cymene')
    ax[day,0].plot(t, meanExpR_Minus[day], color=colors[4], label='No odor')
    ax[day,1].plot(t, meanConR_Plus[day], color=colors[2], label='Cymene')
    ax[day,1].plot(t, meanConR_Minus[day], color=colors[4], label='No odor')
    ax[day,0].fill_between(t, meanExpR_Plus[day]+semExpR_Plus[day], meanExpR_Plus[day]-semExpR_Plus[day], 
                           color= colors[2], alpha=0.4)
    ax[day,0].fill_between(t, meanExpR_Minus[day]+semExpR_Minus[day], meanExpR_Minus[day]-semExpR_Minus[day], 
                           color= colors[4], alpha=0.4)
    ax[day,1].fill_between(t, meanConR_Plus[day]+semConR_Plus[day], meanConR_Plus[day]-semConR_Plus[day], 
                           color= colors[2], alpha=0.4)
    ax[day,1].fill_between(t, meanConR_Minus[day]+semConR_Minus[day], meanConR_Minus[day]-semConR_Minus[day], 
                           color= colors[4], alpha=0.4)
    ax[day,0].axvline(color='blue', x=5, ls='--')
    ax[day,0].axvline(color='blue', x=7, ls='--')
    ax[day,0].axvline(color='black', x=10, ls='--')
    ax[day,0].axvline(color='black', x=11, ls='--')
    ax[day,1].axvline(color='blue', x=5, ls='--')
    ax[day,1].axvline(color='blue', x=7, ls='--')
    ax[day,1].axvline(color='black', x=10, ls='--')
    ax[day,1].axvline(color='black', x=11, ls='--')
    ax[day,0].set_ylabel('Day '+str(day+1), fontweight='bold')
    ax[day,0].set_ylim(0,8)
    ax[day,1].set_ylim(0,8)
    ax[day,0].set_xlim(-1,25)
    ax[day,1].set_xlim(-1,25)
ax[0,1].legend()    
ax[0,0].set_title('Experimental group')
ax[0,1].set_title('Control group')
ax[2,0].set_xlabel('Time (s)')
ax[2,1].set_xlabel('Time (s)')
