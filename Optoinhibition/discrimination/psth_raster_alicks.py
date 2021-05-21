# -*- coding: utf-8 -*-
"""
Created on Mon May 17 19:49:25 2021

@author: ricca
"""

# clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')


import os 
import glob 
from scipy.io import loadmat
import numpy as np
import matplotlib 
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
# index        0       1       2      3       4       5      6      7     8       9
mouse_list= ['PV92','PV94','PV100','PV104','PV107','WT58','WT96','WT97','WT98','WT101']
mouse_name = mouse_list[1]  # CHANGE THIS
day= '2'                    # AND THIS
general_dir = r'C:\Users\ricca\Documents\Iurilli Lab\Experiments\Optoinhibition\optoinhibition\exp\discrimination'
mouse_dir= general_dir + '\\'+ mouse_name


# Load data 
os.chdir(mouse_dir)
data=[]
for file in glob.glob('*.mat'):
    data.append(loadmat(file, simplify_cells=True))

trial_types= data[int(day)]['SessionData']['TrialTypes']
trials_data= data[int(day)]['SessionData']['RawEvents']['Trial'] # a list with every trial
nTrials= len(trial_types)
nTrialPlus= len(np.where(trial_types==2)[0])
nTrialMinus= len(np.where(trial_types==1)[0])


# Processing for raster plots 
csMinus = []
csPlus = []
csPlus_idx = np.array(np.where(trial_types == 2))
csPlus_idx = csPlus_idx.reshape(csPlus_idx.shape[1])
csMinus_idx = np.array(np.where(trial_types == 1))
csMinus_idx = csMinus_idx.reshape(csMinus_idx.shape[1])
for TrialType in range(1, 3):
    licksXtrial = []
    idxTrialType = np.array(np.where(trial_types == TrialType))
    for Trial in range(0, idxTrialType.size):
        # if there was a PortIn
        if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:
            licks_ts = np.array(
                trials_data[idxTrialType[0][Trial]]['Events']['Port1In'])
            if licks_ts.shape == ():
                licks_ts = licks_ts.reshape(1)
            if TrialType == 1:    # valve click no odor
                csMinus.append(licks_ts)
            elif TrialType == 2:
                csPlus.append(licks_ts)


# Processing for aLicks
csMinusTrials= np.zeros(nTrials)
alicks_csMinus= np.zeros(nTrials)
csPlusTrials= np.zeros(nTrials)
alicks_csPlus= np.zeros(nTrials)
for trial in range(0,nTrials):
    infBound= trials_data[trial]['States']['LEDon'][0]             
    supBound= trials_data[trial]['States']['LEDon'][1] 
    if trial_types[trial]== 1:
        csMinusTrials[trial]= 1 
    else:
        csPlusTrials[trial]=1
    if 'Port1In' in trials_data[trial]['Events']:
        licks= trials_data[trial]['Events']['Port1In'] 
        if trial_types[trial]== 1:
            if np.any(licks>infBound) and np.any(licks<supBound):
                alicks_csMinus[trial]= 1
        elif trial_types[trial]== 2:                
            if np.any(licks>infBound) and np.any(licks<supBound):
                alicks_csPlus[trial]= 1
percentCsPlus= np.zeros(nTrials-5)
percentCsMinus= np.zeros(nTrials-5)
for trial in range(5,nTrials):
    percentCsPlus[trial-5]= np.sum(alicks_csPlus[:trial])/np.sum(csPlusTrials[:trial])*100
    percentCsMinus[trial-5]= np.sum(alicks_csMinus[:trial])/np.sum(csMinusTrials[:trial])*100
cum_alicksOdor_convolved= np.convolve(percentCsPlus, np.ones(5)/5, mode= 'valid')
cum_alicksNoOdor_convolved= np.convolve(percentCsMinus, np.ones(5)/5, mode= 'valid')




# Plot PSTH 
colors= [31,120,180],[106,61,154],[227,26,28],[251,127,0],[82,82,82]
colors= np.divide(colors, 251)

fig, ax= plt.subplots(nrows=2, ncols=2,constrained_layout=True)
fig.suptitle(mouse_name)
for TrialType in range(1,3):
    licksXtrial=[]
    idxTrialType= np.array(np.where(trial_types== TrialType))
    for Trial in range(0, idxTrialType.size):
        if 'Port1In' in trials_data[idxTrialType[0][Trial]]['Events']:    #if there was a PortIn 
           licks_ts= trials_data[idxTrialType[0][Trial]]['Events']['Port1In']   # centered on valve opening
           licksXtrial.append(licks_ts)
    [R,t]= get_psth(licksXtrial, sig=0.1, time_windows= [-2, 26])
    if TrialType==1:    # valve click no odor
        ax.flat[0].plot(t, R, color= colors[4], linewidth=1.5, label='CS-')
    elif TrialType==2:
        ax.flat[0].plot(t, R, color= colors[2], linewidth=1.5, label='CS+')
    ax.flat[0].legend()
    ax.flat[0].set_title('')
    #ax.axvline(color='black', x=6)
    ax.flat[0].set_xlabel('Time (s)')
    ax.flat[0].set_ylabel('Hz')
ax.flat[0].add_patch(Rectangle((5,0), 
                       width= 2, height= abs(ax.flat[0].get_ylim()[1]),
                       alpha=0.5))
ax.flat[0].add_patch(Rectangle((10,0), 
                       width= 1, height= abs(ax.flat[0].get_ylim()[1]),
                              alpha=0.5, color= 'red'))


# Plot raster
#fig, ax = plt.subplots(nrows=1, ncols=2, constrained_layout=True)
#fig.suptitle(mouse_name)
ax.flat[2].eventplot(csMinus, colors='black')  # lineoffsets= csMinus_idx)
ax.flat[3].eventplot(csPlus, colors='black')
ax.flat[2].set_title('Carvone \n trials with aLicks = ' + str(round(percentCsMinus[-1]))+'%')
ax.flat[3].set_title('Cymene \n trials with aLicks = ' + str(round(percentCsPlus[-1],2))+'%')
for i in range(2, 4):
    ax.flat[i].set_ylim([0,nTrials/2])
    ax.flat[i].plot([4,8],[0.3,0.3], color='red')                # red line for optoinhibition
    #ax[i].axvline(color='blue', x=5)                        # blue vertical line for odor onset
    ax.flat[i].set_xlabel('Time (s)')
    ax.flat[i].set_ylabel('Trials')
    ax.flat[i].add_patch(Rectangle((5,0), 
                              width= 2, height= abs(ax.flat[i].get_ylim()[1]),
                              alpha=0.5))
    ax.flat[i].add_patch(Rectangle((10,0), 
                              width= 1, height= abs(ax.flat[i].get_ylim()[1]),
                              alpha=0.5, color= 'red'))


# Plot aLicks
plot_trials= len(cum_alicksOdor_convolved)
x_axes= np.arange(0,plot_trials)
#fig, ax= plt.subplots(constrained_layout=True)
#fig.suptitle(mouse_name)
ax.flat[1].plot(x_axes, cum_alicksOdor_convolved[:plot_trials], 'b', label='Odor trials')
ax.flat[1].plot(x_axes, cum_alicksNoOdor_convolved[:plot_trials], 'r', label='No odor trials')
ax.flat[1].legend(loc='best')
ax.flat[1].set_ylabel('% Trials with aLicks')
ax.flat[1].set_xlabel('Trial')
#ax.set_ylim([-100,100])
ax.flat[1].axhline(y= 20, color='black', ls='--')
ax.flat[1].axhline(y= 80, color='black', ls='--')

